#Welcome to the MYLogin project.
import MY_LOGIN

import json
import os
import datetime

try:
        from cryptography.fernet import Fernet

except ImportError:

        print("\033[31m", end = "")
        print("fatal: cryptography module is not currently installed. for more details, see installation folder")
        print("\033[31m", end = "")
        exit(0)


user_info = str(os.getcwd()) + "/.data/.user.json"
data_name = str(os.getcwd()) + "/.data/data.json"
log_path = str(os.getcwd()) + "/logs"
backups_path = str(os.getcwd()) + "/backups"

changelist = ["access at " + str(datetime.datetime.now())]

if not os.path.exists(user_info):

        print("\033[31m", end = "")
        print("fatal: data folder does not exist or cannot be located")
        print("\033[30m", end = "")
        exit(0)


if not os.path.exists("MY_LOGIN.py"):

        print("\033[31m", end = "")
        print("fatal: MY_LOGIN module does not exist or cannot be located")
        print("\033[30m", end = "")
        exit(0)

try:

        with open(data_name) as log_open:

                temp = json.load(log_open)
                log_flag = temp['LOGS']

except:

    print("\033[31m", end = "")
    print("fatal: invalid JSON format (data.json). terminated")
    print("\033[0m", end = "")
    exit()


# MAIN

values = MY_LOGIN.configure_user(user_info)
MY_LOGIN.configure_data(data_name, backups_path)

my_username = values[0]
my_key = values[1].encode('utf-8')
my_cipher = Fernet(my_key)

print("<STARTING> MYLogin 1.1")

MY_LOGIN.menu()

while True:

        user_input = input(f"\033[32m" + my_username + ":~$ \033[0m")

        if len(user_input.split()) == 1:

                user_input = user_input.replace(' ', '')

        match user_input:

                case "home":
                        MY_LOGIN.menu()
                        
                case "help":
                        MY_LOGIN.help()
                        
                case "ls":
                        MY_LOGIN.display(data_name, my_cipher)
                        
                case "fetch":
                        MY_LOGIN.search(data_name, my_cipher)

                case "fetch-all":
                        MY_LOGIN.search_all(data_name, my_cipher)
                        
                case "new":
                        MY_LOGIN.create(data_name, my_cipher, changelist)
                        
                case "rm":
                        MY_LOGIN.remove(data_name, my_cipher, changelist)

                case "edit":
                        MY_LOGIN.edit_password(data_name, my_cipher, changelist)

                case "edit-username":
                        MY_LOGIN.edit_username(data_name, my_cipher, changelist)
                    
                case "edit-password":
                        MY_LOGIN.edit_password(data_name, my_cipher, changelist)

                case "edit-url":
                        MY_LOGIN.edit_url(data_name, my_cipher, changelist)
                        
                case "kill-all":
                        MY_LOGIN.reset(data_name, changelist)

                case "backup":
                        MY_LOGIN.backup(data_name, changelist)

                case "restore":
                        MY_LOGIN.restore(data_name, changelist)

                case "enable":
                        MY_LOGIN.enable(data_name)

                case "disable":
                        MY_LOGIN.disable(data_name)

                case "default":
                        MY_LOGIN.default(data_name, user_info)

                case "version":
                        MY_LOGIN.info()

                case "clear":
                        MY_LOGIN.clear()

                case "cls":
                        MY_LOGIN.clear()

                case "whoami":
                        MY_LOGIN.whoami()
                        
                case "exit":
                        break
                case _:
                        MY_LOGIN.check_argument(data_name, user_input, my_cipher, changelist)


with open (data_name) as log_flag:

        f = json.load(log_flag)

if(f['LOGS'] == "T" and os.path.exists(log_path)):

        log = open(log_path + "/Log " + str(datetime.datetime.now()) + ".txt", 'a')
    
        for i in range(0, len(changelist)):

                log.write(changelist[i])
        
        log.write("\nterminated use at " + str(datetime.datetime.now()))

        log.close()


print("terminated use at " + str(datetime.datetime.now()))
