#!/usr/bin/python3
import discord
import base64
import re
from datetime import datetime
import psycopg2

after = None
pl = None
page = None
embed = None
embeds = None

class myClient(discord.Client):

  # Coroutine to login
    async def on_ready(self):
        print(f'Logged in as {client.user}'.format(client))

    # pagination
    async def on_raw_reaction_add(self, payload):
        global pl, page, embed, embeds, d
        if embeds and pl and payload.message_id==pl.id and payload.user_id!=client.user.id:
            if payload.emoji.name == '⏪' and page > 0:
                page = 0
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '◀️' and page > 0:
                page -= 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '▶️' and page < len(embeds) -1:
                page += 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '⏩' and page < len(embeds) -1:
                page = len(embeds)-1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)

    # pagination
    async def on_raw_reaction_remove(self, payload):
        global pl, page, embed, embeds
        if embeds and pl and payload.message_id==pl.id:
            if payload.emoji.name == '⏪' and page > 0:
                page = 0
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '◀️' and page > 0:
                page -= 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '▶️' and page < len(embeds) -1:
                page += 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            elif payload.emoji.name == '⏩' and page < len(embeds) -1:
                page = len(embeds)-1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)


  # Coroutine to answer messages
    async def on_message(self, ctx):
        global after, pl, page, embeds, embed
        botl = {'groovy': '-', 'rythm': '!', 'rythm2': '>'}

        # auth :p
        if ctx.author==client.user:
            return
        else:
            msg = (await ctx.channel.history(limit=1).flatten())[0]
            if msg.content.lower().startswith('pl '):
                m = msg.content[3:]

                # ping
                if m.lower().startswith('ping'):
                    await ctx.channel.send(f'pong in {round(client.latency * 1000)}ms :)')

                # help
                if m.lower().startswith('help'):
                    embed = discord.Embed(title='PLBot', color=ctx.author.color, description='A bot to manage groovy playlists!\nPrefix for this bot is `pl `.')
                    embed.add_field(inline=False, name='`pl startl`', value='Start listening to groovy commands at this point.')
                    embed.add_field(inline=False, name='`pl save plname`', value='Save the current playlist as plname.')
                    embed.add_field(inline=False, name='`pl list [plname]`', value='List all songs in [plname] or all available playlists if invalid.')
                    embed.add_field(inline=False, name='`pl [groovy|rythm|rythm2] plname`', value='Queue plname using the specified music bot.')
                    embed.add_field(inline=False, name='`pl rename old new`', value='Rename playlist old to new.')
                    embed.add_field(inline=False, name='`pl drop plname`', value='Delete playlist plname.')
                    embed.add_field(inline=False, name='`pl trim plname [space seperated indices]`', value='Remove songs at specified indices from plname.')
                    await ctx.channel.send(embed=embed)

                # start listening
                if m.lower().startswith('startl'):
                    await ctx.add_reaction('😌️')
                    after = datetime.now()

                # save playlist
                elif m.lower().startswith('save'):
                    m = m[5:]
                    await ctx.channel.send('-q', delete_after=1)
                    await ctx.channel.send(f'Saving this queue as playlist `{m}`')
                    dbconn = psycopg2.connect("dbname=DPL")
                    cursor = dbconn.cursor()
                    cursor.execute(f"SELECT * FROM playlists WHERE name='{m}'")
                    if not cursor.fetchall():
                        cursor.execute(f"INSERT INTO playlists (name) VALUES ('{m}')")
                        cursor.execute(f"CREATE TABLE {m} (id serial primary key, title text not NULL, url text, uid text)")
                    async for msg in ctx.channel.history(after=after):
                        if msg.embeds and msg.embeds[0].description:
                            if msg.embeds[0].description.startswith("Queued"):
                                q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
                                if q:
                                    song, link, id = q[0]
                                    cursor.execute(f"INSERT INTO {m} (title, url, uid) VALUES ('{song}', '{link}', '{id}')")
                            elif msg.embeds[0].description.startswith("Removed"):
                                song, link = re.findall("\[(.*)\]\((.*)\)", msg.embeds[0].description)[0]
                                cursor.execute(f"SELECT id FROM {m} WHERE url='{link}' ORDER BY id DESC")
                                id = cursor.fetchone()[0]
                                cursor.execute(f"DELETE FROM {m} WHERE id={id}")
                    after = None
                    dbconn.commit()
                    cursor.close()
                    dbconn.close()

                # list all playlists
                elif m.lower().startswith('list'):
                    dbconn = psycopg2.connect("dbname=DPL")
                    cursor = dbconn.cursor()
                    if len(m) > 5:
                        cursor.execute(f"SELECT * FROM playlists WHERE name={m[6:]}")
                    if len(m) <= 5 or not cursor.fetchall():
                        m = "Playlists"
                        l = '```nim\n'
                        cursor.execute("SELECT name FROM playlists")
                        page = 0
                        embeds = []
                        for name in cursor.fetchall():
                            if page==10:
                                embeds.append(l+'```')
                                page = 0
                                l = '```nim\n'
                            l += f"{str(len(embeds)*10 + page + 1)}) {name[0]}\n"
                            page += 1
                        l += '```'

                    # Show particular pl
                    else:
                        m = m[5:]
                        dbconn = psycopg2.connect("dbname=DPL")
                        cursor = dbconn.cursor()
                        cursor.execute(f"SELECT title, url, uid FROM {m}")
                        embeds = []
                        page = 0
                        l = ''
                        for title, link, user in cursor.fetchall():
                            if page==10:
                                embeds.append(l)
                                l = ''
                                page = 0
                            l += f"{str(len(embeds)*10 + page + 1)}) [{title}]({link})  - [<@!{user}>]\n"
                            page += 1
                    if l:
                        embeds.append(l)
                    cursor.close()
                    dbconn.close()
                    page = 0
                    embed = discord.Embed(title=f'{m}:', color=ctx.author.color, description=embeds[page])
                    embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                    pl = await ctx.channel.send(embed=embed)
                    await pl.add_reaction('⏪')
                    await pl.add_reaction('◀️')
                    await pl.add_reaction('▶️')
                    await pl.add_reaction('⏩')

                # play PL
                elif m.lower().startswith(tuple(botl.keys())):
                    if not ctx.author.voice:
                        await ctx.channel.send("Bruh join a voice channel lol")
                    else:
                        m = m.split()
                        pf = m[0]
                        m = ' '.join(m[1:])
                        dbconn = psycopg2.connect("dbname=DPL")
                        cursor = dbconn.cursor()
                        cursor.execute(f"SELECT url FROM {m}")
                        await ctx.channel.send('Queuing playlist '+ m)
                        vc = await ctx.author.voice.channel.connect()
                        for s in cursor.fetchall():
                            await ctx.channel.send(f'{botl[pf]}p {s[0]}', delete_after=1)
                        await ctx.channel.send(f'{botl[pf]}q', delete_after=1)
                        await vc.disconnect()
                        cursor.close()
                        dbconn.close()

                # rename PL
                elif m.lower().startswith('rename'):
                    old, new = m.split()[1:]
                    dbconn = psycopg2.connect("dbname=DPL")
                    cursor = dbconn.cursor()
                    cursor.execute(f"ALTER TABLE {old} RENAME TO {new}")
                    cursor.execute(f"UPDATE playlists SET name='{new}' WHERE name='{old}'")
                    dbconn.commit()
                    cursor.close()
                    dbconn.close()
                    await ctx.add_reaction('👌️')

                # delete PL
                elif m.lower().startswith('drop'):
                    tata = m[5:]
                    dbconn = psycopg2.connect("dbname=DPL")
                    cursor = dbconn.cursor()
                    cursor.execute(f"DROP TABLE {tata}")
                    cursor.execute(f"DELETE FROM playlists WHERE name='{tata}'")
                    dbconn.commit()
                    cursor.close()
                    dbconn.close()
                    await ctx.add_reaction('👌️')

                # trim PL
                elif m.lower().startswith('trim'):
                    m = m[5:].split()
                    a = map(int, m[1:])
                    m= m[0]
                    dbconn = psycopg2.connect("dbname=DPL")
                    cursor = dbconn.cursor()
                    cursor.execute(f"SELECT id, title, url, uid FROM {m}")
                    embeds = []
                    page = 0
                    l = ''
                    id = 1
                    rows = cursor.fetchall()
                    for _, title, link, user in rows:
                        if page==10:
                            embeds.append(l)
                            l = ''
                            page = 0
                        if id in a:
                            cursor.execute(f"DELETE FROM {m} WHERE id={_}")
                        else:
                            l += f"{str(len(embeds)*10 + page + 1)}) [{title}]({link})  - [<@!{user}>]\n"
                            page += 1
                        id += 1
                    if l:
                        embeds.append(l)
                    cursor.close()
                    dbconn.close()
                    page = 0
                    embed = discord.Embed(title=f'{m} (Updated):', color=ctx.author.color, description=embeds[page])
                    embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                    pl = await ctx.channel.send(embed=embed)
                    await pl.add_reaction('⏪')
                    await pl.add_reaction('◀️')
                    await pl.add_reaction('▶️')
                    await pl.add_reaction('⏩')

# This class is used to interact with the Discord WebSocket and API.
client = myClient()
# Bot login using the token
token = base64.b64decode('T0RBNE1EY3hOekF4T0RreE5URTBORFE0LllNTjdmdy55eWdJU0RELVlES3AwczU2SDZGOWFTTy0yNWs=').decode('utf-8')
client.run(token, bot=False)
