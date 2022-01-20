from os import environ
from pywtdlib.client import Client
from pywtdlib.enum import Update
import logging

# (optional) set some logging to see what is happening under the hood
logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s [%(filename)s:%(lineno)d]|%(levelname)s|%(message)s",
)

# 1. instantiate the telegram client (put your API_ID and API_HASH from https://my.telegram.org/apps)
tg = Client(api_id=environ["API_ID"], api_hash=environ["API_HASH"])

# 2. define an update handler (every time an update is received, it will execute it)
# this will print in console every new message received
def print_messages(event):
    if event["@type"] == Update.NEW_MESSAGE:
        print(event)


# 3. add the update handler
tg.set_update_handler(print_messages)

# 4. start the client (press CTRL + C to stop)
tg.start()
