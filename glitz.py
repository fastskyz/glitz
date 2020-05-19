import json, os, re
from os import chmod
from Crypto.PublicKey import RSA


class Glitz():
    def __init__(self):
        #if os.geteuid() != 0:
            #print("Please run Glitz with root permissions.")

        self.ssh_path = os.path.expanduser('~/.ssh')
        self.config_path = self.ssh_path + '/glitz.conf'
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.loads(f.read())

        self.active_account = self.getActiveAccount()

    def accounts(self):
        return self.config['accounts'].items()

    def saveConfig(self):
        with open(self.config_path, 'w+') as f:
            f.write(json.dumps(self.config))

    def setup(self):
        print("Welcome to Glitz!\nLet's get you setup.")
        self.config = {'accounts': {}}
        print("We'll start with adding the first ssh keys.")
        self.addAccount()
        print('Great, your first account is added!\nIf you want to add more or activate one, you can do so in the menu.')


    def addToAgent(self, name):
        os.system('eval "$(ssh-agent -s)"')
        os.system('ssh-add {base}/{name}.key'.format(base=self.ssh_path, name=name))

    def generateKeypair(self, name):
        file_path = '{base}/{name}.key'.format(name=name, base=self.ssh_path)
        key = RSA.generate(2048)
        with open(file_path, 'wb') as content_file:
            chmod(file_path, 600)
            content_file.write(key.exportKey('PEM'))

        file_path = '{base}/{name}.pub'.format(name=name, base=self.ssh_path)
        pubkey = key.publickey()
        with open(file_path, 'wb') as content_file:
            content_file.write(pubkey.exportKey('OpenSSH'))

    def addAccountToGitConfig(self, name, platform):
        f_name = '{base}config_b'.format(base=self.ssh_path)
        config_data = "\n\n#Added by Glitz, #{name}-Glitz \nHost {platform}-{name} #{name}-Glitz\n\tHostName {platform} #{name}-Glitz\n\tUser git #{name}-Glitz\n\tIdentityFile {base}/{name}.key #{name}-Glitz".format(name=name, platform=platform, base=self.ssh_path)
        if os.path.exists(f_name):
            with open(f_name, 'a+') as f:
                f.write(config_data)
        else:
            with open(f_name, 'w+') as f:
                f.write(config_data)

    def checkConnection(self, name, platform):
        os.system('ssh -T git@{platform}-{name}')

    def addAccount(self):
        #email = input('The email you want to use: ')
        name = input('An easy to remember name for this account: ')
        platform = 'github.com'
        self.generateKeypair(name)
        os.system('pbcopy < {name}.pub'.format(name=name))
        print('SSH Key generated and copied. Add it to the desired git account now.')
        input('Press enter when you are done.')
        #self.addToAgent(name)
        self.addAccountToGitConfig(name, platform)
        print('Added to git config file')
        #self.checkConnection(name, platform)
        
        # save data in config file
        self.config['accounts'][name] = {'platform': platform}
        self.saveConfig()

    def getActiveAccount(self):
        conf_f_name = '{base}/config_b'.format(base=self.ssh_path)

        with open(conf_f_name, "r") as f:
            lines = f.readlines()

        for line in lines:
            if '###' in line:
                name = re.search('###(.*)-Glitz', line)
                return name.group()
                

    def switchAccount(self, name):
        conf_f_name = '{base}/config_b'.format(base=self.ssh_path)

        with open(conf_f_name, "r") as f:
            lines = f.readlines()
        with open(conf_f_name, "w") as f:
            for line in lines:
                if "###" in line:
                    active_name = re.search('###(.*)-Glitz', line)
                    f.write(f"Host github.com-{active_name} #{active_name}-Glitz")
                elif f"Host github.com-{name} #{name}-Glitz" not in line.strip("\n"):
                    f.write(line)
                else:
                    f.write(f"Host github.com ###{name}-Glitz")

    def removeAccount(self):
        print('Your current git accounts created by Glitz are:')
        for name, acc in self.config['accounts'].items():
            print(f"- {name}")
        name = input('\nName of the account you want to remove: ')

        if name in self.config['accounts']:
            confirm = input('Are you sure? y/N\n')
            if confirm == 'y':
                secret_f = '{base}/{name}.key'.format(base=self.ssh_path, name=name)
                public_f = '{base}/{name}.pub'.format(base=self.ssh_path, name=name)
                files = [secret_f, public_f]
                
                for fn in files:
                   os.remove(fn)
            
                conf_f_name = '{base}/config_b'.format(base=self.ssh_path)

                with open(conf_f_name, "r") as f:
                    lines = f.readlines()
                with open(conf_f_name, "w") as f:
                    for line in lines:
                        if f"#{name}-Glitz" not in line.strip("\n"):
                            f.write(line)

                del self.config['accounts'][name]
                self.saveConfig()
                
                print(f'Removed {name}!')

        else:
            print('That is not a valid account name!')
            self.removeAccount()

        return
