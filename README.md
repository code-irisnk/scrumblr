# Scrumblr

Scrumblr is a free and straightforward Last.fm to Tumblr integration tool. It allows you to seamlessly share your recently scrobbled tracks on Last.fm with your Tumblr audience. This tool is designed to be easy to set up and runs on Python.

## Setup

### Prerequisites

Ensure that you have Python installed on your system. If not, you can download it from [python.org](https://www.python.org/downloads/).

### Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/code-irisnk/scrumblr.git
```


Navigate to the project directory:

```bash
cd ApplePye
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

[Create a Last.fm API account](https://www.last.fm/api/account/create) and obtain your API key, API secret, username, and password hash.
[Register a Tumblr API app](https://www.tumblr.com/oauth/register) and obtain your API key, API secret, consumer key, consumer secret and side-blog name.
Edit the file named auth.json keeping the following structure:

```json
{
    "lastfm-API_KEY": "",
    "lastfm-API_SECRET": "",
    "lastfm-username":"",
    "lastfm-passhash":"",


    "tumblr-consumer_key": "",
    "tumblr-consumer_secret": "",
    "tumblr-oauth_token": "",
    "tumblr-oauth_secret":"",
    "tumblr-blogname":""
}
```

Replace the placeholders with your actual Last.fm and Tumblr API credentials.
To get the hashed equivalent of your LastFM password, run

```bash
python hasher.py
```

It should look something like this: `93eb3a355cfad1472e4b59a594159e12`

## Usage

Run the bot using the following command:

```bash
python main.py
```

The bot will continuously monitor your Last.fm scrobbles and automatically post them to your specified Tumblr blog.


## Notes
Ensure that Last.fm is actively scrobbling your tracks.
If you scrobble more than 300 tracks a day, Tumblr might rate limit you.


## Contributing
If you'd like to contribute to Scrumblr, please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes and commit them.
- Submit a pull request.
