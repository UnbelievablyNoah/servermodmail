import discord
from discord.ext import commands


def is_owner():
    async def predicate(ctx):
        return ctx.author.id in ctx.bot.config.owners
    return commands.check(predicate)


def in_database():
    async def predicate(ctx):
        c = ctx.bot.conn.cursor()
        c.execute("SELECT * FROM data WHERE guild=?", (ctx.guild.id,))
        res = c.fetchone()
        if res is None or res[2] is None or res[3] is None:
            await ctx.send(
                embed=discord.Embed(
                    description=f"Your server is not in the database yet. Use `{ctx.prefix}setup` first.",
                    color=ctx.bot.primary_colour,
                )
            )
        return True if res is not None else False
    return commands.check(predicate)


def is_premium():
    async def predicate(ctx):
        c = ctx.bot.conn.cursor()
        c.execute("SELECT server FROM premium")
        res = c.fetchall()
        all_premium = []
        for row in res:
            if row[0] is None:
                continue
            row = row[0].split(",")
            for guild in row:
                all_premium.append(guild)
        if ctx.guild.id not in all_premium:
            await ctx.send(
                embed=discord.Embed(
                    description="This server does not have premium. Want to get premium? More information "
                                f"is available with the `{ctx.prefix}premium` command.",
                    color=ctx.bot.primary_colour,
                )
            )
            return False
        else:
            return True
    return commands.check(predicate)


def is_patron():
    async def predicate(ctx):
        c = ctx.bot.conn.cursor()
        c.execute("SELECT user FROM premium WHERE user=?", (ctx.author.id,))
        res = c.fetchone()
        if res is None:
            await ctx.send(
                embed=discord.Embed(
                    description="This command requires you to be a patron. Want to become a patron? More information "
                                f"is available with the `{ctx.prefix}premium` command.",
                    color=ctx.bot.primary_colour,
                )
            )
            return False
        else:
            return True
    return commands.check(predicate)


def is_modmail_channel():
    async def predicate(ctx):
        if not ctx.channel.category_id or ctx.channel.category_id not in ctx.bot.all_category or \
           not ctx.channel.name.isdigit():
            await ctx.send(
                embed=discord.Embed(
                    description="This channel is not a ModMail channel.",
                    color=ctx.bot.primary_colour,
                )
            )
            return False
        else:
            return True
    return commands.check(predicate)