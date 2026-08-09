"""
Check quyền owner dùng chung cho mọi lệnh cấp cao (global ban, global announce,
quản lý kênh hàng loạt, bộ lọc cầu nối chat, lockall...).

Khoá cứng theo 1 UID cụ thể lấy từ biến môi trường BOT_OWNER_ID (đặt qua .env hoặc
GitHub Secrets), KHÔNG dùng commands.is_owner() mặc định của discord.py.

Lý do: commands.is_owner() xác định owner dựa trên application đang chạy (ai sở hữu
bot token đó trong Developer Portal). Nếu ai đó clone repo này về và tự chạy bằng
token bot riêng của họ, họ sẽ tự động là "owner" theo cách đó. hard_owner_check()
luôn so khớp với đúng UID đã set trong BOT_OWNER_ID, nên dù ai clone repo và deploy
ở đâu (Termux, Codespaces, Windows...), các lệnh cấp cao này vẫn chỉ 1 người dùng
được, trừ khi họ tự đổi UID trong .env của họ.

v2: Tự động dọn dấu ngoặc kép/đơn và khoảng trắng thừa quanh giá trị BOT_OWNER_ID.
Lỗi hay gặp nhất là copy-paste UID bị dính dấu ngoặc (VD: BOT_OWNER_ID="123...")
khiến int() parse lỗi -> khoá luôn cả owner thật. Bản này tự dọn sạch trước khi so sánh.
"""

import os
from discord.ext import commands


def _parse_owner_id() -> int | None:
    """Đọc BOT_OWNER_ID từ biến môi trường, tự dọn dấu ngoặc/khoảng trắng/ký tự ẩn thừa."""
    raw = os.getenv("BOT_OWNER_ID", "")
    if not raw:
        return None

    cleaned = raw.strip()

    # Dọn dấu ngoặc kép/đơn thừa nếu lỡ gõ "123..." hoặc '123...'
    if len(cleaned) >= 2 and cleaned[0] in "\"'" and cleaned[-1] in "\"'":
        cleaned = cleaned[1:-1].strip()

    # Discord snowflake chỉ nên là chuỗi số thuần. Không tự nhặt số từ chuỗi lẫn
    # chữ (VD: "abc123") vì dễ che giấu việc cấu hình sai UID.
    if not cleaned.isdigit():
        return None

    try:
        return int(cleaned)
    except ValueError:
        return None


def get_configured_owner_id() -> int | None:
    """Trả về UID owner đã cấu hình (đã dọn sạch), None nếu chưa set hoặc sai định dạng.
    Dùng để bot.py in ra log lúc khởi động, giúp tự kiểm tra BOT_OWNER_ID có đọc đúng không."""
    return _parse_owner_id()


def hard_owner_check():
    """Check RIÊNG cho các lệnh cấp cao — khoá cứng theo đúng UID trong BOT_OWNER_ID."""
    async def predicate(ctx: commands.Context) -> bool:
        owner_id = _parse_owner_id()
        if owner_id is None:
            return False
        return ctx.author.id == owner_id
    return commands.check(predicate)
    
