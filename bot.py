import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.emojis import e, load_application_emojis

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Prefix mặc định cho toàn bộ thành viên
PREFIX = "?"

# Discord User ID của Owner Bot
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# Nếu muốn slash command đồng bộ tức thì (chỉ cho 1 server) trong lúc test,
# điền GUILD_ID vào file .env. Để trống thì sync toàn cục (mất tới 1h để cập nhật).
GUILD_ID = os.getenv("GUILD_ID")


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# =========================================================
# PREFIX
# =========================================================

async def get_prefix(bot, message):
    """
    Prefix:
    - Thành viên bình thường: ?
    - Owner bot: ? hoặc .
    """

    # Tin nhắn không có author thì dùng prefix mặc định
    if not message.author:
        return "?"

    # Owner được sử dụng cả ? và .
    if message.author.id == OWNER_ID:
        return commands.when_mentioned_or("?", ".")(bot, message)

    # Người dùng bình thường chỉ được dùng ?
    return commands.when_mentioned_or("?")(bot, message)


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=commands.DefaultHelpCommand()
)


COGS = [
    "cogs.moderation",
    "cogs.anti_raid",
    "cogs.anti_link",
    "cogs.setup",
    "cogs.economy",
    "cogs.ping",
    "cogs.chat_bridge",
    "cogs.global_admin",
    "cogs.info",
    "cogs.events"
]


_synced_once = False
_emojis_loaded = False


async def load_cogs():
    for cog in COGS:
        await bot.load_extension(cog)
        print(f"{e('success')} Đã load extension: {cog}")


@bot.listen("on_ready")
async def on_ready_setup():
    global _synced_once, _emojis_loaded

    # 0. Ghi lại thời điểm bot khởi động
    if not hasattr(bot, "start_time"):
        bot.start_time = discord.utils.utcnow()

    # 1. Tự động lấy emoji đã set trong Developer Portal
    if not _emojis_loaded:
        await load_application_emojis(bot)
        _emojis_loaded = True

    # 2. Đồng bộ slash command
    if not _synced_once:
        try:
            if GUILD_ID:
                guild = discord.Object(id=int(GUILD_ID))
                bot.tree.copy_global_to(guild=guild)

                synced = await bot.tree.sync(guild=guild)

                print(
                    f"{e('success')} Đã sync "
                    f"{len(synced)} slash command cho guild {GUILD_ID}"
                )
            else:
                synced = await bot.tree.sync()

                print(
                    f"{e('success')} Đã sync "
                    f"{len(synced)} slash command toàn cục "
                    f"(có thể mất tới 1h để hiện ra)"
                )

            _synced_once = True

        except Exception as ex:
            print(f"{e('error')} Lỗi khi sync slash command: {ex}")


async def main():
    if not TOKEN:
        print(
            f"{e('error')} Không tìm thấy DISCORD_TOKEN. "
            "Hãy tạo file .env dựa theo .env.example rồi điền token vào."
        )
        return

    if not OWNER_ID:
        print(
            f"{e('error')} Không tìm thấy OWNER_ID trong file .env."
        )
        return

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
