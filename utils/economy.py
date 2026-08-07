"""
Lưu trữ hệ thống kinh tế (economy) bằng file JSON đơn giản, tách riêng theo từng server.
Không cần setup database ngoài, phù hợp Termux / Codespaces / Windows.
"""

import json
import os
import time
from typing import Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
ECONOMY_FILE = os.path.join(DATA_DIR, "economy.json")

DEFAULT_USER = {
    "balance": 0,
    "last_daily": 0,   # epoch giây
    "last_work": 0,    # epoch giây
}

DAILY_COOLDOWN = 24 * 60 * 60       # 24 giờ
WORK_COOLDOWN = 60 * 60             # 1 giờ

DAILY_RANGE = (100, 300)
WORK_RANGE = (50, 150)


def _ensure_file():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(ECONOMY_FILE):
        with open(ECONOMY_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def _load() -> dict[str, Any]:
    _ensure_file()
    with open(ECONOMY_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save(data: dict[str, Any]):
    _ensure_file()
    with open(ECONOMY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _get_user(data: dict, guild_id: int, user_id: int) -> dict:
    gkey, ukey = str(guild_id), str(user_id)
    data.setdefault(gkey, {})
    data[gkey].setdefault(ukey, dict(DEFAULT_USER))
    return data[gkey][ukey]


def get_balance(guild_id: int, user_id: int) -> int:
    data = _load()
    return _get_user(data, guild_id, user_id)["balance"]


def add_balance(guild_id: int, user_id: int, amount: int) -> int:
    """Cộng xu (có thể âm để trừ), trả về số dư mới. Không cho âm."""
    data = _load()
    user = _get_user(data, guild_id, user_id)
    user["balance"] = max(0, user["balance"] + amount)
    _save(data)
    return user["balance"]


def transfer(guild_id: int, from_id: int, to_id: int, amount: int) -> tuple[bool, str]:
    if amount <= 0:
        return False, "Số xu chuyển phải lớn hơn 0."

    data = _load()
    sender = _get_user(data, guild_id, from_id)
    if sender["balance"] < amount:
        return False, f"Không đủ xu. Số dư hiện tại: {sender['balance']}."

    receiver = _get_user(data, guild_id, to_id)
    sender["balance"] -= amount
    receiver["balance"] += amount
    _save(data)
    return True, "OK"


def claim_daily(guild_id: int, user_id: int) -> tuple[bool, int, int]:
    """
    Trả về (thành_công, số_xu_nhận_được, giây_còn_lại_nếu_chưa_được_claim).
    """
    import random
    data = _load()
    user = _get_user(data, guild_id, user_id)
    now = time.time()
    elapsed = now - user["last_daily"]

    if elapsed < DAILY_COOLDOWN:
        return False, 0, int(DAILY_COOLDOWN - elapsed)

    amount = random.randint(*DAILY_RANGE)
    user["balance"] += amount
    user["last_daily"] = now
    _save(data)
    return True, amount, 0


def claim_work(guild_id: int, user_id: int) -> tuple[bool, int, int]:
    import random
    data = _load()
    user = _get_user(data, guild_id, user_id)
    now = time.time()
    elapsed = now - user["last_work"]

    if elapsed < WORK_COOLDOWN:
        return False, 0, int(WORK_COOLDOWN - elapsed)

    amount = random.randint(*WORK_RANGE)
    user["balance"] += amount
    user["last_work"] = now
    _save(data)
    return True, amount, 0


def get_leaderboard(guild_id: int, limit: int = 10) -> list[tuple[int, int]]:
    """Trả về list [(user_id, balance)], sắp xếp giảm dần theo balance."""
    data = _load()
    gkey = str(guild_id)
    users = data.get(gkey, {})
    ranked = sorted(users.items(), key=lambda kv: kv[1].get("balance", 0), reverse=True)
    return [(int(uid), info.get("balance", 0)) for uid, info in ranked[:limit]]


def format_seconds(seconds: int) -> str:
    """Định dạng số giây thành 'Xh Ym Zs' cho dễ đọc."""
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    parts = []
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}p")
    if s or not parts:
        parts.append(f"{s}s")
    return " ".join(parts)
          
