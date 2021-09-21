import discord
from discord.ext import commands, tasks
import datetime
import random
from random import randint
import asyncio
import traceback
import aiohttp
from aiohttp import ClientSession
import requests
from discord.ext.commands import command, cooldown
import json
import nekos
import hmtai
from cogs.autonsfw import DanimeAPI
from pygicord import Paginator
from owotext import OwO
import pymongo
#This cog also contains many sfw things :





class vein3(commands.Cog, name="APIs"):
    def __init__(self, Bot):
        self.Bot = Bot
        self.danime_api = DanimeAPI(Bot)


    @commands.Cog.listener()
    async def on_interaction(self, inter):
        if inter.guild.id != 802529391808086066:
            return
        if inter.components[0].components[0].custom_id != "NUTT_BUTTON":
            return
        try:
            url = inter.message.embeds[0].image.url
            tag = inter.message.embeds[0].description.split(":")[-1].strip().replace("||", "")
        except:
            return
        db = self.Bot.db2['AbodeDB']
        collection = db[tag]
        find = collection.find_one({"_id" : url})
        new_nutt = 1
        if not find:
            return

        try:
            count = find['NUTT'] + 1
            collection.update_one({"_id" : url}, {"$set" : {"NUTT" : count}})
            new_nutt = count
        except KeyError:
            collection.update_one({"_id" : url}, {"$set" : {"NUTT" : 1}})


        return await inter.channel.send(delete_after = 5, content = f"You sucessfully :regional_indicator_n: :regional_indicator_u: :regional_indicator_t: :regional_indicator_t: to this image. Total image :regional_indicator_n: :regional_indicator_u: :regional_indicator_t: :regional_indicator_t:'s : {new_nutt}")

        


    @commands.command(description='Echos\' words from clyde')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clyde(self, ctx, *, text):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={text}") as r:
                res = await r.json()
                await cs.close()
                embed = discord.Embed(
                    color=0x529dff

                )
                embed.set_image(url=res['message'])
                embed.set_footer(text=f'Requested by {ctx.author.name}, Source : Nekobot.xyz', icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)
                await ctx.message.delete()

    @commands.command(description='Sends a random year fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yearfact(self, ctx):

        async with aiohttp.ClientSession() as cs:

            async with cs.get(f"http://numbersapi.com/random/year?json") as r:
                data = await r.json()
                await cs.close()

                embed = discord.Embed(
                    title=data['number'], description=data['text'], colour=0x529dff)

                embed.set_footer(text=f"Requested by {ctx.author}, Fact from numbersapi.com", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(description='Sends a random panda fact :heart:')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pandafact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/panda") as r:
                    data = await r.json()
                    await cs.close()

                    embed = discord.Embed(title="Panda fact", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source: Some-random-api", icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)

    @commands.command(description='Sends a random cat fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def catfact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/cat") as r:
                    data = await r.json()
                    await cs.close()

                    embed = discord.Embed(title="Cat fact :D", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command(description='Sends a random doggo fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dogfact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/dog") as r:
                    data = await r.json()
                    await cs.close()
                    embed = discord.Embed(title="Dog fact :D", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)



    @commands.command(description='Sends a random numberfact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def numberfact(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"http://numbersapi.com/random?json") as r:
                data = await r.json()
                await cs.close()
                embed = discord.Embed(
                    title=data['number'], description=data['text'], colour=0x529dff)
                embed.set_footer(text=f"Requested by {ctx.author}, Fact from numbersapi.com", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(description='Advices for you.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def advice(self, ctx):
        r = requests.get("https://api.adviceslip.com/advice").json()
        advice = r["slip"]["advice"]
        embed = discord.Embed(title=advice, colour=0x529dff)
        embed.set_footer(text=f"Requested by {ctx.author}, adviceslip.com", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    @commands.command(description='Give a headpat to someone.', aliases=['pat'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def headpat(self, ctx, user: discord.Member = None):
        r = requests.get("https://some-random-api.ml/animu/pat").json()['link']
        em = discord.Embed(color=0x26fcff)
        if user != None:
            em.description = f"**{ctx.author.name} pats {user.name}, Kawaiii**"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=';)')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx, user: discord.Member = None):
        r = requests.get(
            "https://some-random-api.ml/animu/wink").json()['link']
        em = discord.Embed(color=0x529dff)
        if user != None:
            em.description = f"{ctx.author.name} winked at {user.name}, Kawaiii"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description='Huggggggggggg.....')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, user: discord.Member = None):
        r = requests.get("https://some-random-api.ml/animu/hug").json()['link']
        em = discord.Embed(color=0x26fcff)
        if user != None:
            em.description = f"{ctx.author.name} hugs {user.name}, Kawaiii!!"
        em.set_image(url=r)
        await ctx.send(embed=em)

        
    @commands.guild_only()
    @commands.command(description="Do lewd things....", usage = "dh sex @user", aliases=['handhold'])
    async def sex (self, ctx, user:discord.Member= None):
        url = requests.get(f"{self.Bot.api_url}handhold").json()['url']
        em = discord.Embed(color = 0x529dff)
        if user != None:
            em.description = f" {ctx.author.name} and {user.name} do lewd things >m<"
        em.set_image(url = url)
        await ctx.send(embed = em)

    @commands.command(description='Palm to the face')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facepalm(self, ctx):
        r = requests.get(
            "https://some-random-api.ml/animu/face-palm").json()['link']
        em = discord.Embed(color=0x26fcff)
        em.description = "Palm to the face"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"All bullies shall be punished!")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bully(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/bully"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))
            embed.set_image(url=f"{link}")
            embed.description = f"{user.mention} You bully! Stop hurting {ctx.author.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/cuddle"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} cuddles {user.mention}!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/kiss"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} kissed {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smug(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/smug"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user != None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user == None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"Smug moment heh"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bonk(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/bonk"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} bonked {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kill(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/kill"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} killed {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/slap"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} slaped {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cringe(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/cringe"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{user.mention} Bruh that was cringe asf"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/blush"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"OWO blushy blushy {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/highfive"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

    def hyper_replace(self, text, old: list, new: list):
        msg = str(text)
        for x, y in zip(old, new):
            msg = str(msg).replace(x, y)
        return msg

    @commands.command(aliases=['define'])
    @commands.guild_only()
    async def urban(self, ctx, *, terms):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        embeds = []
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"http://api.urbandictionary.com/v0/define", params={'term': terms}) as r:
                    data = await r.json()
                items = data['list']
                for item in items:
                    embed = discord.Embed()
                    embed.set_author(name= f"Urban Defination of {item['word']} by {item['author']}.")
                    embed.description = self.hyper_replace(
                        str(item['definition']), old=['[', ']'], new=['', ''])
                    embed.add_field(name="Example",
                                    value=self.hyper_replace(str(item['example']), old=['[', ']'], new=['', '']))
                    embed.set_footer(text=f"👍 {item['thumbs_up']:,}  👎 {item['thumbs_down']}")
                    embeds.append(embed)
                paginator = Paginator(pages=embeds, timeout=90.0)
                await paginator.start(ctx)
        except IndexError:
            raise commands.BadArgument(f"Your search terms gave no results.")

    # @commands.command(description=f"Tch weakness")
    # @commands.guild_only()
    # async def lewd(self, ctx, user: discord.Member = None):
    #     embed = discord.Embed(color= random.choice(self.Bot.color_list))
    #     if user != None:
    #       embed.description=f"{user.name} Yu-ouu are very lwedddd!!"
    #     url = await self.lewd_gifs()
    #     embed.set_image(url=f"{url}")

    #     await ctx.send(embed=embed)


    @commands.command(description=f"Gets a random waifu.\nThe categories are SFW and NSFW while the types can be seen through <https://waifu.pics/docs>.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def waifu(self, ctx, category=None, type_=None):

        if category == None and type_ == None:
            url = f"https://api.waifu.pics/sfw/waifu"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)
        if category == "sfw" and type_ != None:
            type_ = type_.lower()
            category = category.lower()
            url = f"https://api.waifu.pics/{category}/{type_}"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)
        if category == "nsfw" and type_ != None:
            type_ = type_.lower()
            category = category.lower()
            if not ctx.channel.is_nsfw():
                await self.notnsfw(ctx=ctx)
                return

            url = f"https://api.waifu.pics/{category}/{type_}"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.danime_api.normal_image_embed(ctx=ctx, link=link)

    @commands.command(description=f"Sends blowjob images ig", aliases=['bj'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blowjob(self, ctx, amount: int = 0) -> None:
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "blowjob", amount)
        
        await self.danime_api.image_embed(ctx, "blowjob")

    @commands.command(description=f"Returns ecchi gifs that won't be nsfw :)")
    @commands.guild_only()
    async def ecchi(self, ctx):
        r = requests.get(f"{self.Bot.api_url}ecchi").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)


    @commands.command(description=f"Sends a cumm picture.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cum(self, ctx, amount:int=0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "cum", amount)
        
        await self.danime_api.image_embed(ctx, "cum")
        
    # @commands.command(description=f"Sends a futanari picture.")
    # @commands.guild_only()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def futanari(self, ctx, amount:int = 0):

    #     if not ctx.channel.is_nsfw():
    #         await self.notnsfw(ctx=ctx)
    #         return
    #     if amount != 0:
    #         return await self.danime_api.send_images(ctx, "", amount)
    #     r = requests.get(f"{self.Bot.api_url}futanari").json()['url']
    #     em = discord.Embed()
    #     em.description = f"Bad image? [Report it]({self.Bot.support})"
    #     em.set_image(url=r)
    #     await ctx.send(embed=em)

    @commands.command(description=f"Sends a femdom picture.", usage = "dh femdom 5")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def femdom(self, ctx, amount: int = 0):
        return await ctx.send("Femdom not available rightnow.")

        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "femdom", amount)
        
        await self.danime_api.image_embed(ctx, "femdom")

    @commands.command(description=f"Sends a yuri picture.", usage="dh yuri 9")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yuri(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "yuri", amount)
        
        await self.danime_api.image_embed(ctx, "yuri")

    @commands.command(description=f"Sends a ass picture.", usage="dh ass 10")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ass(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "ass", amount)
        
        await self.danime_api.image_embed(ctx, "ass")

    @commands.command(description=f"Sends a creampie picture.", usage="dh creampie 5")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def creampie(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "creampie", amount)
        
        await self.danime_api.image_embed(ctx, "creampie")

    @commands.command(description=f"Weird fetish ok!", usage= "dh cuckold 2", aliases=['netorare'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuckold(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "cuckold", amount)
        
        await self.danime_api.image_embed(ctx, "cuckold")

    @commands.command(description=f"5vs1", usage= "dh gangbang 4")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gangbang(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "gangbang", amount)
        
        await self.danime_api.image_embed(ctx, "gangbang")

    @commands.command(description=f"Boobjob, occupation done by boob to earn a living :chad:")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boobjob(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.danime_api.send_images(ctx, "", amount)

        r = requests.get(f"{self.Bot.api_url}boobjob").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Her beautiful face, cheris it!")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ahegao(self, ctx):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "ahegao", amount)
        
        await self.danime_api.image_embed(ctx, "ahegao")

    @commands.command(description=f"Things you shouldn't do in public.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def public(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "public", amount)
        
        await self.danime_api.image_embed(ctx, "public")
    @commands.command(name="1girl")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _1girl(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "1girl", amount)
        
        await self.danime_api.image_embed(ctx, "1girl")

    @commands.command(aliases= ["erofeet"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feet(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "feet", amount)
        
        await self.danime_api.image_embed(ctx, "feet")

    # @commands.command(description=f"Sends a trap picture.")
    # @commands.guild_only()
    # @commands.cooldown(1, 5, commands.BucketType.user)
    # async def trap(self, ctx, amount : int = 0):
    #     if not ctx.channel.is_nsfw():
    #         await self.notnsfw(ctx=ctx)
    #         return
    #     if amount != 0:
    #         return await self.danime_api.send_images(ctx, "", amount)

    #     r = requests.get(f"{self.Bot.api_url}trap").json()['url']
    #     em = discord.Embed()
    #     em.description = f"Bad image? [Report it]({self.Bot.support})"
    #     em.set_image(url=r)
    #     await ctx.send(embed=em)

    @commands.command(description=f"Glasses lady yay!")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glasses(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "glasses", amount)
        
        await self.danime_api.image_embed(ctx, "glasses")


    @commands.command(description=f"Sends a cat pic :kek:")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pussy(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "pussy", amount)
        
        await self.danime_api.image_embed(ctx, "pussy")

    @commands.command(description=f"Sends a NSFW picture where the lead is in a formal uniform.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uniform(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "uniform", amount)
        
        await self.danime_api.image_embed(ctx, "uniform")

    @commands.command(description=f"Thicc")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def thighs(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "thighs", amount)
        
        await self.danime_api.image_embed(ctx, "thighs")

    @commands.command(description=f"Returns anal images and gifs.")
    @commands.guild_only()
    async def anal(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "anal", amount)
        
        await self.danime_api.image_embed(ctx, "anal")




    @commands.command(usage=f"dh nsfw 10 ",
                      description="From a collection of more than 90,000+ images and gifs sends a random one(s).")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nsfw(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "nsfw", amount)
        
        await self.danime_api.image_embed(ctx, "nsfw")


    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def megumin(self, ctx):
        url = f"https://api.waifu.pics/sfw/megumin"
        data = requests.get(f"{url}").json()
        link = data['url']
        await self.danime_api.normal_image_embed(ctx=ctx, link=link)

    @commands.command(aliases=['tits' , 'boobs'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def oppai(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "oppai", amount)
        
        await self.danime_api.image_embed(ctx, "oppai")

    @commands.command(description="Kemo = animal ears")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kemo(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            return await self.danime_api.not_nsfw(ctx)

        if amount != 0:
            return await self.danime_api.send_images(ctx, "kemo", amount)
        
        await self.danime_api.image_embed(ctx, "kemo")


    @commands.command(description="Sends a SFW anime wallpaper.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wallpaper(self, ctx):
        url = "https://memes.blademaker.tv/api/animewallpaper"
        data = requests.get(f"{url}").json()
        if data["nsfw"] == False:
            link = (data['image'])
            await self.danime_api.normal_image_embed(ctx=ctx, link=link, dl=link)
        else:
            return await ctx.send("Try re running the command, got nsfw :(")

    @commands.command()
    @commands.guild_only()
    async def owofy(self, ctx, *, YourText):
        text = OwO().translate(YourText)
        await ctx.send(content = text)
    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tickle(self, ctx, user: discord.Member = None):
        url = nekos.img(target="tickle")
        if user is None:

            await self.danime_api.normal_image_embed(ctx=ctx, link=url)

        else:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{url}")
            embed.description = f"{ctx.author.mention} tickles {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def baka(self, ctx, user: discord.Member = None):
        url = nekos.img(target="baka")
        if user is None:

            await ctx.send(f"No you are not a baka {ctx.author.name}.")

        else:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{url}")
            embed.description = f"{user.mention} BAKA!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animefood(self, ctx):
        await self.get_nekobot(ctx=ctx, query="food")

    async def get_nekobot(self, ctx, query):
        url = f"https://nekobot.xyz/api/image?type={query}"
        data = requests.get(f"{url}").json()
        image = data['message']
        embed = discord.Embed(color=random.choice(self.Bot.color_list))

        embed.set_image(url=f"{image}")
        return await ctx.send(embed=embed)

    @commands.command(usage = "dh reddit anime",
        description = "Sends a random picture from the given subreddit, no need to include `r/`.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reddit(self, ctx, subreddit):
            url = f"https://memes.blademaker.tv/api/{subreddit}"
            data = requests.get(f"{url}").json()
            if data["nsfw"] == False:
                link = (data['image'])
                await self.danime_api.normal_image_embed(ctx=ctx, link=link, dl=link)

            else:
                if not ctx.channel.is_nsfw():
                    return await ctx.send("Non nsfw channel bruv")
                link = data['image']
                await self.danime_api.normal_image_embed(ctx=ctx, link=link, dl=link)
                
def setup(Bot):
    Bot.add_cog(vein3(Bot))
    print("APIs cog is working.")
