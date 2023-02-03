import time
import sys
import logging
import json
import requests
import pylast
import pytumblr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# first, get the lastfm api key and secret from the keys.json file
with open('keys.json') as f:
    keys = json.load(f)

lastfm_api_key = keys['lastfm-API_KEY']
lastfm_api_secret = keys['lastfm-API_SECRET']

# get lastfm username and password from the keys.json file
lastfm_username = keys['lastfm-username']
lastfm_password = keys['lastfm-password']

# do lastfm authentication

password_hash = pylast.md5(keys['lastfm-password'])
network = pylast.LastFMNetwork(
    api_key=lastfm_api_key,
    api_secret=lastfm_api_secret,
    username=lastfm_username,
    password_hash=password_hash,
)

user = network.get_user(lastfm_username)
print("LastFM Authenticated!")

# get the tumblr api key and secret from the keys.json file
tumblr_consumer_key = keys['tumblr-consumer_key']
tumblr_consumer_secret = keys['tumblr-consumer_secret']

# get the tumblr oauth token and secret from the keys.json file
tumblr_oauth_token = keys['tumblr-oauth_token']
tumblr_oauth_secret = keys['tumblr-oauth_secret']

tumblr_blogname = keys['tumblr-blogname']

# do tumblr authentication
client = pytumblr.TumblrRestClient(
    tumblr_consumer_key,
    tumblr_consumer_secret,
    tumblr_oauth_token,
    tumblr_oauth_secret
)

# post hello world to tumblr with current unix time
client.create_text(tumblr_blogname, state="published", tags=["mmmm im a bot :3c"], title="Hello World!", body="I am now online! \nat UNIX_time=[" + str(int(time.time())) + "]")

def justBlogIt(latestScrobble,client,latestScrobbleTime,tumblr_blogname):
        songName = latestScrobble.track.title
        songArtist = latestScrobble.track.artist.name
        try:
                songGenre = latestScrobble.track.get_top_tags(limit=1)[0].item.name
                songGenre2 = latestScrobble.track.get_top_tags(limit=2)[1].item.name
                songGenre3 = latestScrobble.track.get_top_tags(limit=3)[2].item.name
                
        except:
                songGenre = "aasfgfglhkf a;lsdkfj qwq"
                songGenre2 = "we have no tags"
                songGenre3 = "we're sorry"
        
        #try:
        #    songAlbum = latestScrobble.album.title
        #except:
        #    songAlbum = "unknown"
        client.create_text(tumblr_blogname, 
                           state="published", 
                           tags=[str(songGenre),str(songGenre2),str(songGenre3)], 
                           title=str("\"" + songName + "\"" + "\nby " + songArtist), 
                           body=str("\n from "#+ str(songAlbum) 
                                    + "\nat UNIX_time=[" + str(latestScrobbleTime) + "]"))
        logger.info("Posted current song!") 

def loopMeUp(client, user):
    
    # cache the latest scrobble
    # unfortunately this makes us lose the first scrobble from every startup
    cachedScrobble = user.get_recent_tracks(limit=1)[0]
    cachedScrobbleTime = cachedScrobble.timestamp
    cachedScrobbleTime = int(cachedScrobbleTime)
    
    # wait 10 seconds
    time.sleep(10)
    
    # get the latest scrobble
    latestScrobble = user.get_recent_tracks(limit=1)[0]
    latestScrobbleTime = latestScrobble.timestamp
    latestScrobbleTime = int(latestScrobbleTime)
    sessionAlive = False

    
    # this code does the following:
    # if user != listening && sessionAlive == True, post status & sessionAlive = False
    # if user == listening, post status & sessionAlive = True
    if ((user.get_now_playing() == None) & (sessionAlive == True)):
        sessionAlive = False
        justBlogIt(latestScrobble,client,latestScrobbleTime,tumblr_blogname)
    else:
        if (latestScrobbleTime != cachedScrobbleTime):
            sessionAlive = True
            justBlogIt(latestScrobble,client,latestScrobbleTime,tumblr_blogname)
    
while True:
    loopMeUp(client, user)