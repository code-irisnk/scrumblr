import time
import sys
import logging
import json
import requests
import pylast
import pytumblr

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load API keys and credentials from keys.json
with open('keys.json') as f:
    keys = json.load(f)

# Last.fm API key and secret
lastfm_api_key = keys['lastfm-API_KEY']
lastfm_api_secret = keys['lastfm-API_SECRET']
lastfm_username = keys['lastfm-username']
lastfm_passhash = keys['lastfm-passhash']

# Authenticate with Last.fm
password_hash = pylast.md5(keys['lastfm-password'])
network = pylast.LastFMNetwork(
    api_key=lastfm_api_key,
    api_secret=lastfm_api_secret,
    username=lastfm_username,
    password_hash=password_hash,
)

user = network.get_user(lastfm_username)
print("LastFM Authenticated!")

# Load Tumblr credentials from keys.json
tumblr_consumer_key = keys['tumblr-consumer_key']
tumblr_consumer_secret = keys['tumblr-consumer_secret']
tumblr_oauth_token = keys['tumblr-oauth_token']
tumblr_oauth_secret = keys['tumblr-oauth_secret']
tumblr_blogname = keys['tumblr-blogname']

# Authenticate with Tumblr
client = pytumblr.TumblrRestClient(
    tumblr_consumer_key,
    tumblr_consumer_secret,
    tumblr_oauth_token,
    tumblr_oauth_secret
)

# Post "Hello World!" to Tumblr with current UNIX time
client.create_text(tumblr_blogname, state="published", tags=["mmmm im a bot :3c"], title="Hello World!",
                   body="I am now online! \nat UNIX_time=[" + str(int(time.time())) + "]")

def justBlogIt(latestScrobble, client, latestScrobbleTime, tumblr_blogname):
    """
    Posts the information of the latest scrobble to Tumblr.

    Parameters:
    - latestScrobble: The latest scrobble information.
    - client: The Tumblr client for posting.
    - latestScrobbleTime: The timestamp of the latest scrobble.
    - tumblr_blogname: The Tumblr blog where the information will be posted.
    """
    # Extract song information
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

    # Post song information to Tumblr
    client.create_text(tumblr_blogname,
                       state="published",
                       tags=[str(songGenre), str(songGenre2), str(songGenre3)],
                       title=str("\"" + songName + "\"" + "\nby " + songArtist),
                       body=str("\n from "
                                # + str(songAlbum)
                                + "\nat UNIX_time=[" + str(latestScrobbleTime) + "]"))
    logger.info("Posted current song!")

def loopMeUp(client, user):
    """
    The main loop that continuously checks for the latest scrobble and posts it to Tumblr.

    Parameters:
    - client: The Tumblr client for posting.
    - user: The Last.fm user for getting scrobble information.
    """
    # Cache the latest scrobble
    cachedScrobble = user.get_recent_tracks(limit=1)[0]
    cachedScrobbleTime = cachedScrobble.timestamp
    cachedScrobbleTime = int(cachedScrobbleTime)

    # Wait for 10 seconds
    time.sleep(10)

    # Get the latest scrobble
    latestScrobble = user.get_recent_tracks(limit=1)[0]
    latestScrobbleTime = latestScrobble.timestamp
    latestScrobbleTime = int(latestScrobbleTime)
    sessionAlive = False

    # Check if user is not listening and the session is still alive
    if ((user.get_now_playing() is None) and (sessionAlive is True)):
        sessionAlive = False
        justBlogIt(latestScrobble, client, latestScrobbleTime, tumblr_blogname)
    else:
        # Check if the latest scrobble time is different from the cached scrobble time
        if (latestScrobbleTime != cachedScrobbleTime):
            sessionAlive = True
            justBlogIt(latestScrobble, client, latestScrobbleTime, tumblr_blogname)

while True:
    loopMeUp(client, user)
