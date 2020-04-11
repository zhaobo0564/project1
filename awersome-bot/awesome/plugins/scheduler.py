from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
import json
import requests
from bs4 import BeautifulSoup


def judge(years):
    if years % 4 == 0 and years % 100 != 0:
        return True
    else:
        return False


def change(date, hour, minute):
    min = date.minute
    hr = date.hour
    day = date.day
    month = date.month
    year = date.year
    min += minute
    if min >= 60:
        min -= 60
        hr += 1
    hr += hour
    if hr >= 24:
        hr -= 1
        day += 1
    if day == 30 and month == 2 and judge(year):  # 判断是否为闰年
        month += 1
        day -= 29
    elif day == 29 and month == 2 and judge(year) == False:
        day -= 28
        month += 1
    elif day == 31 and month in (4, 6, 9, 11):
        day -= 30
        month += 1
    elif day == 32:
        day -= 31
        month += 1
    if month > 12:
        month = 1
        year += 1
    if min < 10:
        time = ("%s-%s-%s %s:0%s") % (year, month, day, hr, min)
        return time

    time = ("%s-%s-%s %s:%s") % (year, month, day, hr, min)
    return time


def getAtcoder():
    url = 'https://atcoder.jp/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
    }
    r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    div = soup.find("div", id="contest-table-upcoming")

    if div is None:

        print("最近没有比赛")


    else:
        name = []
        time = []
        tbody = div.find("tbody")
        for it in tbody.find_all("tr"):
            a = it.find_all("a")
            time.append(a[0].string)
            name.append(a[1].string)

        data = {}
        for i in range(0, len(name)):
            ti = time[i][:-8]
            date = datetime.strptime(ti, '%Y-%m-%d %H:%M')
           # print(date)
            #print(name[i])
            data[name[i]] = change(date=date, hour=-1, minute=0)  # 日本时差1小时
            #print(change(date=date, hour=-1, minute=0))
       # print(data)
        fp = open("atcoder.json", 'w', encoding='utf-8')
        item_json = json.dumps(data, ensure_ascii=False)
        fp.write(item_json)
        fp.close()


def getCodeChef():
    url = 'https://www.codechef.com/contests'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0)Gecko/20100101 Firefox/66.0"
    }
    r = requests.get(url, timeout=30, headers=headers)
    if (r.status_code != 200):  # 由于codechef网站访问比较慢当出错的时候就在进行访问一次
        r = requests.get(url, timeout=30, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find_all("table", class_="dataTable")
    table = table[1]
    tbody = table.find("tbody")
    name = []
    time = []

    data_time = tbody.find_all("td", class_="start_date")
    for it in tbody.find_all('td'):
        # print(it)

        a = it.find("a")
        if a is not None:
            name.append(a.string)

    for it in data_time:
        time.append(it.text)

    for i in range(0, len(time)):
        date = datetime.strptime(time[i], '%d %b %Y  %H:%M:%S')
        time[i] = change(date, hour=2, minute=30)  # 印度与中国时间相差2时30分
    # 创建字典 比赛名称-->时间

    data = {}

    for i in range(0, len(time)):
        data[name[i]] = time[i]

    # 将获取的字典信息 导入json  不建议用数据库 因为信息比较少用json文件方便
    fp = open("codechef.json", 'w', encoding='utf-8')
    item_json = json.dumps(data, ensure_ascii=False)
    fp.write(item_json)
    fp.close()


def getCodefores():
    contest_name = []
    contest_time = []
    urls = 'https://codeforces.com/contests'
    r = requests.get(urls, timeout=30)
    if r.status_code != 200:
        return
    else:

        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", class_="contestList")
        table = div.find("table", class_="")
        for tr in table.find_all('tr'):
            for td in tr.find_all('td'):
                contest_name.append(td.string)
                break;

        for tr in table.find_all('tr'):
            # print(tr)
            for td in tr.find_all('td'):
                span = td.find("span", class_='format-time')
                if span:
                    contest_time.append(span.string)

        t = []
        for it in contest_time:
            dete = datetime.strptime(it, '%b/%d/%Y %H:%M')
            #print(dete)
            times = change(date=dete, hour=5, minute=0)
            t.append(times)
        cnt = {}
        for i in range(0, len(contest_time)):
            if 'Div. 1' in contest_name[i][2:-6]:
                continue
            cnt[contest_name[i][2:-6]] = t[i]
        fp = open("cf.json", 'w', encoding='utf-8')
        item_json = json.dumps(cnt, ensure_ascii=False)
        fp.write(item_json)
        fp.close()


def getNiuKe():
    url = 'https://ac.nowcoder.com/acm/contest/vip-index?rankTypeFilter=0&signUpFilter=&topCategoryFilter=13&orderType=NO'
    html = requests.get(url)
    if html.status_code != 200:
        return
    else:
        soup = BeautifulSoup(html.text, "html.parser")
        data = {}

        div = soup.find("div", class_="nk-main with-banner-page clearfix js-container")
        div_content = div.find("div", class_="nk-content")
        div_contest = div_content.find("div", class_="platform-mod js-current")
        for contest in div_contest.find_all("div", class_="platform-item js-item"):
            next = contest.find("div", class_="platform-item-cont")
            a = next.find("a")
            li = next.find('li', class_='match-time-icon')
            name = a.string
            if "小白" in name or "练习赛" in name or "周周" in name or "挑战赛" in name:
                data[name] = li.string
        name = list(data)
        f = 0
        for it in name:
            time = data[it][:21]
            time = time[5:]
            data[it] = time

        fp = open("niuke.json", 'w', encoding='utf-8')
        item_json = json.dumps(data, ensure_ascii=False)
        fp.write(item_json)
        fp.close()


### 获取每场比赛最近的时间

def getFirstNiuke():
    file = open('niuke.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    niuke = {}
    niuke[name[0]] = data[name[0]]
    return niuke


def getFirstCf():
    file = open('cf.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    cf = {}
    cf[name[0]] = data[name[0]]
    return cf


def getFirstCodeChef():
    file = open('codechef.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    codechef = {}
    codechef[name[0]] = data[name[0]]
    return codechef


def getFirstAtcoder():
    file = open('atcoder.json', 'r', encoding='utf-8')
    js = file.read()
    data = json.loads(js)
    name = list(data)
    atcoder = {}
    atcoder[name[0]] = data[name[0]]
    return atcoder


# 判断该时间 与先找的时间进行比较 相差小时进行通知

def getAns(date1, date2):
    days = (date1 - date2).days
    print("天")
    print(days)
    # month = (date1 - date2).month  # 年就不要考虑 概率比较小
    if days == 0 and date1.month == date2.month:
        hours = (date1.hour - date2.hour)
        min = (date1.minute - date2.minute)
        print("小时")
        print(hours)
        print("分钟")
        print(min)
        if hours == 1 and min == 0:
            return hours
    return -1000000


# 导入要通知的群与 好友
def loadGroup() -> list:
    file = open('group.json', 'r', encoding='utf-8')
    js = file.read()
    group = json.loads(js)
    group_id = group['group']
    print("通知的群号")
    print(group_id)
    return group_id


def loadId() -> list:
    file = open('id.json', 'r', encoding='utf-8')
    js = file.read()
    id = json.loads(js)
    ID = id['user']
    printf("通知的账号：")
    print(ID)
    return ID


# 'interval', minutes=10

@nonebot.scheduler.scheduled_job('interval', minutes=120)  # 2小时进行1次爬虫
async def loadMsg():
    getNiuKe()
    getCodefores()
    getCodeChef()
    getAtcoder()
    print("导入信息")


@nonebot.scheduler.scheduled_job('interval', minutes=1)
async def _():
    bot = nonebot.get_bot()
    now = datetime.now()
    cf = getFirstCf()
    niuke = getFirstNiuke()
    codechef = getFirstCodeChef()
    atcoder = getFirstAtcoder()

    #  cf
    name = list(cf)
    time = cf[name[0]]
    print("*"*10 + "cf")
    print(time)
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print(dates)
    ans = getAns(dates, now)
    # loadGroup()
    if ans == 1:
        if dates.minute < 10:
            text = "比赛平台 codeforces  \r\n" + name[0] + ", 将会在今天 %s : 0%s 举行记得准时参加哦" % (
                str(dates.hour), str(dates.minute))
        else:
            text = "比赛平台 codeforces  \r\n" + name[0] + ", 将会在今天 %s : %s 举行记得准时参加哦" % (
            str(dates.hour), str(dates.minute))
        try:

            group = loadGroup()
            for it in group:
                await bot.send_group_msg(group_id=it, message=text)
            ID = loadId()
            for it in ID:
                await bot.send_private_msg(user_id=it, message=text)
        except CQHttpError:
            pass

    # 牛客

    name = list(niuke)
    time = niuke[name[0]]
    print("*"*10 + "牛客")
    print(time)
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    ans = getAns(dates, now)

    if ans == 1:
        text = ""
        if (dates.minute < 10):
            text = "比赛平台：牛客  \r\n " + name[0] + ", 将会在今天 %s : 0%s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        else:
            text = "比赛平台：牛客  \r\n " + name[0] + ", 将会在今天 %s : %s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        try:
            group = loadGroup()
            for it in group:
                await bot.send_group_msg(group_id=it, message=text)
            ID = loadId()
            for it in ID:
                await bot.send_private_msg(user_id=it, message=text)

        except CQHttpError:
            pass
    # codechef

    name = list(codechef)
    time = codechef[name[0]]
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print("*" * 10 + "codechef")
    print(dates)
    ans = getAns(dates, now)
    if ans == 1:
        text = ""
        if (dates.minute < 10):
            text = "比赛平台 codechef \r\n" + name[0] + ", 将会在今天 %s : 0%s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        else:
            text = "比赛平台 codechef \r\n" + name[0] + ", 将会在今天 %s : %s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        try:
            group = loadGroup()
            for it in group:
                await bot.send_group_msg(group_id=it, message=text)
            ID = loadId()
            for it in ID:
                await bot.send_private_msg(user_id=it, message=text)

        except CQHttpError:
            pass

    # atcoder

    name = list(atcoder)
    time = atcoder[name[0]]
    dates = datetime.strptime(time, "%Y-%m-%d %H:%M")
    print("**"*5 + "atcoder")
    print(dates)
    ans = getAns(dates, now)
    if ans == 1:
        text = ""
        if (dates.minute < 10):
            text = "比赛平台 atcoder \r\n" + name[0] + ", 将会在今天 %s : 0%s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        else:
            text = "比赛平台 atcoder \r\n" + name[0] + ", 将会在今天 %s : %s 举行记得准时参加哦" % (str(dates.hour), str(dates.minute))
        try:
            group = loadGroup()
            for it in group:
                await bot.send_group_msg(group_id=it, message=text)
            ID = loadId()
            for it in ID:
                await bot.send_private_msg(user_id=it, message=text)

        except CQHttpError:
            pass