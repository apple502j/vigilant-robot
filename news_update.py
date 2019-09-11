import datetime, time, re
from featured_handler import featured_japan

class NewsUpdateBot(object):
    NOINCLUDE_REGEX = re.compile(r"\n;(\d{1,2}月\d{1,2}日)\n:(.+)\n<noinclude>")
    NOINCLUDE_RERL  = "\n<noinclude>\n;\g<1>\n:\g<2>"
    NOTE = "<!-- 追加時はこのページのどこかにあるnoincludeタグを1項目上にずらしてください -->"

    def __init__(self, bot):
        self.bot = bot
        self.wiki = bot.wiki

    def replace_noinclude(self, string):
        return self.NOINCLUDE_REGEX.sub(self.NOINCLUDE_RERL, string)

    @staticmethod
    def date():
        now = datetime.datetime.now()
        return f"{now.month}月{now.day}日"

    def format_items(self, items, original):
        text = f";{self.date()}\n"
        count = 0
        for key, title, pid, user in items:
            if str(pid) in original:
                continue # already put
            count += 1
            kind = {
                "community_featured_projects":"注目のプロジェクト",
                "community_most_loved_projects":"コミュニティが好きなもの",
                "community_most_remixed_projects":"コミュニティで現在リミックスされているもの"
            }[key]
            text += ":{{@|" + user + "}}" + f"さんの[[scratch:projects/{pid}|{title}]]が、[[{kind}]]に選ばれました。\n"
        if count:
            return text, count
        return "", 0

    def run(self):
        featureds = featured_japan()
        page = self.wiki.page("メインページ/ニュース")
        content = page.read()
        addition, added = self.format_items(featureds, content)
        if added:
            content = content.replace(self.NOTE + "\n", self.NOTE + "\n" + addition)
            for i in range(added):
                content = self.replace_noinclude(content)
            page.edit(content, f"ニュースの更新: {added}件追加 (bot)")
            time.sleep(10)
