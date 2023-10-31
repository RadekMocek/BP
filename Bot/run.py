from modules.bot import LingeBot, TOKEN

if __name__ == "__main__":
    bot = LingeBot()
    bot.run(token=TOKEN, reconnect=True)
