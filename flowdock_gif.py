#! /usr/bin/python3

import json
import requests
import argparse
from dotenv import dotenv_values

# Load conf
config = dotenv_values(".env")

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
        "api_key": config['GIPHY_API_KEY']
    }
)

# Send the gif
requests.post(
    "https://api.flowdock.com/private/{}/messages".format(args.user),
    auth = (config['FLOWDOCK_API_TOKEN'], ''),
    json = {
        "event": "message",
        "content": json.loads(gif_r.text)['data']['image_url']
    }
)
