from modules.bot import DisGebra, TOKEN, PATH_IMG

if __name__ == "__main__":
    if not PATH_IMG.is_dir():
        PATH_IMG.mkdir()

    bot = DisGebra()
    bot.run(token=TOKEN, reconnect=True)
