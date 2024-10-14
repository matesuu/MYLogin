#Welcome to the MYLogin project.

import os
import json
import datetime

user_info = str(os.getcwd()) + "/Data/user.json"
data_name = str(os.getcwd()) + "/Data/data.json"
log_path = str(os.getcwd()) + "/Logs"


try:

    with open(data_name) as log_open:

        temp = json.load(log_open)
        log_flag = temp['LOGS']

except:

    print("fatal: invalid JSON format (data.json). terminated")
    exit()


if log_flag == "T":

    log = open(log_path + "/Log " + str(datetime.datetime.now()) + ".txt", 'a')
    log.write("Access at " + str(datetime.datetime.now()))


def clear() -> None: #clears console and checks to see what os is being used

        if os.name == 'nt': # windows
                
                os.system('cls')
                
        else: # mac/linux
                os.system('clear')


def configure_user() -> str:

        my_name = "NULL"

        try:

            with open(user_info) as user_file:
                
                    this_user = json.load(user_file)

                    if this_user['user'] == "NULL":

                            this_user['user'] = str(os.getlogin())
                            my_name = this_user['user']
                        
                    else:
                        
                            my_name = this_user['user']

                    with open(user_info, 'w') as temp:

                            json.dump(this_user, temp, indent=4)

        except:

                print("fatal: invalid JSON format (user.json). terminated")
                exit()

        return my_name

                

def configure_data() -> None: # gets username and path used for backups
        
        with open(data_name) as data_file:

                this_data = json.load(data_file)

                if this_data['backup_path'] == "NULL":


                        cleaned_path = str(os.getcwd()) + "/Backups"
                        this_data['backup_path'] = cleaned_path

                if this_data['date_created'] == "NULL":

                        this_data['date_created'] = str(datetime.datetime.now())

                
                with open(data_name, 'w') as user_data:
                        
                        json.dump(this_data, user_data, indent=4)


def menu() -> None:
    
        icon()
        
        print("Welcome to MYLogin. This is a lightweight CLI tool intended to store user information with associated client login information. Enter 'help' to console to see the list of supported operations.\n")
        


def help() -> None:
        
        print("\nhome - returns to main menu")
        print("ls - displays all current clients as a list")
        print("fetch - returns all associated login information with a given client")
        print("new - creates a new client-information pair in dictionary - flags: Optional: [-all]")
        print("rm - removes a specified cient password pair from dictionary]")
        print("edit - change a pre-existing information with an associated client - flags: [-username] [-password] [-url] default [-password]")
        print("kill -all - deletes all currently existing client-password pairs held within data file")
        print("backup - writes current data to a new backup to be stored in backups folder")
        print("restore - restores data from a given backup")
        print("enable - enables read logs")
        print("disable - disables read logs")
        print("vrs - displays version information")
        print("quit - terminate application\n")


def info() -> None:
        
        print("MyLogin (Build 0)\nDate Started: 06/06/2024\nDate Finalized: 10/13/2024")
        print("Notes: Finished local build repository via JSON storage. Allows for Read-Write operations as well as version control options. Next will be information transfer via Sockets\n")
        print("Written by matesuu")
        print("Fibonacci Yeah! (>_<)")


def display() -> None:
    
        with open(data_name) as outfile:
                clients = json.load(outfile)

        for client in clients['data_entries']:

                for names in client.values():
                
                        print(names['client'])

def search() -> None:

        user_input = input("CLIENT > ")
        cleaned_input = user_input.replace(' ','')

        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        if cleaned_input == keys['client']:

                                print("")
                                print(keys['client'])
                                print(keys['username'])
                                print(keys['password'])
                                print(keys['url'])
                                flag = True
                                

        if flag == False:
            
                print("error: could not locate client", end = "")

        print("")
                


def search_all() -> None:

        with open(data_name) as outfile:
                curr_data = json.load(outfile)
                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        print("\n" + keys['client'])
                        print(keys['username'])
                        print(keys['password'])
                        print(keys['url'])
        print("")


def create() -> None:
        

        flag = False

        with open(data_name) as check_file:
                check_data = json.load(check_file)
        
        new_client = input("CLIENT > ")
        cleaned_client = new_client.replace(' ', '')
        

        for entry in check_data['data_entries']:

                for i in entry.values():

                        if cleaned_client == i['client']:

                                flag = True

        if cleaned_client == '':

                flag = True

                
        if flag == False:

                new_username = input("USERNAME > ")
                new_password = input("PASSWORD > ")
                new_url = input("URL > ")

                cleaned_username = new_username.replace(' ','')
                cleaned_password = new_password.replace(' ','')
                
                new_entry = {"client" : cleaned_client, "username" : cleaned_username, "password" : cleaned_password, "url" : new_url}
                new_dict = {cleaned_client : new_entry}
        
                with open(data_name, 'r+') as outfile:
                        
                        outfile_data = json.load(outfile)
                        outfile_data['data_entries'].append(new_dict)
                        outfile.seek(0)
                        json.dump(outfile_data, outfile, indent=4)

                        log.write("Created New Client: " + cleaned_client + " at " + str(datetime.datetime.now()))
                
        else:

                print("error: client already exists in directory")

def remove() -> None:

        user_input = input("CLIENT > ")
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
                                break

        with open(data_name, 'w') as json_file:
                json.dump(curr_data, json_file, indent=4)
            
                
       
        
        if flag == False:
                print("error: could not locate client")


def edit_username() -> None:

    user_input = input("CLIENT > ")
    cleaned_input = user_input.replace(' ', '')

    flag = False

    with open(data_name) as file:

            data = json.load(file)

    for entry in data['data_entries']:
                
            for i in entry.values():
                        
                    if cleaned_input == i['client']:
                                
                            print(i['client'])
                            edited_value = i['client']
                            new_pass = input("USERNAME > ")
                            clean_pass = new_pass.replace(' ', '')
                            i['username'] = clean_pass
                            flag = True
                            break

            with open(data_name, 'w') as json_file:
                
                json.dump(data, json_file, indent=4)
       
        
            if flag == False:

                print("error: could not locate client")
        
def edit_password() -> None:

        user_input = input("CLIENT > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(data_name) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        if cleaned_input == i['client']:
                                
                                print(i['client'])
                                edited_value = i['client']
                                new_pass = input("PASSWORD > ")
                                clean_pass = new_pass.replace(' ', '')
                                i['password'] = clean_pass
                                flag = True
                                break

        with open(data_name, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

            print("error: could not locate client")

def edit_url() -> None:

    user_input = input("CLIENT > ")
    cleaned_input = user_input.replace(' ', '')

    flag = False

    with open(data_name) as file:

            data = json.load(file)

    for entry in data['data_entries']:
                
            for i in entry.values():
                        
                    if cleaned_input == i['client']:
                                
                            print(i['client'])
                            edited_value = i['client']
                            new_pass = input("URL > ")
                            clean_pass = new_pass.replace(' ', '')
                            i['url'] = clean_pass
                            flag = True
                            break

            with open(data_name, 'w') as json_file:
            
                json.dump(data, json_file, indent=4)
       
        
            if flag == False:

                    print("error: could not locate client")

def reset() -> None:
        
        user_input = input("delete all entries? (y/n)")
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
        data['date_created'] = str(datetime.datetime.now())     # stores the date of creation in 'date_created' as a string
        

        if os.path.exists(path +  str(new_id) + '.json'):

            new_json = open(path + '/backup-' + str(datetime.datetime.now()) + '.json', 'x').close()
            
            with open(path + 'backup-' + str(datetime.datetime.now()) + '.json', 'w') as json_file:

                json.dump(data, json_file, indent=4)

        else:
            
            new_json = open(path + '/backup-' + str(new_id) + '.json', 'x').close()
            
            with open(path + '/backup-' + str(new_id) + '.json', 'w') as json_file:

                json.dump(data, json_file, indent=4)
        

def restore() -> None:

        with open(data_name) as get_path:
            path_data = json.load(get_path)

        dir_list = os.listdir(path_data['backup_path'])
        print(dir_list)

        new_master = int(path_data['ID'])
        
        backup_file = input("RESTORE WITH > ")

        #note: have to handle case where inputted string is not a valid file... try catch block maybe?

        try:
                with open(path_data['backup_path'] + '/' + backup_file) as json_file:
                        backup_data = json.load(json_file)
                        
                backup_data['ID'] = str(new_master)
                
                with open(data_name, 'w') as restored_file:
                        json.dump(backup_data, restored_file, indent=4)
                        
                print("restored from file")

        except FileNotFoundError:
                
                print("error: file not found")


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

    log.close()

    if os.path.exists(log_path + "/Log " + str(datetime.datetime.now())):
        
        os.remove(log_path + "/Log " + str(datetime.datetime.now()))
    

def icon() -> None:

        print("""
                            _
 __  ___    ___            |+|                       
|  \/  \ \ / / |   ___ __ _ _ _ _
| |\/| |\ V /| |__| _ / _` | | '  \                        
|_|  |_| |_| |____|___\__, |_|_||_|
                      |___/ 
        """) # prints icon
        

def invalid_argument() -> None:
        
        print("error: command not found. For a list of supported comamnds, enter 'help' to console.")



my_username = configure_user()
configure_data()

print("<STARTING> MYLogin 1.0")

menu()

while True:

        user_input = input(my_username + ":~$ > ")

        match user_input:

                case "home":
                        menu()
                        
                case "help":
                        help()
                        
                case "ls":
                        display()
                        
                case "fetch":
                        search()

                case "fetch -all":
                        search_all()
                        
                case "new":
                        create()
                        
                case "rm":
                        remove()

                case "edit":
                        edit_password()

                case "edit -username":
                        edit_username()
                    
                case "edit -password":
                        edit_password()

                case "edit -url":
                        edit_url()
                        
                case "kill -all":
                        reset()

                case "backup":
                        backup()

                case "restore":
                        restore()

                case "enable":
                        enable()

                case "disable":
                        disable()

                case "vrs":
                        info()

                case "clear":
                        clear()

                case "cls":
                        clear()
                        
                case "quit":
                        break
                case _:
                        invalid_argument()
                

print("terminated use at " + str(datetime.datetime.now()))