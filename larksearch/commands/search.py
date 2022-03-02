from datetime import datetime
from urllib.parse import quote
from urllib.request import urlopen
from re import compile

from bs4 import BeautifulSoup
from bs4.element import Tag
from discord import Embed
from discord.ext.commands import Context
from discord.ext.commands import Command


NUMERIC_PATTERN = compile('[0-9][,.0-9]+')


def extract_number(string: str) -> float:
    numeric_string = next(NUMERIC_PATTERN.finditer(string)).group()
    numeric_string = numeric_string.replace(',', '')
    return float(numeric_string)


async def search(ctx: Context, *, arg: str):
    if ctx.author.bot:
        return
    username = arg
    embed = Embed(title="... **검색중입니다. 잠시만 기다려주세요.**",
                  color=0X36393F)
    message = await ctx.send(embed=embed)
    try:
        embed = embed_user(username)
    except:
        embed = embed_user_not_found(username)
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    await message.edit(embed=embed)


def embed_user_not_found(name: str) -> Embed:
    embed = Embed(title=name,
                  description="플레이어 정보가 존재하지 않습니다.",
                  color=0X36393F,
                  timestamp=datetime.utcnow())
    return embed


def embed_server_is_down(name: str) -> Embed:
    embed = Embed(title=name,
                  description="전투 정보실에 접속할 수 없습니다.",
                  color=0X36393F,
                  timestamp=datetime.utcnow())
    return embed


def embed_user(name: str) -> Embed:
    profile_url = f"https://lostark.game.onstove.com/Profile/Character/{quote(name)}"
    html = urlopen(profile_url)
    soup = BeautifulSoup(html, "html.parser")
    embed = Embed(title=name,
                  description=user_server(soup),
                  color=0X36393F,
                  timestamp=datetime.utcnow())
    embed.set_author(name=class_name(soup))
    embed.set_thumbnail(url=class_image_src(soup))
    embed.add_field(name="아이템 레벨",
                    value=f"**`{item_level(soup)}`**",
                    inline=True)
    embed.add_field(name="원정대 레벨",
                    value=f"**`{expedition_level(soup)}`**",
                    inline=True)
    embed.add_field(name="길드",
                    value=f"**`{user_guild(soup)}`**",
                    inline=True)
    embed.add_field(name="정보 더보기",
                    value=(
                        f"[전투정보실]({profile_url})\t"
                        f"[로아와](https://loawa.com/char/{name})\n"
                        "\n"
                    ),
                    inline=False)
    return embed


def item_level(soup: BeautifulSoup) -> float:
    """아이템 레벨"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)')
    return extract_number(tag.get_text())


def character_level(soup: BeautifulSoup) -> float:
    """캐릭터 레벨"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__item > span:nth-child(2)')
    return extract_number(tag.get_text())


def expedition_level(soup: BeautifulSoup) -> float:
    """원정대 레벨"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)')
    return extract_number(tag.get_text())


def domain_level(soup: BeautifulSoup) -> float:
    """영지 레벨"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__wisdom > span:nth-child(2)')
    return extract_number(tag.get_text())


def _class_image(soup: BeautifulSoup) -> Tag:
    """클래스 이미지"""
    return soup.select_one('#lostark-wrapper > div > main > div > div.profile-character-info > img')


def class_image_src(soup: BeautifulSoup) -> str:
    tag = _class_image(soup)
    return tag['src']


def class_name(soup: BeautifulSoup) -> str:
    """클래스 명"""
    tag = _class_image(soup)
    return tag['alt']


def user_title(soup: BeautifulSoup) -> str:
    """칭호"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__title > span:nth-child(2)')
    return tag.get_text()


def user_guild(soup: BeautifulSoup) -> str:
    """길드"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.game-info > div.game-info__guild > span:nth-child(2)')
    return tag.get_text()


def user_server(soup: BeautifulSoup) -> str:
    """서버"""
    tag = soup.select_one(
        '#lostark-wrapper > div > main > div > div.profile-character-info > span.profile-character-info__server')
    return tag.get_text()


def itemlv_to_gold(item_level: float) -> int:
    if item_level < 1325:
        return 0
    elif item_level < 1370:
        return 1300
    elif item_level < 1415:
        return 2900
    elif item_level < 1430:
        return 4100
    elif item_level < 1445:
        return 6600
    elif item_level < 1460:
        return 8600
    elif item_level < 1475:
        return 10600
    elif item_level < 1490:
        return 13500
    elif item_level < 1500:
        return 13500
    elif item_level < 1520:
        return 15000
    elif item_level < 1540:
        return 17500
    elif item_level < 1550:
        return 18500
    elif item_level < 1560:
        return 19000
    else:
        return 19500


command = Command(search,
                  name="검색",
                  aliases=['정보', '캐릭터', '캐릭'],
                  usage="!검색 [닉네임]",
                  help="전투정보실에서 플레이어의 정보를 불러옵니다.")
