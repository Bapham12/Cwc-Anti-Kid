import asyncio
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.emojis import e, load_application_emojis
from utils.owner_check import get_configured_owner_id

load_dotenv()

TOKEN = (os.getenv("DISCORD_TOKEN") or "").strip()
NORMAL_PREFIX = os.getenv("NORMAL_PREFIX", "!")   # Member & mod dùng tiền tố này
OWNER_PREFIX = os.getenv("OWNER_PREFIX", ".")      # Chỉ chủ bot dùng tiền tố này

# Nếu muốn slash command đồng bộ tức thì (chỉ cho 1 server) trong lúc test,
# điền GUILD_ID vào file .env. Để trống thì sync toàn cục (mất tới 1h để cập nhật).
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True   # Bắt buộc để đọc lệnh prefix (!)
intents.members = True           # Bắt buộc để kick/ban/mute/anti-raid hoạt động đúng

bot = commands.Bot(command_prefix=[NORMAL_PREFIX, OWNER_PREFIX], intents=intents, help_command=commands.DefaultHelpCommand())

from utils.prefix_gate import register_prefix_gate
register_prefix_gate(bot, NORMAL_PREFIX, OWNER_PREFIX)

COGS = ["cogs.moderation", "cogs.anti_raid", "cogs.anti_link", "cogs.setup", "cogs.economy", "cogs.ping", "cogs.chat_bridge", "cogs.global_admin", "cogs.lockall", "cogs.info", "cogs.events"]

_synced_once = False
_emojis_loaded = False


async def load_cogs():
    for cog in COGS:
        await bot.load_extension(cog)
        print(f"{e('success')} Đã load extension: {cog}")


def _check_owner_id():
    """In ra trạng thái BOT_OWNER_ID lúc khởi động, tự soi lỗi mà không cần đoán mù."""
    owner_id = get_configured_owner_id()
    if owner_id is None:
        print(f"{e('error')} BOT_OWNER_ID chưa set hoặc sai định dạng trong .env — toàn bộ lệnh owner-only (globalban, lockall...) sẽ bị KHOÁ cho tới khi sửa đúng.")
    else:
        print(f"{e('success')} BOT_OWNER_ID hợp lệ: {owner_id} — lệnh owner-only chỉ UID này dùng được.")


@bot.listen("on_ready")
async def on_ready_setup():
    global _synced_once, _emojis_loaded

    # 0. Ghi lại thời điểm bot khởi động (dùng cho lệnh !ping hiện uptime)
    if not hasattr(bot, "start_time"):
        bot.start_time = discord.utils.utcnow()

    # 1. Tự động lấy emoji đã set trong Developer Portal (chỉ cần chạy 1 lần)
    if not _emojis_loaded:
        await load_application_emojis(bot)
        _emojis_loaded = True

    # 2. Đồng bộ slash command (chỉ cần chạy 1 lần dù on_ready gọi lại nhiều lần)
    if not _synced_once:
        try:
            if GUILD_ID:
                guild = discord.Object(id=int(GUILD_ID))
                bot.tree.copy_global_to(guild=guild)
                synced = await bot.tree.sync(guild=guild)
                print(f"{e('success')} Đã sync {len(synced)} slash command cho guild {GUILD_ID}")
            else:
                synced = await bot.tree.sync()
                print(f"{e('success')} Đã sync {len(synced)} slash command toàn cục (có thể mất tới 1h để hiện ra)")
            _synced_once = True
        except Exception as ex:
            print(f"{e('error')} Lỗi khi sync slash command: {ex}")


def _has_valid_token_format(token: str) -> bool:
    """Chặn trường hợp để nguyên placeholder/token rỗng trước khi gọi Discord API."""
    if not token:
        return False
    lowered = token.lower()
    return lowered not in {"your_bot_token_here", "token", "discord_token"}


async def main():
    if not _has_valid_token_format(TOKEN):
        print(f"{e('error')} DISCORD_TOKEN chưa set hoặc vẫn là placeholder. Hãy tạo file .env từ .env.example rồi điền token bot thật của riêng bạn.")
        return

    _check_owner_id()

    async with bot:
        await load_cogs()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
    
