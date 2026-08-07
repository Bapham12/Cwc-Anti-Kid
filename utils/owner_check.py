"""
Check quyền owner dùng chung cho mọi lệnh cấp cao (global ban, global announce,
quản lý kênh hàng loạt, bộ lọc cầu nối chat...).

Khoá cứng theo 1 UID cụ thể lấy từ biến môi trường BOT_OWNER_ID (đặt qua .env hoặc
GitHub Secrets), KHÔNG dùng commands.is_owner() mặc định của discord.py.

Lý do: commands.is_owner() xác định owner dựa trên application đang chạy (ai sở hữu
bot token đó trong Developer Portal). Nếu ai đó clone repo này về và tự chạy bằng
token bot riêng của họ, họ sẽ tự động là "owner" theo cách đó. hard_owner_check()
luôn so khớp với đúng UID đã set trong BOT_OWNER_ID, nên dù ai clone repo và deploy
ở đâu (Termux, Codespaces, Windows...), các lệnh cấp cao này vẫn chỉ 1 người dùng
được, trừ khi họ tự đổi UID trong .env của họ.
"""

import os
from discord.ext import commands


def hard_owner_check():
    async def predicate(ctx: commands.Context) -> bool:
        owner_id_env = os.getenv("BOT_OWNER_ID", "").strip()
        if not owner_id_env:
            # Chưa set BOT_OWNER_ID -> để an toàn, không ai dùng được cho tới khi cấu hình
            return False
        try:
            return ctx.author.id == int(owner_id_env)
        except ValueError:
            return False
    return commands.check(predicate)
  
