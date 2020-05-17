import rumps
from glitz import Glitz
from functools import partial

class GlitzApp(object):
    def __init__(self):
        rumps.debug_mode(False)
        self.glitz = Glitz()
        self.config = {
            "app_name": "Glitz",
        }
        self.app = rumps.App(self.config["app_name"])

        self.app.menu = ["Switch git account"]

    @rumps.clicked("Switch git account")
    def switch(self):
        rumps.notification(title="Almost available!", subtitle="This is coming soon!", message="Hello this is a long message!")

    def run(self):
        self.app.run()

if __name__ == '__main__':
    app = GlitzApp()
    app.run()