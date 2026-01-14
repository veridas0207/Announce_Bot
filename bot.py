import discord
from discord import app_commands
import io
import csv
from config import (
    DISCORD_BOT_TOKEN,
    GUILD_ID,
    ADMIN_ROLE_NAME,
    ALLOWED_ANNOUNCE_CHANNELS_IDS
)

# =========================
# Bot Client
# =========================

class AnnounceBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        try:
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print("Guild commands synced")
        except discord.Forbidden:
            print(f"Guild sync failed for GUILD_ID: {GUILD_ID}, fallback to global sync")
            await self.tree.sync()


    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = AnnounceBot()

# =========================
# Permission Check
# =========================

def is_admin():
    async def predicate(interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            return True

        if ADMIN_ROLE_NAME:
            # Convert role names to lowercase for case-insensitive comparison
            role = discord.utils.get(interaction.guild.roles, name__iexact=ADMIN_ROLE_NAME)
            if role and role in interaction.user.roles:
                return True

        await interaction.response.send_message(
            f"您沒有權限使用此指令（需要管理員或 `{ADMIN_ROLE_NAME}` 角色）。",
            ephemeral=True
        )
        return False

    return app_commands.check(predicate)

# =========================
# Announcement Modal
# =========================

class AnnouncementModal(discord.ui.Modal, title="📢 發布新公告"):
    content = discord.ui.TextInput(
        label="公告內容",
        style=discord.TextStyle.paragraph,
        placeholder="請輸入公告內容（支援多行）",
        required=True,
        max_length=1800
    )

    def __init__(self, channel: discord.TextChannel, mention_everyone: bool):
        super().__init__()
        self.channel = channel
        self.mention_everyone = mention_everyone

    async def on_submit(self, interaction: discord.Interaction):
        # Channel whitelist check
        if (
            ALLOWED_ANNOUNCE_CHANNELS_IDS
            and self.channel.id not in ALLOWED_ANNOUNCE_CHANNELS_IDS
        ):
            await interaction.response.send_message(
                f"❌ 不允許在 {self.channel.mention} 發布公告。",
                ephemeral=True
            )
            return

        # @everyone
        if self.mention_everyone:
            await self.channel.send(
                "@everyone",
                allowed_mentions=discord.AllowedMentions(everyone=True)
            )

        embed = discord.Embed(
            title="✨ 新公告 ✨",
            description=self.content.value,
            color=discord.Color.blue()
        )
        embed.set_footer(
            text=f"由 {interaction.user.display_name} 發布",
            icon_url=interaction.user.avatar.url
            if interaction.user.avatar
            else interaction.user.default_avatar.url
        )
        embed.timestamp = interaction.created_at

        await self.channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ 公告已發布至 {self.channel.mention}",
            ephemeral=True
        )

# =========================
# Slash Commands
# =========================

@bot.tree.command(
    name="announce",
    description="使用彈出式表單發布公告"
)
@app_commands.describe(
    channel="要發布公告的頻道",
    mention_everyone="是否 @everyone"
)
@is_admin()
async def announce(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    mention_everyone: bool = False
):
    modal = AnnouncementModal(channel, mention_everyone)
    await interaction.response.send_modal(modal)


@bot.tree.command(
    name="members",
    description="匯出伺服器成員與身分組 CSV",
    guild=discord.Object(id=GUILD_ID)
)
@is_admin()
async def members(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Member Name", "Roles"])

    for member in interaction.guild.members:
        roles = [r.name for r in member.roles if r.name != "@everyone"]
        writer.writerow([member.display_name, "; ".join(roles)])

    output.seek(0)
    file = discord.File(fp=output, filename="members_export.csv")

    await interaction.followup.send(
        "📄 成員列表 CSV：",
        file=file,
        ephemeral=True
    )


@bot.tree.command(
    name="help",
    description="顯示指令說明",
    guild=discord.Object(id=GUILD_ID)
)
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Announce Bot 指令",
        color=discord.Color.green()
    )

    embed.add_field(
        name="/announce",
        value="以彈出式表單發布公告（管理員限定）",
        inline=False
    )
    embed.add_field(
        name="/members",
        value="匯出成員與角色 CSV（管理員限定）",
        inline=False
    )
    embed.add_field(
        name="/help",
        value="顯示此說明",
        inline=False
    )

    await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================
# Run Bot
# =========================

if __name__ == "__main__":
    if not DISCORD_BOT_TOKEN:
        print("❌ DISCORD_BOT_TOKEN 未設定")
    elif not GUILD_ID:
        print("❌ GUILD_ID 未設定")
    else:
        # GUILD_ID validation is now handled in config.py
        bot.run(DISCORD_BOT_TOKEN)
