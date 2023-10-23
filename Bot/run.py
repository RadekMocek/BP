from modules.bot import DisGebra, TOKEN

if __name__ == "__main__":
    bot = DisGebra()
    bot.run(token=TOKEN, reconnect=True)
