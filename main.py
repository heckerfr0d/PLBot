#!/usr/bin/python3
import discord
import base64
import re
from datetime import datetime
import psycopg2

music = None
after = None
pl = None
page = None
embed = None
embeds = None

class myClient(discord.Client):

  # Coroutine to login
    async def on_ready(self):
        print(f'Logged in as {client.user}'.format(client))
        # dbconn = psycopg2.connect("dbname=DPL")
        # cursor = dbconn.cursor()
        # m = "Kammattipadam"
        # # cursor.execute(f"DELETE FROM playlists WHERE name='{m}'")
        # # cursor.execute(f"INSERT INTO playlists (name) VALUES ('{m}')")
        # # cursor.execute(f"DROP TABLE IF EXISTS {m}")
        # # cursor.execute(f"CREATE TABLE {m} (id serial primary key, title text not NULL, url text, uid text)")
        # # kp = {"651060433972756492" : "Annen", "757506147606593547" : "Cellu", "578439959678025729" : "Heri", "724357207533027358" : "Jawad", "611501944649023498" : "Hedif", "755712019549782080" : "JFK", "757502893786923088" : "Meden", "758333159674085386" : "Shehz", "757502277434212362" : "Shen"}
        # # for v in kp.values():
        # #     cursor.execute(f"DELETE FROM playlists WHERE name='{v}'")
        # #     cursor.execute(f"INSERT INTO playlists (name) VALUES ('{v}')")
        # #     cursor.execute(f"DROP TABLE IF EXISTS {v}")
        # #     cursor.execute(f"CREATE TABLE {v} (id serial primary key, title text not NULL, url text, uid text)")
        # before = datetime(2021, 4, 3)
        # groovy = await client.fetch_user(234395307759108106)
        # chatH = []
        # yesterday = datetime(2019, 1, 1).strftime("%d_%m_%Y")
        # async for msg in client.get_channel(756746075758657572).history(limit=None, before=before, oldest_first=True):
        #     if msg.author==groovy and msg.embeds and msg.embeds[0].description:
        #         chatH.append(msg)
        # botsH = []
        # async for msg in client.get_channel(760829747168673804).history(limit=None, before=before, oldest_first=True):
        #     if msg.author==groovy and msg.embeds and msg.embeds[0].description:
        #         botsH.append(msg)
        # while chatH and botsH:
        #     if chatH[0].created_at < botsH[0].created_at:
        #         msg = chatH.pop(0)
        #     else:
        #         msg = botsH.pop(0)
        #     if msg.embeds and msg.embeds[0].description:
        #         if msg.embeds[0].description.startswith("Queued"):
        #             q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
        #             if q:
        #                 today = msg.created_at.strftime("%d_%m_%Y")
        #                 if today != yesterday:
        #                     cursor.execute(f"INSERT INTO playlists (name) VALUES ('{m}_{today}')")
        #                     cursor.execute(f"CREATE TABLE {m}_{today} (id serial primary key, title text not NULL, url text, uid text)")
        #                     print(yesterday, "done :)")
        #                     yesterday = today
        #                 title, url, uid = q[0]
        #                 title = title.replace("'", "")
        #                 cursor.execute(f"INSERT INTO {m}_{today} (title, url, uid) VALUES ('{title}', '{url}', '{uid}')")
        # print("main done")
        # for msg in chatH:
        #     if msg.embeds and msg.embeds[0].description:
        #         if msg.embeds[0].description.startswith("Queued"):
        #             q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
        #             if q:
        #                 today = msg.created_at.strftime("%d_%m_%Y")
        #                 if today != yesterday:
        #                     cursor.execute(f"INSERT INTO playlists (name) VALUES ('{m}_{today}')")
        #                     cursor.execute(f"CREATE TABLE {m}_{today} (id serial primary key, title text not NULL, url text, uid text)")
        #                     print(yesterday, "done :)")
        #                     yesterday = today
        #                 title, url, uid = q[0]
        #                 title = title.replace("'", "")
        #                 cursor.execute(f"INSERT INTO {m}_{today} (title, url, uid) VALUES ('{title}', '{url}', '{uid}')")
        #         # elif msg.embeds[0].description.startswith("Removed"):
        #         #     q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
        #         #     if q:
        #         #         title, url, uid = q[0]
        #         #         cursor.execute(f"DELETE FROM {m} WHERE url='{url}'")
        # print("chatH done")
        # for msg in botsH:
        #     if msg.embeds and msg.embeds[0].description:
        #         if msg.embeds[0].description.startswith("Queued"):
        #             q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
        #             if q:
        #                 today = msg.created_at.strftime("%d_%m_%Y")
        #                 if today != yesterday:
        #                     cursor.execute(f"INSERT INTO playlists (name) VALUES ('{m}_{today}')")
        #                     cursor.execute(f"CREATE TABLE {m}_{today} (id serial primary key, title text not NULL, url text, uid text)")
        #                     print(yesterday, "done :)")
        #                     yesterday = today
        #                 title, url, uid = q[0]
        #                 title = title.replace("'", "")
        #                 cursor.execute(f"INSERT INTO {m}_{today} (title, url, uid) VALUES ('{title}', '{url}', '{uid}')")
        #         # elif msg.embeds[0].description.startswith("Removed"):
        #         #     q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
        #         #     if q:
        #         #         title, url, uid = q[0]
        #         #         cursor.execute(f"DELETE FROM {m} WHERE url='{url}'")
        # print("botsh done")

        # dbconn.commit()
        # print(f"{m} done :)")
        # cursor.close()
        # dbconn.close()


    async def on_raw_reaction_add(self, payload):
        global pl, page, embed, embeds
        if embeds and pl and payload.message_id==pl.id and payload.user_id!=client.user.id:
            if payload.emoji.name == '⏪' and page > 0:
                page = 0
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '◀️' and page > 0:
                page -= 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '▶️' and page < len(embeds) -1:
                page += 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '⏩' and page < len(embeds) -1:
                page = len(embeds)-1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)

    async def on_raw_reaction_remove(self, payload):
        global pl, page, embed, embeds
        if embeds and pl and payload.message_id==pl.id:
            if payload.emoji.name == '⏪' and page > 0:
                page = 0
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '◀️' and page > 0:
                page -= 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '▶️' and page < len(embeds) -1:
                page += 1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)
            if payload.emoji.name == '⏩' and page < len(embeds) -1:
                page = len(embeds)-1
                embed.description = embeds[page]
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                await pl.edit(embed=embed)


  # Coroutine to answer messages
    async def on_message(self, ctx):
        global music, after, pl, page, embeds, embed
        botl = {'groovy': '-', 'rythm': '!', 'rythm2': '>'}

        # auth :p
        if ctx.author==client.user:
            return
        else:
            m = (await ctx.channel.history(limit=1).flatten())[0].content[1:]
            # start listening
            if m.lower().startswith('startl'):
                music = ctx.channel
                await ctx.add_reaction('😌️')
                after = datetime.now()

            # save playlist
            elif m.lower().startswith('savepl'):
                m = m[7:]
                await ctx.channel.send('-q', delete_after=1)
                await ctx.channel.send(f'Saving this queue as playlist `{m}`')
                dbconn = psycopg2.connect("dbname=DPL")
                cursor = dbconn.cursor()
                cursor.execute(f"DELETE FROM playlists WHERE Name='{m}'")
                cursor.execute(f"INSERT INTO playlists (Name) VALUES ('{m}')")
                cursor.execute(f"DROP TABLE IF EXISTS {m}")
                cursor.execute(f"CREATE TABLE {m} (id serial primary key, title text not NULL, url text, uid text)")
                async for msg in music.history(after=after):
                    if msg.embeds and msg.embeds[0].description:
                        if msg.embeds[0].description.startswith("Queued"):
                            q = re.findall("\[(.*)\]\((.*)\).*(\d{18})", msg.embeds[0].description)
                            if q:
                                song, link, id = q[0]
                                cursor.execute(f"INSERT INTO {m} (title, url, uid) VALUES ('{song}', '{link}', '{id}')")
                        elif msg.embeds[0].description.startswith("Removed"):
                            song, link = re.findall("\[(.*)\]\((.*)\)", msg.embeds[0].description)[0]
                            cursor.execute(f"DELETE FROM {m} WHERE url='{link}'")
                after = None
                music = None
                dbconn.commit()
                cursor.close()
                dbconn.close()

            # list all playlists
            elif m.lower().startswith('listpls'):
                l = '```nim\n'
                dbconn = psycopg2.connect("dbname=DPL")
                cursor = dbconn.cursor()
                cursor.execute("SELECT Name from playlists")
                page = 0
                embeds = []
                for name in cursor.fetchall():
                    if page==10:
                        embeds.append(l+'```')
                        page = 0
                        l = '```nim\n'
                    l += f"{str(page+1)}) {name[0]}\n"
                    page += 1
                l += '```'
                cursor.close()
                dbconn.close()
                if l:
                    embeds.append(l)
                page = 0
                embed = discord.Embed(title='Playlists:', color=ctx.author.color, description=embeds[page])
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                pl = await ctx.channel.send(embed=embed)
                await pl.add_reaction('⏪')
                await pl.add_reaction('◀️')
                await pl.add_reaction('▶️')
                await pl.add_reaction('⏩')
                try:
                    msg = await client.wait_for('message', timeout= 60.0)
                    pl = None
                    embed = None
                    embeds = None
                    page = None
                except:
                    pl = None
                    embed = None
                    embeds = None
                    page = None

            # Show particular pl
            elif m.lower().startswith('showpl'):
                m = m[7:]
                dbconn = psycopg2.connect("dbname=DPL")
                cursor = dbconn.cursor()
                cursor.execute(f"SELECT title, url, uid from {m}")
                embeds = []
                page = 0
                l = ''
                id = 1
                for title, link, user in cursor.fetchall():
                    if page==10:
                        embeds.append(l)
                        l = ''
                        page = 0
                    l += f"{str(id)}) [{title}]({link})  - [<@!{user}>]\n"
                    page += 1
                    id += 1
                cursor.close()
                dbconn.close()
                if l:
                    embeds.append(l)
                page = 0
                embed = discord.Embed(title=f'{m}:', color=ctx.author.color, description=embeds[page])
                embed.set_footer(text=f'Page {page+1} of {len(embeds)}')
                pl = await ctx.channel.send(embed=embed)
                await pl.add_reaction('⏪')
                await pl.add_reaction('◀️')
                await pl.add_reaction('▶️')
                await pl.add_reaction('⏩')
                try:
                    msg = await client.wait_for('message', timeout= 60.0)
                    pl = None
                    embed = None
                    embeds = None
                    page = None
                except:
                    pl = None
                    embed = None
                    embeds = None
                    page = None



            # play PL
            elif m.lower().startswith(tuple(botl.keys())):
                m = m.split()
                pf = m[0]
                m = ' '.join(m[1:])
                dbconn = psycopg2.connect("dbname=DPL")
                cursor = dbconn.cursor()
                cursor.execute(f"SELECT url FROM {m}")
                music = ctx.channel
                await ctx.channel.send('Queuing playlist '+ m)
                for s in cursor.fetchall():
                    await ctx.channel.send(f'{botl[pf]}p {s[0]}', delete_after=0.5)
                await ctx.channel.send(f'{botl[pf]}q', delete_after=1)
                cursor.close()
                dbconn.close()


# This class is used to interact with the Discord WebSocket and API.
client = myClient()
# Bot login using the token
token = base64.b64decode('T0RBNE1EY3hOekF4T0RreE5URTBORFE0LllNTjdmdy55eWdJU0RELVlES3AwczU2SDZGOWFTTy0yNWs=').decode('utf-8')
client.run(token, bot=False)
