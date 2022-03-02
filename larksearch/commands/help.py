from discord.ext.commands import Context
from discord.ext.commands import Command


async def help(ctx: Context, *args):
    await ctx.reply('ㅎㅇ')


command = Command(help,
                  name="도움말",
                  aliases=['도움'],
                  usage="!도움말",
                  help="아직 기능이 없습니다.")
