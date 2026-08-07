import discord
from discord.ext import commands
from utils.emojis import e


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{e('success')} Đã đăng nhập với tên {self.bot.user} (ID: {self.bot.user.id})")
        print(f"{e('info')} Đang hoạt động ở {len(self.bot.guilds)} server.")
        await self.bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="server | !help hoặc /help")
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        # Lỗi riêng của từng lệnh mod đã được xử lý trong cogs/moderation.py
        # Đây chỉ là fallback cho các lỗi chung / lệnh không tồn tại
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            return  # đã được cog con xử lý
        print(f"[LỖI] {ctx.command}: {error}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
  
