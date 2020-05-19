import rumps
from glitz import Glitz
from functools import partial

class GlitzApp(rumps.App):
    def __init__(self):
        rumps.debug_mode(True)
        self.glitz = Glitz()

        self.config = {
            "app_name": "Glitz",
            "app_icon": "icons/app.png",
            "switch_icon": "icons/switch.png"
        }
    
        active_account = self.glitz.active_account if self.glitz.active_account != None else "No account active"

        menu = [
            rumps.MenuItem(title="app", template=True, callback=None),
            rumps.MenuItem(title="Switch", icon=self.config["switch_icon"], dimensions=(16, 16), template=True)
        ]

        super(GlitzApp, self).__init__(name=self.config["app_name"], icon=self.config["app_icon"], template=True, menu=menu)

    @rumps.clicked("Switch")
    def switch(self, sender):
        for name, acc in self.glitz.accounts():
            if name != self.glitz.active_account:
                rumps.notification(title="Switched!", subtitle=None, message=f"Switched to git account {name}!")

    def menu(self):
        while True:
            print('1:\tAdd account\n2:\tRemove account\n0:\tExit')
            choice = input('> ')
            if choice == '1':
                self.glitz.addAccount()
            elif choice == '2':
                self.glitz.removeAccount()
            elif choice == '3':
                input('Hi there code explorer! This option is coming soon!\n')
                #self.activateAccount()
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                input('Please enter number from the list above.\n')


if __name__ == '__main__':
    GlitzApp().run()