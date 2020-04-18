# Miku Bot

[![Build Status](https://travis-ci.com/kadahlin/MikuBot.svg?branch=master)](https://travis-ci.com/kadahlin/MikuBot)

Twitch bot with some basic flavored commands.

## How to run and test

#### To run
MikuBot needs two things completed in order to run successfully:

1. [Configure][1] your local aws-cli with your access key and secret key
2. Set the `mikubotPass` and `mikubotNick` environment variables with your twitch credentials.

After both steps are completed simply run `python3 miku/mikubot.py` to connect to Twitch
and send commands. An optional `debug` flag can be given to this command to see additional logs while developing.

#### To tests

Make sure `pytest` is installed and from the root directory run `pytest tests`





[1]: https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration
