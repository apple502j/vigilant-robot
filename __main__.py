if __name__ == "__main__":
    import argparse
    import mw_api_client as mwc
    import bot
    from _secret import USERNAME, PASSWORD

    wiki = mwc.Wiki("https://ja.scratch-wiki.info/w/api.php", "Apple Bot")
    wiki.login(USERNAME, PASSWORD)
    my_bot = bot.Bot(wiki)
    running = []

    parser = argparse.ArgumentParser(description='Run the bot.')
    parser.add_argument(
        '--disable', nargs='*', metavar='feature',
        help='disable bot feature(s)'
    )
    cmdargs = parser.parse_args()

    if 'news' not in cmdargs.disable:
        from news_update import NewsUpdateBot
        running.append(NewsUpdateBot)

    my_bot.run(*running)
