import requests, datetime, pytz
from dateutil import parser
from bs4 import BeautifulSoup

TZ=pytz.timezone("Asia/Kolkata")

def fetch_all():
    out=[]

    # ---------- Codeforces ----------
    try:
        cf=requests.get("https://codeforces.com/api/contest.list",timeout=10).json()["result"]
        for c in cf:
            if c["phase"]=="BEFORE":
                start=datetime.datetime.fromtimestamp(c["startTimeSeconds"],pytz.utc).astimezone(TZ)
                out.append((c["name"],start,"https://codeforces.com"))
    except:
        print("CF fetch failed")

    # ---------- LeetCode ----------
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        r=requests.get("https://leetcode.com/contest/api/list/",headers=headers,timeout=10)
        data=r.json()

        for c in data.get("contests",[]):
            start=datetime.datetime.fromtimestamp(c["start_time"],pytz.utc).astimezone(TZ)
            if start>datetime.datetime.now(TZ):
                out.append((c["title"],start,"https://leetcode.com"))
    except:
        print("LeetCode fetch failed")

    # ---------- CodeChef ----------
    try:
        headers={"User-Agent":"Mozilla/5.0"}
        cc=requests.get("https://www.codechef.com/api/list/contests/all",headers=headers,timeout=10).json()
        for c in cc.get("future_contests",[]):
            start=parser.parse(c["contest_start_date"]).astimezone(TZ)
            out.append((c["contest_name"],start,"https://codechef.com"))
    except:
        print("CodeChef fetch failed")

    # ---------- AtCoder ----------
    try:
        from bs4 import BeautifulSoup
        headers={"User-Agent":"Mozilla/5.0"}
        html=requests.get("https://atcoder.jp/contests/",headers=headers,timeout=10).text
        soup=BeautifulSoup(html,"html.parser")

        table=soup.find("div",id="contest-table-upcoming")
        if table:
            rows=table.find_all("tr")[1:]
            for r in rows:
                tds=r.find_all("td")
                start=parser.parse(tds[0].text.strip()).astimezone(TZ)
                name=tds[1].text.strip()
                out.append((name,start,"https://atcoder.jp"))
    except:
        print("AtCoder fetch failed")

    return out

def make_ics(contests):
    text="BEGIN:VCALENDAR\nVERSION:2.0\n"

    for name,start,url in contests:
        end=start+datetime.timedelta(hours=2)

        text+="BEGIN:VEVENT\n"
        text+=f"DTSTART;TZID=Asia/Kolkata:{start.strftime('%Y%m%dT%H%M%S')}\n"
        text+=f"DTEND;TZID=Asia/Kolkata:{end.strftime('%Y%m%dT%H%M%S')}\n"
        text+=f"SUMMARY:{name}\n"
        text+=f"DESCRIPTION:{url}\n"
        text+="END:VEVENT\n"

    text+="END:VCALENDAR"

    with open("contests.ics","w",encoding="utf-8") as f:
        f.write(text)

if __name__=="__main__":
    contests=fetch_all()
    make_ics(contests)
