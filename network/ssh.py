from paramiko import SSHClient, AutoAddPolicy
from getpass import getpass


class SecureShell(object):
    def __init__(self, ip):
        self.IP = ip

    def connect(self):
        self.client = SSHClient()
        try:
            self.client.load_system_host_keys()
            self.client.load_host_keys('~/.ssh/known_hosts')
        except:
            self.client.set_missing_host_key_policy(AutoAddPolicy())
        user = input("Enter username :- ")
        passkey = getpass("Enter password :- ")
        self.client.connect(self.IP, username=user, password=passkey)

    def commands(self):
        while True:
            cmd = input("Enter your command :- ")
            if cmd == "logout":
                self.client.close()

            else:
                stdin, stdout, stderr = self.client.exec_command(cmd)
                if len(stdout.read()) > 0:
                    print('STDOUT')
                    print(stdout.read().decode('utf-8'))
                elif len(stdin.read()) > 0:
                    print('STDIN')
                    sec_cmd = input(">> ")
                    stdin.write(sec_cmd)
                    print(stdout.read().decode('utf-8'))
                else:
                    print(stderr.read().decode('utf-8'))


# obj = SecureShell('192.168.1.120')
# obj.connect()
# obj.commands()
