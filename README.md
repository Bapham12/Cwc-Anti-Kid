# 🛡️ CWC Anti Kid (CWC Moderator - Bridge Chat - Auto protect 24/7)

Bot moderator + anti-raid + economy cho Discord, hỗ trợ **cả prefix `!` lẫn slash command `/`** cùng lúc (không cần viết 2 lần), kèm phản hồi bằng emoji cho từng hành động.

## ✨ Tính năng điều hành cơ bản

| Lệnh | Mô tả | Quyền cần có |
|---|---|---|
| `kick <member> [reason]` | Kick thành viên | Kick Members |
| `ban <member> [delete_days] [reason]` | Ban thành viên | Ban Members |
| `unban <user_id> [reason]` | Gỡ ban | Ban Members |
| `mute <member> [minutes] [reason]` | Timeout thành viên | Moderate Members |
| `unmute <member>` | Gỡ timeout | Moderate Members |
| `warn <member> [reason]` | Cảnh báo + lưu lại | Moderate Members |
| `warnings <member>` | Xem danh sách cảnh báo | Moderate Members |
| `clearwarn <member>` | Xoá hết cảnh báo | Moderate Members |
| `purge <amount>` | Xoá hàng loạt tin nhắn (1-100) | Manage Messages |
| `lock` / `unlock` | Khoá / mở khoá kênh | Manage Channels |
| `slowmode <seconds>` | Bật/tắt slowmode | Manage Channels |

## 🪙 Hệ thống kinh tế (economy, mới ở v2.0)

| Lệnh | Mô tả |
|---|---|
| `balance [member]` | Xem số dư Xu |
| `daily` | Nhận thưởng hàng ngày (100-300 Xu, cooldown 24h) |
| `work` | Đi làm kiếm Xu (50-150 Xu, cooldown 1h) |
| `pay <member> <amount>` | Chuyển Xu cho thành viên khác |
| `leaderboard` | Bảng xếp hạng giàu nhất server |
| `addmoney <member> <amount>` | [Admin] Cộng Xu thủ công | 
| `removemoney <member> <amount>` | [Admin] Trừ Xu thủ công |

Dữ liệu lưu riêng theo từng server trong `data/economy.json`, không ảnh hưởng qua lại giữa các server khác nhau.

## 📡 Lệnh ping (mới ở v2.0)

`ping` — hiện độ trễ websocket, độ trễ round-trip API, và uptime của bot, kèm đánh giá nhanh bằng emoji (✅ tốt / ⚠️ bình thường / ❌ chậm).

## ⚙️ Setup nhanh khu vực riêng cho mod (mới ở v2.0)

| Lệnh | Mô tả | Quyền cần có |
|---|---|---|
| `setup [mod_role] [reset]` | 1 lệnh duy nhất tự tạo category **🛠️ Mod Area** gồm kênh `#mod-logs` + `#mod-announcements`, chỉ mod thấy được | Administrator |
| `modannounce <nội dung>` | Gửi thông báo vào kênh `#mod-announcements` vừa tạo | Manage Messages |

Chạy `setup` xong thì:
- `#mod-logs` **tự động** nhận mọi cảnh báo raid/bot giả dạng (không cần chạy `setmodlog` nữa)
- Nếu server đã có role tên chứa "mod" (VD: Moderator, Mod Team...) bot tự dùng lại, không thì tự tạo role `Moderator` mới
- Chạy lại `setup` không tạo trùng kênh — muốn làm lại từ đầu thì thêm `reset:true`

## 🌉 Cầu nối chat xuyên server (chat bridge, mới ở v2.0)

| Lệnh | Mô tả | Quyền cần có |
|---|---|---|
| `bridgesetup [channel]` | Tự động thiết lập cầu nối — kênh này sẽ nối với kênh cầu nối ở mọi server khác đang dùng bot | Administrator |
| `bridgeoff` | Huỷ cầu nối của server này | Administrator |
| `bridgestatus` | Xem trạng thái + tổng số server trong mạng lưới | Ai cũng xem được |

Sau khi setup, mọi tin nhắn gõ trong kênh đó sẽ **tự động hiện ở kênh cầu nối của các server khác** đã setup, dùng webhook nên hiện đúng tên + avatar người gửi gốc kèm tên server, không cần gõ lệnh gì thêm mỗi lần chat. Ảnh/file đính kèm cũng được relay qua dạng link.

Cần quyền bot **Manage Webhooks** khi mời bot vào server.

Kênh cầu nối có bộ lọc riêng (chặn invite link, từ ngữ không phù hợp) trước khi relay sang server khác — tin nhắn vi phạm sẽ không được gửi đi và bị xoá tại chỗ.

## 🔗 Chống spam link (anti-link, mới ở v2.0)

| Lệnh | Mô tả | Quyền cần có |
|---|---|---|
| `antilink` | Xem trạng thái + cấu hình hiện tại | Administrator |
| `antilink on` / `antilink off` | Bật/tắt anti-link | Administrator |
| `antilink mode <invite_only\|all_links>` | Đổi chế độ chặn | Administrator |
| `antilinkwhitelist add/remove <domain>` | Thêm/xoá domain được phép (dùng khi mode = all_links) | Administrator |
| `antilinkchannel add/remove <#channel>` | Thêm/xoá kênh miễn kiểm tra | Administrator |

2 chế độ:
- **`invite_only`** (mặc định) — chỉ chặn link mời vào server Discord khác, dùng chống việc lôi kéo/quảng cáo server khác trong chat
- **`all_links`** — chặn mọi URL, trừ những domain đã thêm vào whitelist (VD: `youtube.com`, `tenor.com`)

Tin nhắn vi phạm sẽ tự động bị xoá, người gửi nhận 1 cảnh báo (tính chung với hệ thống `warn`/`warnings` sẵn có), và log vào kênh mod-log nếu đã cấu hình qua `setmodlog` hoặc `setup`. Mod (người có quyền Manage Messages) và kênh trong whitelist luôn được miễn kiểm tra.

## 🚨 Tính năng chống raid & bot giả dạng (mới ở v2.0)

| Lệnh | Mô tả | Quyền cần có |
|---|---|---|
| `autodefense` | Xem trạng thái auto-defense hiện tại | Administrator |
| `autodefense on` | **Bật chế độ tự động phòng vệ 24/7** | Administrator |
| `autodefense off` | Tắt auto-defense (chỉ còn cảnh báo, không tự xử lý) | Administrator |
| `setmodlog <#kênh>` | Chọn kênh nhận cảnh báo raid / bot giả dạng | Administrator |
| `trustbot <@bot>` | Thêm bot vào whitelist, bỏ qua kiểm tra fake bot | Administrator |
| `features` | Xem bảng chức năng đầy đủ (embed có ảnh gif) | Ai cũng dùng được |

Khi **auto-defense đang BẬT**, bot tự động phát hiện các dấu hiệu bất thường (bot giả dạng, join ồ ạt bất thường...) và tự xử lý (kick/khoá server), báo vào mod-log. Chi tiết thuật toán phát hiện không công khai để tránh bị lợi dụng né tránh.

Khi **auto-defense đang TẮT**, bot vẫn phát hiện và **cảnh báo qua mod-log** nhưng không tự kick/khoá gì cả — an toàn để bật thử trước.

## 🎭 Emoji tự động lấy từ Developer Portal

Từ v2.0, bạn **không cần copy tay ID emoji gif nữa**. Chỉ cần:
1. Vào https://discord.com/developers/applications → app của bạn → tab **Emoji**
2. Upload emoji gif, đặt **tên trùng** với các key: `success`, `warn`, `error`, `kick`, `ban`, `unban`, `mute`, `unmute`, `purge`, `lock`, `unlock`, `slowmode`, `info`, `loading`, `raid`, `shield`, `fakebot`, `coin`, `daily`, `work`, `pay`, `leaderboard`, `ping`, `pong`, `link`
3. Chạy lại bot — log console sẽ báo `Đã fetch N emoji từ Developer Portal, khớp X key đang dùng`

Mỗi lệnh gọi bằng `!` sẽ được bot **thả reaction emoji** lên tin nhắn (✅ thành công, ❌ lỗi, 👢 kick, 🔨 ban, 🔇 mute...). Gọi bằng `/` thì emoji sẽ nằm trong embed trả về (vì slash command không có tin nhắn gốc để thả reaction).

Muốn đổi emoji nào → sửa trong `utils/emojis.py`, hoặc đơn giản là đổi tên/emoji trong Developer Portal.

## 📁 Cấu trúc

```
mod-bot-v1/
├── bot.py                  # File chạy chính, tự fetch emoji + sync slash command
├── cogs/
│   ├── moderation.py        # Lệnh kick/ban/mute/warn/purge/lock...
│   ├── anti_raid.py         # Chống raid + chống bot giả dạng + autodefense 24/7
│   ├── anti_link.py         # Chống spam link (invite Discord / mọi link trừ whitelist)
│   ├── chat_bridge.py       # Cầu nối chat xuyên server qua webhook
│   ├── setup.py             # Lệnh setup — tự tạo khu vực riêng cho mod
│   ├── economy.py           # Hệ thống kinh tế: balance/daily/work/pay/leaderboard
│   ├── ping.py              # Lệnh ping — kiểm tra độ trễ bot
│   ├── global_admin.py      # Quản trị nội bộ nâng cao (chi tiết xem trong code)
│   ├── info.py               # Lệnh !features — embed giới thiệu chức năng (có ảnh gif)
│   └── events.py            # Sự kiện on_ready, xử lý lỗi chung
├── utils/
│   ├── emojis.py             # Bảng emoji + tự fetch từ Developer Portal
│   ├── storage.py            # Lưu cảnh báo (warn) bằng JSON
│   ├── guild_config.py       # Lưu cấu hình autodefense/mod-log riêng từng server
│   ├── economy.py            # Lưu số dư & cooldown daily/work bằng JSON
│   ├── bridge_data.py        # Lưu danh sách kênh cầu nối chat xuyên server
│   └── global_data.py        # Dữ liệu nội bộ nâng cao (chi tiết xem trong code)
├── data/                    # Tự tạo khi bot chạy lần đầu (warnings.json, guild_config.json, economy.json, global_bans.json, bridge_channels.json)
├── requirements.txt
├── .env.example
└── .gitignore
```

## 🔧 Bước 1: Tạo bot trên Discord Developer Portal

1. Vào https://discord.com/developers/applications → **New Application**
2. Vào tab **Bot** → bấm **Reset Token** để lấy token → lưu lại. Token này phải đặt vào biến `DISCORD_TOKEN` trong `.env`/Secret, **không commit token thật lên repo**.
3. Lấy UID owner: bật Developer Mode trong Discord (User Settings → Advanced), chuột phải tài khoản owner → **Copy User ID**, rồi đặt vào `BOT_OWNER_ID`. Các lệnh nguy hiểm như `.globalban`, `.lockall`, `bridgefilter` chỉ chạy khi UID người gọi khớp đúng biến này.
4. Bật 2 intent bắt buộc trong tab Bot:
   - `MESSAGE CONTENT INTENT`
   - `SERVER MEMBERS INTENT`
5. Vào tab **OAuth2 → URL Generator**:
   - Scopes: `bot`, `applications.commands`
   - Bot Permissions: `Kick Members`, `Ban Members`, `Moderate Members`, `Manage Messages`, `Manage Channels`, `Manage Webhooks` (dùng cho cầu nối chat), `Manage Server` (để auto-lock verification level khi có raid), `Send Messages`, `Read Message History`
   - Copy link → mở link đó để mời bot vào server
6. (Tuỳ chọn) Vào tab **Emoji** để upload sẵn emoji gif cho bot — xem phần "Emoji tự động lấy từ Developer Portal" bên dưới

## 🚀 Bước 2: Chạy bot

### Termux (Android)

```bash
pkg update && pkg install python git -y
cd mod-bot-v1
pip install -r requirements.txt
cp .env.example .env
nano .env    # điền DISCORD_TOKEN và BOT_OWNER_ID rồi Ctrl+X, Y, Enter để lưu
python bot.py
```

### GitHub Codespaces

1. Tạo repo mới trên GitHub, upload toàn bộ thư mục này lên
2. Vào repo → **Settings → Secrets and variables → Codespaces** → thêm secret `DISCORD_TOKEN` với token bot và `BOT_OWNER_ID` với UID owner Discord
3. Mở Codespace, trong terminal chạy:
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```
   Codespaces sẽ tự đưa secret vào biến môi trường, nhưng vì `bot.py` đọc qua `.env` bằng `python-dotenv`, bạn có thể thêm dòng sau vào đầu terminal nếu secret không tự nhận:
   ```bash
   { echo "DISCORD_TOKEN=$DISCORD_TOKEN"; echo "BOT_OWNER_ID=$BOT_OWNER_ID"; } > .env
   python bot.py
   ```
4. Lưu ý: Codespaces free tier không chạy 24/7, bot sẽ tắt khi hết giờ hoặc đóng tab.

### Windows CMD

```cmd
cd mod-bot-v1
pip install -r requirements.txt
copy .env.example .env
notepad .env    # điền DISCORD_TOKEN và BOT_OWNER_ID
python bot.py
```

## 🔐 Cấu hình Token & Owner UID

- `.env.example` chỉ chứa tên biến và giá trị trống/placeholder an toàn. Sau khi fork hoặc clone, hãy copy sang `.env` rồi điền token/UID thật ở máy hoặc trong Secret của môi trường chạy.
- `DISCORD_TOKEN` là token của bot Discord của bạn. Nếu để trống hoặc giữ placeholder, bot sẽ dừng trước khi gọi Discord API.
- `BOT_OWNER_ID` phải là chuỗi số UID Discord thuần của owner. Repo không nên hard-code UID của chủ cũ; mỗi người fork cần đặt UID của mình trong `.env`/Secret.
- `NORMAL_PREFIX` mặc định là `!`, còn `OWNER_PREFIX` mặc định là `.`. Các lệnh owner-only vẫn bị kiểm tra bằng `BOT_OWNER_ID`, không chỉ dựa vào prefix.

## ⚙️ Ghi chú về Slash Command

- Nếu điền `GUILD_ID` trong `.env`, slash command sẽ hiện ra **ngay lập tức** trong server đó (dùng để test).
- Nếu để trống, bot sync toàn cục — có thể mất **tới 1 tiếng** để `/` hiện ra ở mọi server, nhưng dùng được ở mọi nơi bot có mặt.
- Cách lấy Guild ID: Bật Developer Mode trong Discord (Settings → Advanced), chuột phải vào server → Copy Server ID.

## 🗺️ Lộ trình v2.1 (gợi ý)

- Anti-spam / anti-flood tin nhắn (không chỉ join raid)
- Tự động hạ verification level lại sau X phút thay vì phải chỉnh tay
- Lệnh `role add/remove`
- Hệ thống warn tự động ban khi đạt ngưỡng số lần cảnh báo
- Dashboard web xem log raid/fake bot thay vì chỉ xem qua kênh mod-log

---
Bot này dùng chung style với các dự án Anti-Raid / Anti-Nuke Sentinel trước đó — có thể ghép chung vào cùng 1 bot nếu muốn, chỉ cần copy thư mục `cogs/moderation.py` này vào project kia.
