from datetime import datetime, timedelta
import os
from plurk_oauth import PlurkAPI
import pytz

execute_gap = os.environ.get("EXECUTE_GAP", 5)

api_key = os.environ.get("API_KEY")
api_secret = os.environ.get("API_SECRET")
access_key = os.environ.get("TOKEN_KEY")
access_secret = os.environ.get("TOKEN_SECRET")

friend_dict = {}
headers = {"x-api-key": "{$$.env.x-api-key}"}
plurkAPI = PlurkAPI(api_key, api_secret)
plurkAPI.authorize(access_key, access_secret)


def getGMTNow():
    # get the current time in UTC
    utc_now = datetime.utcnow()

    # convert to GMT timezone
    gmt = pytz.timezone("GMT")
    gmt_now = gmt.localize(utc_now)

    return gmt_now


def addAndGetFriends():
    plurkAPI.callAPI("/APP/Alerts/addAllAsFriends")
    setFriendList()


def setFriendList():
    try:
        data = plurkAPI.callAPI("/APP/FriendsFans/getCompletion")
        if data is not None:
            for user in data:
                if not user in friend_dict:
                    friend_dict[user] = data[user]["display_name"]
    except Exception as e:
        print(f"setFriendList err: {e}")


def getNeedReplyCount():
    unreadRes = plurkAPI.callAPI("/APP/Polling/getUnreadCount")
    return unreadRes.get("all", 0) - unreadRes.get("responded", 0)


def addResponse(pid, content):
    plurkAPI.callAPI(
        "/APP/Responses/responseAdd",
        {"plurk_id": pid, "content": content, "qualifier": ":"},
    )


def dealContent(pid, content, isCmd, pu, user_id):
    print(f"reply plurk id:{pid} content:{content} pu: {pu}")
    addResponse(pid, "[emo1]")


def handlePlurks(now: datetime):
    offset = now - timedelta(minutes=int(execute_gap))

    plurks = plurkAPI.callAPI(
        "/APP/Polling/getPlurks",
        {"offset": offset.strftime("%Y-%m-%dT%H:%M:%S"), "limit": 100},
    ).get("plurks", [])

    for plurk in plurks:
        pid = plurk.get("plurk_id")
        user_id = plurk.get("owner_id")
        if str(user_id) not in friend_dict:
            print("Not in friend list.")
            continue
        if plurk.get("is_unread") != 1:
            continue
        if plurk.get("responed") == 1:
            continue

        content = plurk.get("content_raw")
        print(f"reply to {friend_dict[str(user_id)]}, content:{content}")
        addResponse(pid, "[emo1]")


def main():
    now = getGMTNow()
    print(f"Starting bot at {now.strftime('%Y-%m-%d %H:%M:%S GMT')}")

    addAndGetFriends()

    count = getNeedReplyCount()
    if count > 0:
        handlePlurks(now)
    else:
        print("No new plurks to reply.")

    print(f"Ending bot at {now.strftime('%Y-%m-%d %H:%M:%S GMT')}")


if __name__ == "__main__":
    main()
