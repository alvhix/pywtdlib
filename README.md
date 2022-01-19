# Python Wrapper TDLib

### Description

A simple Python TDLib Wrapper (pywtdlib) that makes you easy to create new Python Telegram clients.

### Installation

1. By pip3

```python
pip3 install pywtdlib
```

### Setup

This project depends on [TDLib](https://github.com/tdlib/td). TDLib is the official cross-platform library for building Telegram clients written in C++.

##### Example:

This wrapper is so easy to use, for example the following code prints every new message that is received in your Telegram account.

```python
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
```

### Libraries

In the _lib/_ folder are located the binaries for Windows and Linux. If you need other binaries or you want to build by your own, go to the [TDLib build page](https://tdlib.github.io/td/build.html).

### Logs

Support for basic logging

### Issues

If you detect a [bug](.github/ISSUE_TEMPLATE/bug_report.md) or you have a [suggestion](.github/ISSUE_TEMPLATE/feature_request.md), open a ticket with the corresponding template.
