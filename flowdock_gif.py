#! /usr/bin/python3

import sys
import requests
import argparse
from pathlib import Path
from dotenv import dotenv_values

# Load conf
config = dotenv_values(f"{Path(__file__).parent.absolute()}/.env")

# Parse arguments
parser = argparse.ArgumentParser()
requiredNamed = parser.add_argument_group("required named arguments")
requiredNamed.add_argument(
    "-u", "--user", help="Flowdock user recipient id", type=int, required=True
)
parser.add_argument(
    "-t", "--tag", help="Giphy tag for the random search", type=str, default="unicorn"
)
args = parser.parse_args()

# Get a random gif
gif_r = requests.get(
    "https://api.giphy.com/v1/gifs/random",
    params={"tag": args.tag, "api_key": config["GIPHY_API_KEY"], "rating": "pg-13"},
)

if gif_r_dict := gif_r.json()["data"]:
    gif_url = gif_r_dict["images"]["original"]["url"].split("?")[0]
    print(f"Sending {gif_url} gif.")
    requests.post(
        f"https://api.flowdock.com/private/{args.user}/messages",
        auth=(config["FLOWDOCK_API_TOKEN"], ""),
        json={"event": "message", "content": f"/giphy {args.tag} \n{gif_url}"},
    )
else:
    print(f"No gif found for '{args.tag}'.", file=sys.stderr)
    sys.exit(1)
