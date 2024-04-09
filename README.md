# @anekdot_megabot
The telegram bot parses a website with jokes and provides a random joke. Bot users can like/dislike jokes. Implemented a database where downloaded jokes will be added (to avoid redundant requests to the website) along with the number of likes/dislikes for a specific joke. The bot operates around the clock on a remote server.

# Installation locally:
```bash
cd <folder_where_to_clone>
git clone git@github.com:ganjubas2008/megabot-anekdot.git .
echo <your_token> > src/config.py
pip install requirements.txt
chmod +x run.sh
./run.sh
```
It is recommended to change the token in the config.py file here, as if two bots are launched on two machines with the same token, they will both crash.
 If it doesn't start locally on the first try, you may need to try a couple more times.

# Interaction:
Open Telegram, write @anekdot_megabot, then the command /help will help. If the buttons disappear, you can write /start to the bot again.


![plot](./images/bot.png)
