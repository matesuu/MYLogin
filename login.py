#Welcome to the MYLogin project.

import os
import json
import datetime

user_info = str(os.getcwd()) + "/.data/user.json"
data_name = str(os.getcwd()) + "/.data/data.json"
log_path = str(os.getcwd()) + "/logs"

changelist = ["access at " + str(datetime.datetime.now())]

if not os.path.exists(user_info):

        print("\033[31m", end = "")
        print("fatal: data folder does not exist or cannot be located")
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

def clear() -> None: #clears console and checks to see what os is being used

        if os.name == 'nt': # windows
                
                os.system('cls')
                
        else: # mac/linux
                os.system('clear')


def default() -> None:

        default_input = input("default all data? (y/n) ")
        new_input = default_input.replace(" ", '')

        if new_input == 'n':

                print("process aborted")

        else:

                with open(user_info) as read_user:

                        default_user = json.load(read_user)

                        default_user['user'] = ""
                        default_user['connections'] = []
        
                        with open(user_info, 'w') as write_user:

                               json.dump(default_user, write_user, indent = 4)

                with open(data_name) as read_data:

                        default_data = json.load(read_data)

                        default_data['data_entries'] = []
                        default_data['backup_path'] = ""
                        default_data['date_created'] = ""
                        default_data['ID'] = "0"
                        default_data['LOGS'] = "F"

                        with open(data_name, 'w') as write_data:

                                json.dump(default_data, write_data, indent =4)

                print("defaulted to base settings. terminate")
                exit()

def configure_user() -> str:

        my_name = ""

        try:

            with open(user_info) as user_file:
                
                    this_user = json.load(user_file)

                    if this_user['user'] == "":

                            this_user['user'] = str(os.getlogin())
                            my_name = this_user['user']
                        
                    else:
                        
                            my_name = this_user['user']

                    with open(user_info, 'w') as temp:

                            json.dump(this_user, temp, indent=4)

        except:
                print("\033[31m", end = "")
                print("fatal: invalid JSON format (user.json). terminated")
                print("\033[0m", end = "")
                exit()

        return my_name

                

def configure_data() -> None: # gets username and path used for backups
        
        with open(data_name) as data_file:

                this_data = json.load(data_file)

                if this_data['backup_path'] == "":

                        cleaned_path = str(os.getcwd()) + "/backups"
                        this_data['backup_path'] = cleaned_path

                if this_data['date_created'] == "":

                        this_data['date_created'] = str(datetime.datetime.now())

                
                with open(data_name, 'w') as user_data:
                        
                        json.dump(this_data, user_data, indent=4)

def whoami() -> None:

        print(str(os.getlogin()))


def menu() -> None:
    
        icon()
        
        print("Welcome to MYLogin. This is a lightweight CLI tool intended to store user information with associated client login information. Enter 'help' to console to see the list of supported operations.\n")
        


def help() -> None:
        
        print("\nhome - returns to main menu")
        print("ls - displays all current clients as a list")
        print("fetch - returns all associated login information with a given client [shortcut -> fetch <client> fetches specified client]")
        print("new - creates a new client-information pair in dictionary - flags: Optional: [-all]")
        print("rm - removes a specified cient password pair from dictionary [shortcut -> rm <client> removes specified client]")
        print("edit - change a pre-existing information with an associated client - flags: [edit-username] [edit-password] [edit-url] default [edit-password] -> takes arguments")
        print("kill-all - deletes all currently existing client-password pairs held within data file")
        print("default - reset data folder and terminates execution prematurely - [DEV TOOL]")
        print("clear/cls - clear screen")
        print("backup - writes current data to a new backup to be stored in backups folder")
        print("restore - restores data from a given backup")
        print("enable - enables read logs")
        print("disable - disables read logs")
        print("version - displays version information")
        print("exit - terminate execution\n")


def info() -> None:
        
        print("MyLogin (Build 0)\nDate Started: 06/06/2024\nDate Finalized: 10/13/2024")
        print("Notes: Finished local build repository via JSON storage. Allows for Read-Write operations as well as version control options. Next will be encryption of data\n")
        print("Written by matesuu")


def display() -> None:
    
        with open(data_name) as outfile:
                clients = json.load(outfile)

        for client in clients['data_entries']:

                for names in client.values():

                        print("\033[34m", end = "")
                        print(names['client'])
                        print("\033[0m", end = "")

def search() -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ','')

        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        if cleaned_input == keys['client']:

                                print("\033[34m", end = "")
                                print("client ~ " + keys['client'])
                                print("username ~ " + keys['username'])
                                print("password ~ " + keys['password'])
                                print("url ~ " + keys['url'])
                                print("\033[0m", end = "")
                                flag = True
                                

        if flag == False:
            
                print("error: could not locate client")

        print("")
                

def search_arg(arg):

        user_input = arg
        cleaned_input = user_input.replace(' ','')

        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        if cleaned_input == keys['client']:

                                print("\033[34m", end = "")
                                print("client ~ " + keys['client'])
                                print("username ~ " + keys['username'])
                                print("password ~ " + keys['password'])
                                print("url ~ " + keys['url'])
                                print("\033[0m", end = "")
                                flag = True
                                

        if flag == False:
            
                print("error: could not locate client", end = "")

        print("")
                

def search_all() -> None:

        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        print("\033[34m", end = "")
                        print("\nclient ~ " + keys['client'])
                        print("username ~ " + keys['username'])
                        print("password ~ " + keys['password'])
                        print("url ~ " + keys['url'])
                        print("\033[0m", end = "")
        print("")


def create() -> None:
        

        flag = False

        with open(data_name) as check_file:
                check_data = json.load(check_file)
        
        new_client = input("client > ")
        cleaned_client = new_client.replace(' ', '')
        

        for entry in check_data['data_entries']:

                for i in entry.values():

                        if cleaned_client == i['client']:

                                flag = True

        if cleaned_client == '':

                flag = True

                
        if flag == False:

                new_username = input("username > ")
                new_password = input("password > ")
                new_url = input("url > ")

                cleaned_username = new_username.replace(' ','')
                cleaned_password = new_password.replace(' ','')
                
                new_entry = {"client" : cleaned_client, "username" : cleaned_username, "password" : cleaned_password, "url" : new_url}
                new_dict = {cleaned_client : new_entry}
        
                with open(data_name, 'r+') as outfile:
                        
                        outfile_data = json.load(outfile)
                        outfile_data['data_entries'].append(new_dict)
                        outfile.seek(0)
                        json.dump(outfile_data, outfile, indent=4)

                        changelist.append("\ncreated new client " + cleaned_client + " at " + str(datetime.datetime.now()))
                
        else:

                print("error: client already exists in directory")

def remove() -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ','')
        
        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

        for entry in curr_data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:

                                removed_value = i['client']
                                curr_data['data_entries'].remove(entry)
                                flag = True

                                changelist.append("\nremoved client " + i['client'] + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
                json.dump(curr_data, json_file, indent=4)
            
        
        if flag == False:
                print("error: could not locate client")

        
def remove_arg(arg) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')
        
        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

        for entry in curr_data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:

                                removed_value = i['client']
                                curr_data['data_entries'].remove(entry)
                                flag = True

                                changelist.append("\nremoved client " + i['client'] + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
                json.dump(curr_data, json_file, indent=4)
            
        
        if flag == False:
                print("error: could not locate client")



def edit_username() -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['username']
                                edited_value = i['client']
                                new_pass = input("username > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['username'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " username from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_username_arg(arg) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['username']
                                edited_value = i['client']
                                new_pass = input("username > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['username'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " username from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")
        
def edit_password() -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False


        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['password']
                                edited_value = i['client']
                                new_pass = input("password > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['password'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " password from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_password_arg(arg) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['password']
                                edited_value = i['client']
                                new_pass = input("password > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['password'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " password from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")

def edit_url() -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['url']
                                edited_value = i['client']
                                new_pass = input("url > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['url'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " URL from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_url_arg(arg) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                old = i['url']
                                edited_value = i['client']
                                new_pass = input("url > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['url'] = clean_pass
                                flag = True

                                changelist.append("\nedited " + i['client'] + " URL from " + old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def reset() -> None:
        
        user_input = input("delete all entries? (y/n) ")
        cleaned_input = user_input.replace(' ', '')
        flag = False

        with open(data_name) as outfile:

                data = json.load(outfile)

        if cleaned_input == 'y':

                for entry in data['data_entries']:

                        for i in entry.values():
                                data['data_entries'].clear()
                                flag = True
                                break
                        
        with open(data_name, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        
        if flag == True:
                
                print("deleted everything")
                changelist.append("\ndeleted all entries at " + str(datetime.datetime.now()))

        else:
                print("process aborted")


def backup() -> None:

        with open(data_name) as file: # opens data.json to read from file and store in dictionary 'data'

                data = json.load(file)
                

        new_id = int(data['ID'])      # stores the current backup ID in new_id
        new_id+=1                               # increments ID by 1
        data['ID'] = str(new_id)      # casts new_id to string
        

        with open(data_name, 'w') as update_id:       # opens data.json to write to file and dumps data, the only difference being 
                                                        # the incremented ID
                        
                json.dump(data, update_id, indent=4)

        

        path = data['backup_path']                      # gets path of backup folder

        if not os.path.exists(path):

                print('error: backups folder does not exist or cannot be located')
                return 

        data['date_created'] = str(datetime.datetime.now())     # stores the date of creation in 'date_created' as a string
        

        if os.path.exists(path +  str(new_id) + '.json'):

            new_json = open(path + '/backup(' + str(datetime.datetime.now()) + ').json', 'x').close()
            
            with open(path + 'backup(' + str(datetime.datetime.now()) + ').json', 'w') as json_file:

                json.dump(data, json_file, indent=4)

        else:
            
            new_json = open(path + '/backup(' + str(new_id) + ').json', 'x').close()
            
            with open(path + '/backup(' + str(new_id) + ').json', 'w') as json_file:

                json.dump(data, json_file, indent=4)
        
        changelist.append("\ndata backup at " + str(datetime.datetime.now()))

def restore() -> None:

        with open(data_name) as get_path:
            path_data = json.load(get_path)

            if not os.path.exists(path_data['backup_path']):

                print("error: backups folder does not exist or cannot be located")
                
                return 

        dir_list = os.listdir(path_data['backup_path'])

        print("\033[34m", end = "")
        print(dir_list)
        print("\033[0m", end = "")

        new_master = int(path_data['ID'])
        
        backup_file = input("restore with > ")

        #note: have to handle case where inputted string is not a valid file... try catch block maybe?

        try:
                with open(path_data['backup_path'] + '/' + backup_file) as json_file:
                        backup_data = json.load(json_file)
                        changelist.append("\nrestored data from " + backup_file + " at " + str(datetime.datetime.now()))
                        
                backup_data['ID'] = str(new_master)
                
                with open(data_name, 'w') as restored_file:
                        json.dump(backup_data, restored_file, indent=4)
                        
                print("restored from file")

        except:
                
                print("error: file error")


def restore_arg(arg) -> None:

        with open(data_name) as get_path:

                path_data = json.load(get_path)

                if not os.path.exists(path_data['backup_path']):

                        print("error: backups folder does not exist or cannot be located")
                
                        return 

        dir_list = os.listdir(path_data['backup_path'])
        new_master = int(path_data['ID'])
        backup_file = ""
        
        for i in range(1, len(arg)):

                backup_file = backup_file + arg[i]
        
        #note: have to handle case where inputted string is not a valid file... try catch block maybe?

        try:
                with open(path_data['backup_path'] + '/' + backup_file) as json_file:
                        backup_data = json.load(json_file)
                        changelist.append("\nrestored data from " + backup_file + " at " + str(datetime.datetime.now()))
                        
                backup_data['ID'] = str(new_master)
                
                with open(data_name, 'w') as restored_file:
                        json.dump(backup_data, restored_file, indent=4)
                        
                print("restored from file")

        except:
                
                print("error: file error")

        

def enable() -> None:

    with open(data_name) as enable_logs:

        e = json.load(enable_logs)

    e['LOGS'] = "T"
    
    with open(data_name, 'w') as finish_enable:

        json.dump(e, finish_enable, indent=4)
        

def disable() -> None:

    with open(data_name) as disable_logs:

        d = json.load(disable_logs)

    d['LOGS'] = "F"

    with open(data_name, 'w') as finish_disable:

        json.dump(d, finish_disable, indent=4)


def icon() -> None:


        print("\033[35m", end = "")
        print(r"""
                                                                                ---------------------------------------
                                                                                |                             _       |
                                                                                |  __  ___    ___            |+|      |                 
                                                                                | |  \/  \ \ / / |   ___ __ _ _ _ _   |
                                                                                | | |\/| |\ V /| |__| _ / _` | | '  \ |                      
                                                                                | |_|  |_| |_| |____|___\__, |_|_||_| |
                                                                                |                       |___/         |
                                                                                ---------------------------------------
        """)# prints icon

        print("\033[0m", end = "")

def check_argument(string) -> None:

        # valid: rm, fetch, restore, edit
        op = 0
        c = 0
        command = ""
        arg = ""
        cFlag = False

        for i in range(0, len(string)):
                
                if string[i] == " " and cFlag == False:  

                        continue

                elif string[i] == " " and cFlag == True:

                        break
                else:
                        cFlag = True
                        command = command + string[i]
                        c = c + 1

        for i in range(c, len(string)):

                arg = arg + string[i]

        arg.replace(' ', '')
        
        match command:

                case 'rm':
                        remove_arg(arg)
                case 'fetch':
                        search_arg(arg)
                case 'restore':
                        restore_arg(arg)
                case 'edit-username':
                        edit_username_arg(arg)
                case 'edit-password':
                        edit_password_arg(arg)
                case 'edit-url':
                        edit_url_arg(arg)

                case 'edit-url':
                        edit_password_arg(arg)
                case _:
                        invalid_argument()
        

def invalid_argument() -> None:
        
        print("error: command not found. For a list of supported comamnds, enter 'help' to console.")

# MAIN

my_username = configure_user()
configure_data()


print("<STARTING> MYLogin 1.0")

menu()

while True:

        user_input = input(f"\033[32m" + my_username + ":~$ \033[0m")

        if len(user_input.split()) == 1:

                user_input = user_input.replace(' ', '')

        match user_input:

                case "home":
                        menu()
                        
                case "help":
                        help()
                        
                case "ls":
                        display()
                        
                case "fetch":
                        search()

                case "fetch-all":
                        search_all()
                        
                case "new":
                        create()
                        
                case "rm":
                        remove()

                case "edit":
                        edit_password()

                case "edit-username":
                        edit_username()
                    
                case "edit-password":
                        edit_password()

                case "edit-url":
                        edit_url()
                        
                case "kill-all":
                        reset()

                case "backup":
                        backup()

                case "restore":
                        restore()

                case "enable":
                        enable()

                case "disable":
                        disable()

                case "default":
                        default()

                case "version":
                        info()

                case "clear":
                        clear()

                case "cls":
                        clear()

                case "whoami":
                        whoami()
                        
                case "exit":
                        break
                case _:
                        check_argument(user_input)


with open (data_name) as log_flag:

        f = json.load(log_flag)

if(f['LOGS'] == "T" and os.path.exists(log_path)):

        log = open(log_path + "/Log " + str(datetime.datetime.now()) + ".txt", 'a')
    
        for i in range(0, len(changelist)):

                log.write(changelist[i])
        
        log.write("\nterminated use at " + str(datetime.datetime.now()))

        log.close()


print("terminated use at " + str(datetime.datetime.now()))
