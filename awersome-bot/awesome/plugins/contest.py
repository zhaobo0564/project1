from nonebot import on_command, CommandSession
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json
import random


def getAtcoderMsg():
    file = open('atcoder.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    file.close()
    return data


def getCodeChefMsg():
    file = open('codechef.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    file.close()
    return data


def getCodeforcesMsg():
    file = open('cf.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    file.close()
    return data


def getNiuKeMsg():
    file = open('niuke.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    file.close()
    return data


def getText(msg):
    name = list(msg)
    text = ""
    for it in name:
        text += "比赛名称："
        text += it
        text += "\n\n比赛时间："
        text += str(msg[it])
        text += "\n\n"
    print(text)
    return text


def getNews():
    url = 'https://news.cnblogs.com/'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    content = []
    link = []
    div = soup.find("div", id="news_list")
    for h in div.find_all("h2"):
        a = h.find('a')
        content.append(a.string)
        link.append(a['href'])

    text = ""
    for i in range(0, 3):
        cnt = random.randint(0, len(content))
        text += "  " + content[cnt] + "\n"
        text += 'https://news.cnblogs.com' + link[cnt] + "\n\n"
    return text


@on_command('atcoder', aliases=('at', 'ac'))
async def contestatcode(session: CommandSession):
    msg = getAtcoderMsg()
    text = "比赛平台：atcoder\r\n"
    text += getText(msg)
    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('codechef', aliases=('cc', 'chef', 'Codechef', 'CODECHEF'))
async def contestCodeChef(session: CommandSession):
    msg = getCodeChefMsg()
    text = "比赛平台：codechef\r\n"
    text += getText(msg)
    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('cf', aliases=('CF', 'CODEFORCES', 'codeforces', 'CodeForces'))
async def contestCF(session: CommandSession):
    msg = getCodeforcesMsg()
    text = "比赛平台：codeforces\r\n"
    text += getText(msg)
    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('牛客', aliases=('nk', 'Nk', 'NIUKE', 'Nk'))
async def contestNIUKE(session: CommandSession):
    msg = getNiuKeMsg()
    text = "比赛平台：牛客\r\n"

    text += getText(msg)
    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('新闻')
async def news(session: CommandSession):
    text = getNews()

    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)


@on_command('通知该群')
async def notice(session: CommandSession):
    self_id = session.ctx['user_id']
    group_id = session.ctx['group_id']
    admins = await session.bot._get_group_info(group_id=group_id)
    print(admins['owner_id'])
    if self_id == 1173007724 or self_id == admins['owner_id']:  # 主人qq
        file = open('group.json', 'r', encoding='utf-8')
        js = file.read()
        group = json.loads(js)
        Id = group['group']
        for it in Id:
            if it == group_id:
                await session.bot.send_group_msg(group_id=session.ctx['group_id'], message="该群已经通知")
                return

        Id.append(group_id)
        group['group'] = Id
        print(group)
        fp = open("group.json", 'w', encoding='utf-8')
        item_json = json.dumps(group, ensure_ascii=False)
        fp.write(item_json)
        fp.close()
        file.close()
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message="好的! ！")
    else:
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message="你不是群主，无法操作！")


@on_command('取消通知该群')
async def CancelNotice(session: CommandSession):
    self_id = session.ctx['user_id']
    group_id = session.ctx['group_id']
    admins = await session.bot._get_group_info(group_id=group_id)
    if self_id == 1173007724 or self_id == admins['owner_id']:  # 主人qq
        file = open('group.json', 'r', encoding='utf-8')
        js = file.read()
        group = json.loads(js)
        Id = group['group']
        ID = []
        for it in Id:
            if it == group_id:
                continue
            ID.append(it)
        group["group"] = ID
        print(group)
        fp = open("group.json", 'w', encoding='utf-8')
        item_json = json.dumps(group, ensure_ascii=False)
        fp.write(item_json)
        fp.close()
        file.close()
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message="好的！")
    else:
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message="你不是群主，无法操作！")


@on_command('通知我')
async def NoticeMe(session: CommandSession):
    message_type = session.ctx['message_type']
    if (message_type == 'private'):
        self_id = session.ctx['user_id']
        file = open('id.json', 'r', encoding='utf-8')
        js = file.read()
        id = json.loads(js)
        Id = id['user']
        ID = []
        for it in Id:
            if it == self_id:
                await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="您已经被通知无需操作！")
                return
            ID.append(it)
        ID.append(self_id)
        id["user"] = ID
        print(id)
        fp = open("id.json", 'w', encoding='utf-8')
        item_json = json.dumps(id, ensure_ascii=False)
        fp.write(item_json)
        fp.close()
        file.close()
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="将在比赛开始前一个小时通知您！")
    else:
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="加好友才能操作哦！")


@on_command('取消通知我')
async def NoticeMe(session: CommandSession):
    message_type = session.ctx['message_type']
    if (message_type == 'private'):
        self_id = session.ctx['user_id']
        file = open('id.json', 'r', encoding='utf-8')
        js = file.read()
        id = json.loads(js)
        Id = id['user']
        ID = []
        for it in Id:
            if it == self_id:
                continue
            ID.append(it)
        id["user"] = ID
        print(id)
        fp = open("id.json", 'w', encoding='utf-8')
        item_json = json.dumps(id, ensure_ascii=False)
        fp.write(item_json)
        fp.close()
        file.close()
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message="已经取消！")


@on_command('菜单', aliases=('hellp'))
async def mnue(session: CommandSession):
    text = "小明cf （获取cf比赛信息，有时候会因为一些bug导致回复比较慢时间不准等问题）\r\n\r\n小明牛客 （同上）\r\n\r\n小明codechef (同上)\r\n\r\n小明atcoder(同上)\r\n\r\n小明新闻 （获取垃圾新闻）\r\n\r\n小明通知该群 （会在比赛前一个小时通知，对了，只有群主才能用此功能）\r\n\r\n小明取消通知该群 （取消通知比赛）\r\n\r\n小明通知我 （会在比赛一个小时前通知你，必须加我好友私聊我才可以，和上面功能一样，没啥用）\r\n\r\n小明取消通知我 (同上)\r\n\r\n更多垃圾功能尽情期待。"

    message_type = session.ctx['message_type']
    if (message_type == 'group'):
        await session.bot.send_group_msg(group_id=session.ctx['group_id'], message=text)
    elif (message_type == 'private'):
        await session.bot.send_private_msg(user_id=session.ctx['user_id'], message=text)

