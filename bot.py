class Bot(object):
    def __init__(self, wiki, **kwargs):
        self.wiki = wiki
        self.running = []
        self.kwargs = kwargs

    def run(self, *bots):
        for bot in bots:
            self.running.append(bot(self))

        for instance in self.running:
            instance.run()
