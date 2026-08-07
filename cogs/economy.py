import discord
from discord import app_commands
from discord.ext import commands

from utils.emojis import e
from utils.economy import (
    get_balance, add_balance, transfer, claim_daily, claim_work,
    get_leaderboard, format_seconds,
)

CURRENCY_NAME = "Xu"


def mod_embed(title: str, description: str, color: discord.Color = discord.Color.gold()):
    return discord.Embed(title=title, description=description, color=color)


class Economy(commands.Cog):
    """Hệ thống kinh tế đơn giản: kiếm xu, chuyển xu, xếp hạng."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="balance", aliases=["bal", "xu"], description="Xem số dư xu hiện tại")
    @app_commands.describe(member="Xem số dư của người khác (để trống = xem của bạn)")
    async def balance(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        bal = get_balance(ctx.guild.id, member.id)
        embed = mod_embed(
            f"{e('coin')} Số dư của {member.display_name}",
            f"**{bal:,} {CURRENCY_NAME}**",
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="daily", description="Nhận thưởng hàng ngày")
    async def daily(self, ctx: commands.Context):
        success, amount, remaining = claim_daily(ctx.guild.id, ctx.author.id)
        if success:
            new_bal = get_balance(ctx.guild.id, ctx.author.id)
            embed = mod_embed(
                f"{e('daily')} Đã nhận thưởng hàng ngày",
                f"Bạn nhận được **+{amount:,} {CURRENCY_NAME}**!\nSố dư hiện tại: **{new_bal:,} {CURRENCY_NAME}**",
                discord.Color.green(),
            )
        else:
            embed = mod_embed(
                f"{e('error')} Chưa thể nhận",
                f"Bạn cần đợi thêm **{format_seconds(remaining)}** nữa mới nhận được thưởng hàng ngày tiếp theo.",
                discord.Color.red(),
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="work", description="Đi làm kiếm xu (cooldown 1 tiếng)")
    async def work(self, ctx: commands.Context):
        success, amount, remaining = claim_work(ctx.guild.id, ctx.author.id)
        if success:
            new_bal = get_balance(ctx.guild.id, ctx.author.id)
            embed = mod_embed(
                f"{e('work')} Đi làm xong!",
                f"Bạn kiếm được **+{amount:,} {CURRENCY_NAME}**.\nSố dư hiện tại: **{new_bal:,} {CURRENCY_NAME}**",
                discord.Color.green(),
            )
        else:
            embed = mod_embed(
                f"{e('error')} Đang mệt, chưa đi làm tiếp được",
                f"Cần đợi thêm **{format_seconds(remaining)}** nữa mới đi làm lại được.",
                discord.Color.red(),
            )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="pay", aliases=["transfer"], description="Chuyển xu cho thành viên khác")
    @app_commands.describe(member="Người nhận", amount="Số xu muốn chuyển")
    async def pay(self, ctx: commands.Context, member: discord.Member, amount: app_commands.Range[int, 1]):
        if member.id == ctx.author.id:
            embed = mod_embed(f"{e('error')} Không hợp lệ", "Không thể tự chuyển xu cho chính mình.", discord.Color.red())
            return await ctx.send(embed=embed, ephemeral=True)
        if member.bot:
            embed = mod_embed(f"{e('error')} Không hợp lệ", "Không thể chuyển xu cho bot.", discord.Color.red())
            return await ctx.send(embed=embed, ephemeral=True)

        success, msg = transfer(ctx.guild.id, ctx.author.id, member.id, amount)
        if not success:
            embed = mod_embed(f"{e('error')} Chuyển thất bại", msg, discord.Color.red())
            return await ctx.send(embed=embed, ephemeral=True)

        embed = mod_embed(
            f"{e('pay')} Chuyển xu thành công",
            f"{ctx.author.mention} đã chuyển **{amount:,} {CURRENCY_NAME}** cho {member.mention}.",
            discord.Color.green(),
        )
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="leaderboard", aliases=["lb", "top"], description="Bảng xếp hạng giàu nhất server")
    async def leaderboard(self, ctx: commands.Context):
        top = get_leaderboard(ctx.guild.id, limit=10)
        if not top:
            embed = mod_embed(f"{e('info')} Chưa có dữ liệu", "Chưa ai có xu trong server này cả.", discord.Color.blurple())
            return await ctx.send(embed=embed)

        medals = ["🥇", "🥈", "🥉"]
        lines = []
        for i, (user_id, bal) in enumerate(top):
            prefix = medals[i] if i < 3 else f"**#{i+1}**"
            lines.append(f"{prefix} <@{user_id}> — {bal:,} {CURRENCY_NAME}")

        embed = mod_embed(f"{e('leaderboard')} Bảng xếp hạng {CURRENCY_NAME}", "\n".join(lines), discord.Color.gold())
        await ctx.send(embed=embed)

    # -----------------------------------------------------------------
    # Lệnh admin: chỉnh số dư thủ công (sửa lỗi, event, phạt...)
    # -----------------------------------------------------------------
    @commands.hybrid_command(name="addmoney", description="[Admin] Cộng xu cho thành viên")
    @app_commands.describe(member="Thành viên", amount="Số xu muốn cộng")
    @commands.has_permissions(administrator=True)
    async def addmoney(self, ctx: commands.Context, member: discord.Member, amount: app_commands.Range[int, 1]):
        new_bal = add_balance(ctx.guild.id, member.id, amount)
        embed = mod_embed(f"{e('success')} Đã cộng xu", f"Đã cộng **{amount:,} {CURRENCY_NAME}** cho {member.mention}.\nSố dư mới: **{new_bal:,}**", discord.Color.green())
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="removemoney", description="[Admin] Trừ xu của thành viên")
    @app_commands.describe(member="Thành viên", amount="Số xu muốn trừ")
    @commands.has_permissions(administrator=True)
    async def removemoney(self, ctx: commands.Context, member: discord.Member, amount: app_commands.Range[int, 1]):
        new_bal = add_balance(ctx.guild.id, member.id, -amount)
        embed = mod_embed(f"{e('success')} Đã trừ xu", f"Đã trừ **{amount:,} {CURRENCY_NAME}** của {member.mention}.\nSố dư mới: **{new_bal:,}**", discord.Color.orange())
        await ctx.send(embed=embed)

    @addmoney.error
    @removemoney.error
    async def economy_admin_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            embed = mod_embed(f"{e('error')} Không đủ quyền", "Lệnh này cần quyền Administrator.", discord.Color.red())
        else:
            embed = mod_embed(f"{e('error')} Lỗi", f"```{error}```", discord.Color.red())
        await ctx.send(embed=embed, ephemeral=True if ctx.interaction else False)


async def setup(bot: commands.Bot):
    await bot.add_cog(Economy(bot))
  
