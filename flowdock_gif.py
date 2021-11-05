#! /usr/bin/python3

import sys
import json
import requests
import argparse
from pathlib import Path
from dotenv import dotenv_values

# Load conf
config = dotenv_values("{}/.env".format(Path(__file__).parent.absolute()))

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--user", help="Flowdock user recipient id", type=int, required=True)
parser.add_argument("-t", "--tag", help="Giphy tag for the random search", type=str, default="unicorn")
args = parser.parse_args()

# Get a random gif
gif_r = requests.get(
    'https://api.giphy.com/v1/gifs/random',
    params = {
        "tag": args.tag,
        "api_key": config['GIPHY_API_KEY'],
        "rating": "pg-13"
    }
)

gif_r_dict = json.loads(gif_r.text)

if gif_r_dict['data']:
    gif_url = gif_r_dict['data']['images']['original']['url'].split('?')[0]
    print("Sending '{}' gif.".format(gif_url))
    requests.post(
       "https://api.flowdock.com/private/{}/messages".format(args.user),
       auth = (config['FLOWDOCK_API_TOKEN'], ''),
       json = {
           "event": "message",
           "content": "/giphy " + args.tag + "\n" + gif_url
       }
    )
else:
    print("No gif found for '{}'.".format(args.tag), file=sys.stderr)
    sys.exit(1)
