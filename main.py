import setting as s
import discord, dateutil.parser, random, asyncio, time
#from discord import Activity, ActivityType, AutoShardedBot, Sticker
from discord.ext import commands
from discord.ui import View, Button
#from PIL import Image, ImageDraw, ImageFont
import numpy as np
from numpy import linalg as LA
import discord, random, requests, io, os, spotipy, json, datetime
from dotenv import load_dotenv
from os.path import join, dirname
from datetime import datetime, timedelta, timezone
from discord.ext import pages
from spotipy.oauth2 import SpotifyClientCredentials
from discord.ext import tasks
from discord.commands import Option, OptionChoice
from discord.ext.commands import MissingPermissions
import typing 
import urllib.parse
import requests
from discord_timestamps.formats import TimestampType
import discord_timestamps as dts 
import datetime as dt
load_dotenv()

def jst():
    now = datetime.datetime.utcnow()
    now = now + datetime.timedelta(hours=9)
    return now

token =  os.getenv('token')

JST = timezone(timedelta(hours=9))

BUMP_BOT_ID = 302050872383242240

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="e642f5ffe0034cde946a1396455a2344",
    client_secret="30372bec7f214db7b523b6e716bd37d2"))

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="a.", intents=intents)
bot.remove_command("help")

DATA_FILE = "member_stats.json"
ch_name = "┃log"

# データ読み込み
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# データ保存
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


#event ##################################################################################################


@bot.event
async def on_guild_join(guild):
    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    member_count = guild.member_count
    await bot.change_presence(
        activity=discord.Game(name=f"/help┃あはん鯖"),
        status=discord.Status.idle)


@bot.event
async def on_guild_remove(guild):
    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
        await bot.change_presence(
            activity=discord.Game(name=f"/help┃あはん鯖"),
            status=discord.Status.idle)


@bot.event
async def on_ready():
    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
        await bot.change_presence(
            activity=discord.Game(name=f"/help┃あはん鯖"),
            status=discord.Status.idle)
    print('起動完了')

    for channel in bot.get_all_channels():
        if channel.name == ch_name:
            runem = discord.Embed(
                title="<:e_wumpusx:1401767727630123109> 起動完了!!",
                description=
                f"<@869868208964915210>が起動しました",
                color=0x206694)
            await channel.send(embed=runem)

@bot.event
async def on_member_join(member):
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in data:
        data[today] = {"join": 0, "leave": 0}
    data[today]["join"] += 1
    save_data(data)
    channel = discord.utils.get(member.guild.text_channels, name="┃なんでも雑談") 
    if channel:
        await channel.send(f"**<:i_Join:1432754189091606579> {member.mention}が参加しました！**")
        b = Button(label=f"ここはどんなサーバー？",
                   url=f"https://discord.com/channels/1395422385460613120/1395422386609717269/1403203158271852545",
                   emoji=f"❓")
        view = View()
        view.add_item(b)
        await channel.send(view=view)

@bot.event
async def on_member_remove(member):
    data = load_data()
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in data:
        data[today] = {"join": 0, "leave": 0}
    data[today]["leave"] += 1
    save_data(data)
    channel = discord.utils.get(member.guild.text_channels, name="┃なんでも雑談")  
    if channel:
        await channel.send(f"**<:p_cry:1432024236033183804> {member.name}が退出しました...**") 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"実行者の必要な権限が無いため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BotMissingPermissions):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"Botの必要な権限が無いため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        embed.set_footer(text="お困りの場合は、サーバー管理者をメンションしてください。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"不明なコマンドもしくは現在使用不可能なコマンドです。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        embed.set_footer(text="/helpを実行してコマンドを確認しましょう。")
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"指定されたメンバーが見つかりません。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"指定された引数がエラーを起こしているため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    elif isinstance(error,
                    discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(title="<:d_icons_Wrong:1017795302830387290> エラー",
                              description=f"指定された引数が足りないため実行出来ません。",
                              timestamp=ctx.message.created_at,
                              color=discord.Colour.red())
        await ctx.send(embed=embed)
    else:
        raise error

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    e = discord.Embed(description=error, color=discord.Color.red())
    await ctx.respond(embeds=[e], ephemeral=True)

#Slash command #######################################################################################

'''
@bot.slash_command(name="verify", description="認証パネルを作成します")
async def verify(ctx, role: Option(discord.Role, description="認証後に付与されるロールを設定してください")):
  embed = discord.Embed(title="認証 - Verify", description=f"**「認証」**と書かれたボタンをクリックすると認証が完了します\n付与されるロール:{role}", color=0x206694)
  b = Button()
  await ctx.respond(embed=embed)
'''

@bot.slash_command(name="memberstats", description="サーバーの参加/退出統計を表示")
async def memberstats(
    ctx,
    period: str = Option(
        str,
        "期間を選択",
        choices=[
            OptionChoice(name="今日", value="today"),
            OptionChoice(name="昨日", value="yesterday"),
            OptionChoice(name="過去7日間", value="week"),
            OptionChoice(name="過去30日間", value="month")
        ]
    )
):
    await ctx.defer()

    data = load_data()
    now = datetime.now()

    embed = discord.Embed(
        title=f"📊 サーバー統計 ({period})",
        color=discord.Color.green()
    )
    
    if period == "today":
        key = now.strftime("%Y-%m-%d")
        stats = data.get(key, {"join": 0, "leave": 0})
        embed.add_field(name="今日", value=f"参加: {stats['join']}人\n退出: {stats['leave']}人", inline=False)
    elif period == "yesterday":
        key = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        stats = data.get(key, {"join": 0, "leave": 0})
        embed.add_field(name="昨日", value=f"参加: {stats['join']}人\n退出: {stats['leave']}人", inline=False)
    elif period == "week":
        desc = ""
        for i in range(7):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            stats = data.get(day, {"join": 0, "leave": 0})
            desc += f"{day} → 参加: {stats['join']} 退出: {stats['leave']}\n"
        embed.add_field(name="過去7日間", value=desc, inline=False)
    elif period == "month":
        desc = ""
        for i in range(30):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            stats = data.get(day, {"join": 0, "leave": 0})
            desc += f"{day} → 参加: {stats['join']} 退出: {stats['leave']}\n"
        embed.add_field(name="過去30日間", value=desc, inline=False)

    await ctx.followup.send(embed=embed)

@bot.slash_command(name="button", description="ボタンを作成します")
async def button(ctx, label: Option(str, description="ラベルを入力してください"), url:  Option(str, description="URLを入力してください"), emoji: Option(str, description="絵文字を設定できます")):
  b = Button(label=f"{label}",
             url=f"{url}",
             emoji=f"{emoji}")
  view = View()
  view.add_item(b)
  await ctx.respond(view=view)

@bot.slash_command(name="avatar", description="指定したユーザーのアバターを取得します")
async def avatar(ctx, user: discord.Member = None):
    if not user: user = ctx.author
    avatar = user.display_avatar
    embed = discord.Embed(description=f"{user.mention}'s Avatar",
                          color=0x206694)
    embed.set_author(name=str(user), icon_url=avatar)
    embed.set_image(url=avatar)
    embed.set_footer(text=f"Author: {ctx.author}")
    b = Button(label="URL",
               url=f"{avatar}")
    view = View()
    view.add_item(b)
    await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="banner", description="指定したユーザのバナーを取得します")
async def banner(interaction: discord.Interaction,
                 user: discord.Member = None):
    if not user: user = interaction.author
    user = await bot.fetch_user(user.id)
    try:
        banner_url = user.banner.url
        await interaction.respond(embed=discord.Embed(
            description=f"{user.mention}'s Banner", color=0x206694).set_image(
                url=banner_url).set_footer(
                    text=f"Author: {str(interaction.author)}"))
    except:
        await interaction.respond("バナーが見つかりません")


@bot.slash_command(name="clear", description="指定した数だけメッセージを削除します")
@commands.has_permissions(manage_messages=True)
async def purge(interaction: discord.Interaction, amount: int):
    deleted = await interaction.channel.purge(limit=amount + 1)
    embed = discord.Embed(title="Message Purged!", color=0x206694)
    embed.add_field(name=f"{len(deleted)-1} messages",
                    value="Automatically deleted after 3 seconds")
    embed.set_footer(text=f"Author: {interaction.author}")
    await interaction.respond(embed=embed, delete_after=3)

#@bot.slash_command(name="invite", description="指定したBotの招待URLを取得します")
#async def invite(ctx, id: discord.Member):
 #   e = discord.Embed(description=f"{id.mention}(**{id.id}**)",
  #                    color=0x206694)
   # date_format = "%Y/%m/%d %H:%M"
   # e.add_field(name=f"このBotの作成日",
    #            value=f"**`{id.created_at.strftime(date_format)}`**")
    #e.add_field(name="サーバー参加日",
    #value=f"**`{id.joined_at.strftime(date_format)}`**")
   # b = Button(
    #    label="権限無し",
     #   url=
      #  f"https://discord.com/oauth2/authorize?client_id={id.id}&permissions=0&scope=bot%20applications.commands"
   # )
    #b_2 = Button(
     #   label="管理者権限",
      #  url=
       # f"https://discord.com/oauth2/authorize?client_id={id.id}&permissions=8&scope=bot%20applications.commands"
    #)
    #view = View()
    #view.add_item(b)
    #view.add_item(b_2)
    #try:
     #   e.set_thumbnail(url=id.avatar.url)
    #except:
     #   e.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
      #  e.set_footer(text=f"Author: {str(ctx.author)}")
    #await ctx.respond(embed=e, view=view)


@bot.slash_command(name="ping", description="Botのping値を計測します")
async def ping(ctx: commands.Context):
    pingem = discord.Embed(
        title="Ping🏓",
        description=f"Ping値は**{round(bot.latency * 1000)}ms**です",
        color=0x206694)
    pingem.set_footer(text=f"Author: {ctx.author}")
    await ctx.respond(embed=pingem)


@bot.slash_command(name="mute", description="指定したメンバーをミュートします")
async def mute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        mute = discord.Embed(
            title="メンバーをミュートしました",
            description=f"{ctx.author.mention}さんが{member.mention}さんをミュートしました",
            color=0x206694)
        mute.set_footer(text=f"Author: {ctx.author}")
        await ctx.respond(embed=mute)
        guild = ctx.guild
        for channel in guild.channels:
            await channel.set_permissions(member, send_messages=False)
    else:
        await ctx.respond("このコマンドを実行できるのは管理者のみです！")


@bot.slash_command(name="unmute", description="指定したメンバーのミュートを解除します")
async def unmute(ctx, member: discord.Member):
    if ctx.author.guild_permissions.administrator:
        mute = discord.Embed(
            title="メンバーのミュートを解除しました",
            description=
            f"{ctx.author.mention}さんが{member.mention}さんのミュートを解除しました",
            color=0x206694,
        )
        mute.set_footer(text=f"Author: {ctx.author}")
        await ctx.respond(embed=mute)
        guild = ctx.guild
        for channel in guild.channels:
            await channel.set_permissions(member, overwrite=None)
    else:
        await ctx.respond("このコマンドを実行できるのは管理者のみです！")


@bot.slash_command(name="userinfo", description="指定したユーザーの情報を取得します")
async def userinfo(ctx, user: discord.Member = None):
    if not user: user = ctx.author
    async with ctx.channel.typing():
        date_format = "%Y/%m/%d"
        s = str(user.status)
        s_icon = ""
        if s == "online": s_icon = "🟢"
        elif s == "idle": s_icon = "🌙"
        elif s == "dnd": s_icon = "⛔"
        elif s == "offline": s_icon = "⚫"
        embed = discord.Embed(title=f"{user}({user.id})",
                              color=0x206694)
        embed.set_thumbnail(url=user.display_avatar)
        embed.add_field(name="Nickname",
                        value=f"> `{user.display_name}`",
                        inline=True)
        embed.add_field(name="Status", value=f"> `{s_icon} {s}`", inline=True)
        if len(user.roles) >= 1:
            role_string = " ".join([r.mention for r in user.roles][1:])
            embed.add_field(name=f"Roles(`{len(user.roles)-1}`)",
                            value=f"> {role_string}",
                            inline=False)
        embed.add_field(name="Created Account",
                        value=f"> `{user.created_at.strftime(date_format)}`",
                        inline=True)
        embed.add_field(name="Joined Server",
                        value=f"> `{user.joined_at.strftime(date_format)}`",
                        inline=True)
        user = await bot.fetch_user(user.id)
        try:
            embed.set_image(url=user.banner.url)
        except:
            pass
        embed.set_footer(text=f"Author: {str(ctx.author)}")
        await ctx.respond(embed=embed)


@bot.slash_command(name="help", description="ヘルプパネルを表示します")
async def help(ctx: commands.Context):
    embed = discord.Embed(title="Help",
                          description="Prefix: `/`",
                          color=0x206694)
    embed.add_field(name="🤖 ≫ Bot",
                    value="> `ping`, `help`, `about`",
                    inline=False)
    embed.add_field(
        name="🔨 ≫ Moderation",
        value="> `clear`, `mute`, `unmute`, `kick`, `ban`, `slowmode`, `nuke`",
        inline=False)
    embed.add_field(
        name="💻 ≫ Tool",
        value=
        "> `serverinfo`, `userinfo`, `spotify`, `avatar`, `banner`, `button`",
        inline=False)
    embed.add_field(name="🛠️ ≫ Admin",
                    value="> `leave`, `globalban`, `guilds`, `memberstats`",
                    inline=False)
    embed.add_field(name="🎉 ≫ fun",
                    value="> `cat`, `totusi`, `5000choyen`",
                    inline=False)
    embed.set_image(
        url=
        "https://cdn.discordapp.com/attachments/1395422386609717274/1432796756403421304/rumtyahan.png?ex=69025b76&is=690109f6&hm=e98817a46e86fac01543218ea700632af1c3c034f15e2ebd8e7dea304bd6695e&"
    )
    embed.set_footer(text=f"Author: {str(ctx.author)}")
    await ctx.respond(embed=embed)


@bot.slash_command(name="about", description="このBotについて")
async def about(ctx: commands.Context):
    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    embed = discord.Embed(title="About",
                          description="About <@869868208964915210>",
                          color=0x206694)
    embed.add_field(name="言語 - Language",
                    value="> **discord.py(version 2.0.1)**",
                    inline=True)
    embed.add_field(name="サーバー - Guilds",
                    value=f"> **{str(servers)}サーバー**",
                    inline=True)
    embed.add_field(name="ユーザー - Users",
                    value=f"> **{str(members)}ユーザー**",
                    inline=True)
    embed.add_field(name="ピング - Ping",
                    value=f"> **{round(bot.latency * 1000)}ms**",
                    inline=True)
    embed.add_field(
        name="開発者 - Developer",
        value=f"**[Rumty](https://discordapp.com/users/691137657484476466)**",
        inline=True)
    embed.set_footer(text=f"Author: {ctx.author}")
    await ctx.respond(embed=embed)


@bot.slash_command(name="serverinfo", description="サーバー情報を取得します")
async def serverinfo(ctx):
    guild = ctx.guild
    name = str(ctx.guild.name)
    sid = str(ctx.guild.id)
    owner = str(ctx.guild.owner.id)
    mcount = str(ctx.guild.member_count)
    ucount = str(sum(1 for member in guild.members if not member.bot))
    bcount = str(sum(1 for member in guild.members if member.bot))
    tchannels = len(ctx.guild.text_channels)
    vchannels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = tchannels + vchannels
    embed = discord.Embed(title=f"{name}",
                          description="Information about this server.",
                          color=0x206694)
    embed.add_field(
        name="Owner",
        value=f"<@{owner}>",
        inline=True)
  
    embed.add_field(
        name="Server ID",
        value=f"{sid}",
        inline=True)

    embed.add_field(
        name="Creation day",
        value = f"{dts.format_timestamp(guild.created_at.timestamp(), TimestampType.RELATIVE)}",
        inline=True)
        
    embed.add_field(
        name=f"Member({mcount})",
        value=f"**{ucount}**users\n**{bcount}**bots",
        inline=True)
    embed.add_field(
        name=f"Channel({channels})",
        value=
        f"**{tchannels}**text channels\n**{vchannels}**voice channels\n**{categories}**categorys",
        inline=True,
    )
    embed.set_thumbnail(url = guild.icon.url)
    embed.set_footer(text=f"Author: {ctx.author}")
    await ctx.respond(embed=embed)

@bot.slash_command(name="spotify", description="メンバーがSpotifyで聴いてる曲を取得します")
async def spotify(ctx, user: discord.Member = None):
    if not user: user = ctx.author
    _spotify_result = next((activity for activity in user.activities
                            if isinstance(activity, discord.Spotify)), None)
    if _spotify_result is None:
        await ctx.respond(f"**{user.name}**さんは現在Spotifyで音楽を聴いていません！")
    if _spotify_result:
        embed = discord.Embed(color=_spotify_result.color)
        embed.set_thumbnail(url=_spotify_result.album_cover_url)
        embed.set_footer(text=f"Author: {str(ctx.author)}")
        embed.add_field(name="Title", value=f"```{_spotify_result.title}```")
        artists = _spotify_result.artists
        if not artists[0]: re_result = _spotify_result.artist
        else: re_result = ', '.join(artists)
        embed.add_field(name="Artist", value=f"```{re_result}```")
        embed.add_field(name="Album",
                        value=f"```{_spotify_result.album}```",
                        inline=False)
        embed.add_field(
            name="Time",
            value=
            f"```{dateutil.parser.parse(str(_spotify_result.duration)).strftime('%M:%S')}```"
        )
        #embed.add_field(name="URL", value=f"```https://open.spotify.com/track/{_spotify_result.track_id}```", inline=False)
        embed.set_footer(text=f"Author: {str(ctx.author)}")
        view = View()
        b = Button(
            label="URL",
            url=f"https://open.spotify.com/track/{_spotify_result.track_id}")
        jacket = Button(label="ジャケット", style=discord.ButtonStyle.green)

        async def Button_callback(interaction: discord.Interaction):
            await interaction.response.send_message(
                _spotify_result.album_cover_url, ephemeral=True)

        jacket.callback = Button_callback
        view.add_item(b)
        view.add_item(jacket)
        await ctx.respond(embed=embed, view=view)


@bot.slash_command(name="slowmode", description="チャンネルの低速モードを設定します")
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: Option(str, description="秒数を設定してください")):
    await ctx.channel.edit(slowmode_delay=seconds)
    embed = discord.Embed(title="設定完了！",
                          description=f"このチャンネルの低速モードを**{seconds}秒**に設定しました！",
                          color=0x206694)
    embed.set_footer(text=f"Author: {str(ctx.author)}")
    await ctx.respond(embed=embed)


@bot.slash_command(name="nuke", description="チャンネルを再作成")
@commands.has_permissions(administrator=True)
async def delete(interaction,
                 channel: discord.TextChannel = None,
                 meonly: Option(str, "再作成後にチャンネルメンションの表示について",
                                choices=["Yes", "No"]) = None):
    if not channel: channel = interaction.channel
    else:
        channel = discord.utils.get(interaction.guild.channels,
                                    name=channel.name)
    pos = channel.position
    await channel.delete()
    new_channel = await channel.clone()
    await new_channel.edit(position=pos)
    if meonly in ("Yes"):
        await interaction.respond(f"<#{new_channel.id}>", ephemeral=True)
    else:
        await interaction.respond(f"<#{new_channel.id}>")


@bot.slash_command(name="guilds", description="管理者専用")
async def inserver(interaction: discord.Interaction):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.send("管理者専用です")
        return
    with open("server.txt", "w", encoding='utf-8') as f:
        activeservers = bot.guilds
        for guild in activeservers:
            f.write(f"[ {str(guild.id)} ] {guild.name}\n")
    await interaction.response.send_message(file=discord.File(
        "server.txt", filename="SERVERLIST.txt"),
                                            ephemeral=True)


@bot.slash_command(name="leave", description="管理者専用")
async def leave(interaction, guild_id=None):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("管理者専用です", ephemeral=True)
        return
    guild = bot.get_guild(int(guild_id))
    await guild.leave()
    await interaction.respond(f"**{guild}**から脱退しました。")


@bot.slash_command(name="globalban", description="管理者専用")
async def global_ban(interaction, member: discord.Member, reason: str):
    if not int(interaction.author.id) in s.admin_users:
        await interaction.response.send_message("管理者専用です", ephemeral=True)
        return
    msg_1 = await interaction.response.send_message(
        "<a:S_Loading:1023051592443904030>")
    count = 0
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(f"done!!\n")
     # [{datetime.datetime.now()}]
        for guild in bot.guilds:
            try:
                await guild.ban(member, reason=reason)
                f.write(f"SUCCESS [{guild.id:>20} ] {guild}\n")
                count += 1
            except:
                f.write(f"FAILURE [{guild.id:>20} ] {guild}\n")
    e = discord.Embed(description=f"Name: **{member}**\nID: **{member.id}**",
                      color=0xff0000)
    e.add_field(
        name=f"Global BAN Result",
        value=f"Success: **{count:<4}**\nFailure: **{len(bot.guilds) - count}**"
    ).add_field(name="Reason", value=f"```{reason}```", inline=False)
    await msg_1.edit_original_message(content=None, embed=e)
    await interaction.respond(file=discord.File("result.txt",
                                                filename="GbanResult.txt"),
                              ephemeral=True)


@bot.slash_command(name="ban", description="指定したメンバーをbanします")
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: Option(discord.Member, description="Banするメンバー"),
              reason: Option(str, description="reason", required=False)):
    if member.id == ctx.author.id:  #checks to see if they're the same
        await ctx.respond("自分自身をbanする事はできません！")
    else:
        if reason == None:
            reason = f"Author: {ctx.author}"
        await member.ban(reason=reason)
        ban = discord.Embed(
            title="メンバーをBANしました。",
            description=f"{ctx.author.mention}さんが{member.mention}さんをBANしました。",
            color=0x206694)
        ban.set_footer(text=f"Author: {str(ctx.author)}")
        await ctx.respond(embed=ban)


@ban.error
async def banerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたは権限を持っていません！")
    else:
        await ctx.respond("...?")  #most likely due to missing permissions
        raise error


@bot.slash_command(name="kick", description="指定したメンバーをkickします")
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: Option(discord.Member, description="kickするメンバー"),
               reason: Option(str, description="reason", required=False)):
    if member.id == ctx.author.id:  #checks to see if they're the same
        await ctx.respond("自分自身をkickする事はできません！")
    else:
        if reason == None:
            reason = f"Author: {ctx.author}"
        await member.kick(reason=reason)
        kick = discord.Embed(
            title="メンバーをキックしました。",
            description=f"{ctx.author.mention}さんが{member.mention}さんをキックしました。",
            color=0x206694)
        kick.set_footer(text=f"Author: {str(ctx.author)}")
        await ctx.respond(embed=kick)


@kick.error
async def kickerror(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.respond("あなたは権限を持っていません！")
    else:
        await ctx.respond("...?")  #most likely due to missing permissions
        raise error


@bot.slash_command(name="cat", description="猫の画像を送信します")
async def cat(interaction: discord.Interaction, tag: typing.Optional[str]):
    if tag == None:
        # no tags
        await interaction.response.send_message("https://cataas.com" +
                                                get_url("null"))
    else:
        # tags
        await interaction.response.send_message("https://cataas.com" +
                                                get_url(tag))


def get_url(tag):
    x = "initiate"
    if tag == "null":
        x = requests.get("https://cataas.com/cat?json=true").json()
    else:
        x = requests.get(f"https://cataas.com/cat/{tag}?json=true").json()

    return x["url"]


@bot.slash_command(name="totusi", description="突然の死AAを作成します")
async def totusi(ctx, text: Option(str, description="文字を入れてください")):
    await asyncio.sleep(0)
    ue = "人" * len(text)
    sita = "^Y" * len(text)
    embed = discord.Embed(title="突然の死ジェネレーター",
                          description="```＿人" + ue + "人＿\n＞　" + text +
                          "　＜\n￣^Y" + sita + "^Y￣```",
                          color=0x206694)
    embed.set_footer(text=f"Author: {str(ctx.author)}")
    await ctx.respond(embed=embed)


@bot.slash_command(name="5000choyen", description="5000兆円ジェネレーターです")
async def choyen(ctx, top="5000兆円", bottom="欲しい！"):
    embed = discord.Embed(title="5000兆円ジェネレーター",
                          description=f"{top}{bottom}",
                          color=0x3498DB)
    embed.set_image(
        url="https://gsapi.cbrx.io/image?"
        f"top={urllib.parse.quote(top)}&bottom={urllib.parse.quote(bottom)}")
    await ctx.respond(embed=embed)


###############################################################################################

#User command ##################################################################################


@bot.user_command(name="user info")
async def accountdetails(interaction: discord.Interaction,
                         usr: discord.Member):
    date_format = "%Y/%m/%d %H:%M"
    e = discord.Embed(description=f"**名前:** {usr}\n**ID  :** {usr.id}\n",
                      color=0x206694).set_thumbnail(url=usr.display_avatar)
    e.add_field(name=f"アカウント作成日",
                value=f"**`{usr.created_at.strftime(date_format)}`**")
    e.add_field(name="サーバー参加日",
                value=f"**`{usr.joined_at.strftime(date_format)}`**")
    await interaction.response.send_message(embed=e, ephemeral=True)


@bot.user_command(name="Avatar")
async def avatar(ctx, user: discord.Member = None):
    if not user: user = ctx.author
    avatar = user.display_avatar
    embed = discord.Embed(description=f"{user.mention} のアバター", color=0x206694)
    embed.set_author(name=str(user), icon_url=avatar)
    embed.set_image(url=avatar)
    embed.set_footer(text=f"Author: {ctx.author}")
    await ctx.respond(embed=embed, ephemeral=True)


##################################################################################################

#Message command ##################################################################################
##################################################################################

bot.run(token)