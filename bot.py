import requests, datetime, pytz
from dateutil import parser

TZ=pytz.timezone("Asia/Kolkata")

def fetch_all():
    out=[]

    # Codeforces
    cf=requests.get("https://codeforces.com/api/contest.list").json()["result"]
    for c in cf:
        if c["phase"]=="BEFORE":
            start=datetime.datetime.fromtimestamp(c["startTimeSeconds"],pytz.utc).astimezone(TZ)
            out.append((c["name"],start,"https://codeforces.com"))

    # LeetCode
    lc=requests.get("https://leetcode.com/contest/api/list/").json()["contests"]
    for c in lc:
        start=datetime.datetime.fromtimestamp(c["start_time"],pytz.utc).astimezone(TZ)
        if start>datetime.datetime.now(TZ):
            out.append((c["title"],start,"https://leetcode.com"))

    # CodeChef
    cc=requests.get("https://www.codechef.com/api/list/contests/all").json()
    for c in cc.get("future_contests",[]):
        start=parser.parse(c["contest_start_date"]).astimezone(TZ)
        out.append((c["contest_name"],start,"https://codechef.com"))

    return out

def make_ics(contests):
    text="BEGIN:VCALENDAR\nVERSION:2.0\n"

    for name,start,url in contests:
        end=start+datetime.timedelta(hours=2)

        text+="BEGIN:VEVENT\n"
        text+=f"DTSTART:{start.strftime('%Y%m%dT%H%M%S')}\n"
        text+=f"DTEND:{end.strftime('%Y%m%dT%H%M%S')}\n"
        text+=f"SUMMARY:{name}\n"
        text+=f"DESCRIPTION:{url}\n"
        text+="END:VEVENT\n"

    text+="END:VCALENDAR"

    with open("contests.ics","w",encoding="utf-8") as f:
        f.write(text)

if __name__=="__main__":
    contests=fetch_all()
    make_ics(contests)
