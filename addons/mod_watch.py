import discord
import json
from discord.ext import commands
from sys import argv

class Modwatch:
    """
    User watch management commands.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True)
    async def watch(self, ctx, user):
        member = ctx.message.mentions[0]
        self.bot.watching[member.id] = "{}#{}".format(member.name, member.discriminator)
        with open("watch.json", "w") as f:
            json.dump(self.bot.watching, f)
        await self.bot.say("{} is being watched.".format(member.mention))
        await self.bot.send_message(self.bot.modlogs_channel, "👀 **Watch**: {} put {} on watch | {}#{}".format(ctx.message.author.mention, member.mention, member.name, member.discriminator))

    @commands.has_permissions(manage_nicknames=True)
    @commands.command(pass_context=True)
    async def unwatch(self, ctx, user):
        member = ctx.message.mentions[0]
        if member.id not in self.bot.watching:
            await self.bot.say("This user was not being watched.")
            return
        self.bot.watching.pop(member.id)
        with open("watch.json", "w") as f:
            json.dump(self.bot.watching, f)
        await self.bot.say("{} is no longer being watched.".format(member.mention))
        await self.bot.send_message(self.bot.modlogs_channel, "❌ **Unwatch**: {} removed {} from watch | {}#{}".format(ctx.message.author.mention, member.mention, member.name, member.discriminator))

def setup(bot):
    bot.add_cog(Modwatch(bot))
