from datetime import datetime
from random import choice
from urllib.request import urlopen

from bs4 import BeautifulSoup
from bs4.element import Tag
from discord import Embed
from discord import Message
from discord.ext.commands import Context
from discord.ext.commands import Command

from larksearch.bot import bot


def add_command():
    bot.add_command(
        Command(notice,
                name="공지사항",
                aliases=['공지', '업데이트', '패치', '업뎃', '패치노트'],
                usage="!공지",
                help="로스트아크 홈페이지의 공지사항을 불러옵니다.")
    )


async def notice(ctx: Context, *arg):
    if ctx.author.bot:
        return
    embed = Embed(title="... **검색중입니다. 잠시만 기다려주세요.**",
                  color=0X36393F)
    message: Message = await ctx.send(embed=embed)
    embed = get_notice_embed()
    await message.edit(embed=embed)


def get_notice_embed() -> Embed:
    url = 'https://lostark.game.onstove.com/News/Notice/List?noticetype=all'
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    embed = Embed(title="로스트아크 공지사항",
                  description="로스트아크 점검 시, 봇의 기능이 제한됩니다.",
                  color=0X36393F,
                  timestamp=datetime.utcnow())
    embed.add_field(name=f"**이슈**",
                    value=f"[:arrow_forward: {issue_title(soup)}]({issue_url(soup)})\n",
                    inline=False)
    for i in range(3):
        embed.add_field(name=f"**공지사항 {i+1}**",
                        value=f"[:arrow_forward: {nth_notice_title(soup, i)}]({nth_notice_url(soup, i)})\n",
                        inline=False)
    embed.set_image(url=get_random_image_src())
    embed.set_footer(text="LarkSearch", icon_url="https://bit.ly/3FzSF1Q")
    return embed


def _issue(soup: BeautifulSoup) -> Tag:
    tag = soup.select_one(
        '#list > div.list.list--default > ul:nth-child(1) > li:nth-child(1)')
    return tag


def issue_title(soup: BeautifulSoup) -> str:
    tag = _issue(soup)
    return tag.find('span',{'class':'list__title'}).get_text()


def issue_url(soup: BeautifulSoup) -> str:
    tag = _issue(soup)
    relative_path = tag.find('a')['href']
    return f"https://lostark.game.onstove.com{relative_path}"


def _nth_notice(soup: BeautifulSoup, index: int) -> Tag:
    tag = soup.select_one(
        f'#list > div.list.list--default > ul:nth-child(2) > li:nth-child({index+1})')
    return tag


def nth_notice_title(soup: BeautifulSoup, index: int) -> str:
    tag = _nth_notice(soup, index)
    title_tag = tag.find('span', {'class': 'list__title'})
    return title_tag.get_text()


def nth_notice_url(soup: BeautifulSoup, index: int) -> str:
    tag = _nth_notice(soup, index)
    relative_path = tag.find('a')['href']
    return f"https://lostark.game.onstove.com{relative_path}"


def get_random_image_src() -> str:
    url = 'https://lostark.game.onstove.com/Artwork'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find('div', {"class": "list list--artwork"}).find_all('li')
    img_src_list = list(map(lambda tag: tag.find('a')['href'], images))
    random_img_src = choice(img_src_list)
    return random_img_src


# 이 모듈을 import 하는 것 만으로 커멘드가 추가되도록 함.
add_command()
