import praw
import pprint

reddit = praw.Reddit(client_id="DEnzCMrEAr23eg",
                      client_secret="13m_HnyitkdNrqlxbxRwUtVgajU",
                      redirect_uri="http://localhost:8080",
                      user_agent="Floria_bot by /u/websinthe")
#print(reddit.auth.url(["read, identity, account, history"], "discord_bot", "permanent"))

refresh_code = "5511418-0TtgsCqKUIeQaPngHBlHbPfqPWY"

#print(reddit.auth.authorize(code))
print(reddit.user.me())

subreddit = reddit.subreddit("aww")

aww_list = subreddit.hot(limit=10)

cute_list = []

for submission in aww_list:
    try:
        cute_mid = submission.secure_media["reddit_video"]
        cute_pic = cute_mid["fallback_url"]
    except:    
        cute_pic = submission.url
    print(cute_pic)
    cute_list.append(cute_pic)
    last_id = submission.id

