import discord
from discord import app_commands
import io
import csv
from config import DISCORD_BOT_TOKEN, GUILD_ID, ADMIN_ROLE_NAME, ALLOWED_ANNOUNCE_CHANNELS_IDS

class AnnounceBot(discord.Client):
    def __init__(self):
        # Set intents. Message content and members intents are needed.
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True # Required to get member information
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        # We'll sync commands to a specific guild for faster development
        try:
            guild_obj = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild_obj)
            await self.tree.sync(guild=guild_obj)
            print("Commands synced successfully!")
        except ValueError:
            print("Error: GUILD_ID is not a valid integer. Please check your .env file.")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def setup_hook(self):
        # This is where we would typically load cogs if we had them
        pass

bot = AnnounceBot()

# Command to check if the user has the required admin role
def is_admin():
    async def predicate(interaction: discord.Interaction):
        # Check for server administrator permission
        if interaction.user.guild_permissions.administrator:
            return True

        # If not a server administrator, check for the specific ADMIN_ROLE_NAME
        if ADMIN_ROLE_NAME:
            admin_role = discord.utils.get(interaction.guild.roles, name=ADMIN_ROLE_NAME)
            if admin_role and admin_role in interaction.user.roles:
                return True
        
        await interaction.response.send_message(
            f"您沒有權限使用此指令。您需要伺服器管理員權限或 '{ADMIN_ROLE_NAME}' 角色。", 
            ephemeral=True
        )
        return False
    return app_commands.check(predicate)


@bot.tree.command(name="announce", description="發布公告到指定的頻道。", guild=discord.Object(id=int(GUILD_ID)))
@app_commands.describe(
    channel="要發布公告的頻道",
    message="公告的內容",
    mention_everyone="是否在公告中 @everyone (機器人需有權限)"
)
@is_admin()
async def announce(interaction: discord.Interaction, channel: discord.TextChannel, message: str, mention_everyone: bool = False):
    """
    發布公告到指定的頻道。
    """
    try:
        # Check if the channel is allowed for announcements
        if ALLOWED_ANNOUNCE_CHANNELS_IDS and channel.id not in ALLOWED_ANNOUNCE_CHANNELS_IDS:
            await interaction.response.send_message(
                f"您不能在這個頻道 ({channel.mention}) 發布公告。請選擇允許的頻道。",
                ephemeral=True
            )
            return

        # Send @everyone mention if requested
        if mention_everyone:
            # Send as a separate message to ensure it triggers the mention notification
            await channel.send("@everyone", allowed_mentions=discord.AllowedMentions(everyone=True))

        embed = discord.Embed(
            title="✨ 新公告 ✨",
            description=message,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"由 {interaction.user.display_name} 發布", icon_url=interaction.user.avatar.url if interaction.user.avatar else interaction.user.default_avatar.url)
        embed.timestamp = interaction.created_at

        await channel.send(embed=embed)
        await interaction.response.send_message(f"公告已成功發布到 {channel.mention}。", ephemeral=True)
    except Exception as e:
        print(f"Error publishing announcement: {e}")
        await interaction.response.send_message(f"發布公告時發生錯誤: {e}", ephemeral=True)


@bot.tree.command(name="members", description="匯出伺服器成員及其身份組的 CSV 檔案。", guild=discord.Object(id=int(GUILD_ID)))
@is_admin()
async def members(interaction: discord.Interaction):
    """
    Exports a CSV file of server members and their roles.
    """
    await interaction.response.defer(ephemeral=True)
    try:
        # Create an in-memory text buffer
        output = io.StringIO()
        writer = csv.writer(output)

        # Write the header row
        header = ['Member Name', 'Roles']
        writer.writerow(header)

        # Iterate through all members in the guild
        for member in interaction.guild.members:
            # Get role names, excluding @everyone
            role_names = [role.name for role in member.roles if role.name != '@everyone']
            roles_str = '; '.join(role_names)
            writer.writerow([member.display_name, roles_str])

        # Seek to the beginning of the buffer
        output.seek(0)

        # Create a discord.File object
        csv_file = discord.File(fp=output, filename='members_export.csv')

        # Send the file as an ephemeral message
        await interaction.followup.send("這是您要求的成員列表 CSV 檔案：", file=csv_file, ephemeral=True)

    except Exception as e:
        print(f"Error exporting members: {e}")
        await interaction.followup.send(f"匯出成員列表時發生錯誤: {e}", ephemeral=True)


@bot.tree.command(name="help", description="顯示機器人所有可用指令的說明。", guild=discord.Object(id=int(GUILD_ID)))
async def help_command(interaction: discord.Interaction):
    """
    Displays information about all available commands.
    """
    embed = discord.Embed(
        title="🤖 Announce Bot 指令說明 🤖",
        description="以下是您可以使用的指令列表：",
        color=discord.Color.green()
    )

    embed.add_field(
        name="`/announce <頻道> <訊息>`",
        value=f"發布公告到指定的文字頻道。\n*權限要求: 伺服器管理員或 '{ADMIN_ROLE_NAME}' 角色*",
        inline=False
    )
    embed.add_field(
        name="`/members`",
        value=f"匯出伺服器所有成員的名稱及其身份組為 CSV 檔案。\n*權限要求: 伺服器管理員或 '{ADMIN_ROLE_NAME}' 角色*",
        inline=False
    )
    embed.add_field(
        name="`/help`",
        value="顯示此幫助訊息。",
        inline=False
    )

    embed.set_footer(text="使用斜線 (/) 即可查看所有指令。")
    await interaction.response.send_message(embed=embed, ephemeral=True)


if __name__ == "__main__":
    if DISCORD_BOT_TOKEN is None:
        print("Error: DISCORD_BOT_TOKEN not found in environment variables. Please create a .env file and set it.")
    elif GUILD_ID is None:
        print("Error: GUILD_ID not found in environment variables. Please create a .env file and set it.")
    else:
        bot.run(DISCORD_BOT_TOKEN)
