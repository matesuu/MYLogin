import json
import os
import sys
import datetime

try:
        from cryptography.fernet import Fernet

except ImportError:

        print("\033[31m", end = "")
        print("fatal: cryptography module is not currently installed. for more details, see installation folder")
        print("\033[0m", end = "")
        exit(0)


def encrypt_file(path, cipher) -> None:

        with open(path, 'r') as decrypted:

                data = decrypted.read()
                encoded_data = data.encode('utf-8')
                encrypted_data = cipher.encrypt(encoded_data)
        
        with open(path, 'wb') as write_back:

                write_back.write(encrypted_data)


def decrypt_file(path, cipher) -> None:

        with open(path, 'rb') as encrypted:

                data = encrypted.read()

        decrypted_data = cipher.decrypt(data)
        decoded_data = decrypted_data.decode('utf-8')

        with open(path, 'w') as write_back:

                write_back.write(decoded_data)

def clear() -> None: #clears console and checks to see what os is being used

        if os.name == 'nt': # windows
                
                os.system('cls')
                
        else: # mac/linux
                os.system('clear')


def default(dpath, upath) -> None:

        default_input = input("default all data? (y/n) ")
        new_input = default_input.replace(" ", '')

        if new_input == 'y':

                with open(upath) as read_user:

                        default_user = json.load(read_user)

                        default_user['user'] = ""
                        default_user['val'] = ""
                        default_user['file'] = ""
        
                        with open(upath, 'w') as write_user:

                               json.dump(default_user, write_user, indent = 4)

                with open(dpath) as read_data:

                        default_data = json.load(read_data)

                        default_data['data_entries'] = []
                        default_data['backup_path'] = ""
                        default_data['date_created'] = ""
                        default_data['ID'] = "0"
                        default_data['LOGS'] = "F"

                        with open(dpath, 'w') as write_data:

                                json.dump(default_data, write_data, indent =4)
                
                print("defaulted to base settings. terminate")
                exit()


        else:

                print("process aborted")

def configure_user(path) -> list:

        my_name = ""
        my_h = ""
        my_f = ""
        flag = 0

        key = Fernet.generate_key()
        file = Fernet.generate_key()

        try:

            with open(path) as user_file:
                
                this_user = json.load(user_file)

                if this_user['user'] == "":

                        this_user['user'] = str(os.getlogin())
                        my_name = this_user['user']
                        
                else:
                        
                        my_name = this_user['user']


                if this_user['val'] == "":

                        this_user['val'] = key.decode('utf-8')
                        my_h = this_user['val']

                else:

                        my_h = this_user['val']


                if this_user['file'] == "":

                        this_user['file'] = file.decode('utf-8')
                        my_f = this_user['file']

                else:
                        
                        my_f = this_user['file']

                if this_user['status'] == "D":

                        flag = 0

                else:

                        flag = 1

                with open(path, 'w') as temp:

                        json.dump(this_user, temp, indent=4)

        except:
                print("\033[31m", end = "")
                print("fatal: invalid JSON format (user.json). terminated")
                print("\033[0m", end = "")
                exit()

        return [my_name, my_h, my_f, flag]

                

def configure_data(dpath, bpath) -> None: # gets username and path used for backups
        
        with open(dpath) as data_file:

                this_data = json.load(data_file)

                if this_data['backup_path'] == "":

                        cleaned_path = bpath
                        this_data['backup_path'] = cleaned_path

                if this_data['date_created'] == "":

                        this_data['date_created'] = str(datetime.datetime.now())

                
                with open(dpath, 'w') as user_data:
                        
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
        
        print("MyLogin (Build 0)\nDate Started: 6th June, 2024")
        print("Version Notes:")
        print("1.0: Finished local build repository via JSON storage. Allows for Read-Write operations as well as version control options. Next will be encryption of data.s")
        print("1.1: Added encryption as standard functionality through the crpytography(Fernet) module. See details of how to install in Documentation.")
        print('1.11: Restructed codebase to function as a module rather than a singular file. Added addtional error handling and bug fixes')
        print("\nWritten by matesuu")


def display(path, cipher) -> None:
    
        with open(path) as outfile:
                clients = json.load(outfile)

        for client in clients['data_entries']:

                for names in client.values():

                        encoded_name = names['client'].encode('utf-8')
                        decrypted_name = cipher.decrypt(encoded_name)
                        decoded_name = decrypted_name.decode('utf-8')

                        print("\033[34m", end = "")
                        print(decoded_name)
                        print("\033[0m", end = "")

def search(path, cipher) -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ','')

        with open(path) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        encoded_client = keys['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        if cleaned_input == decoded_client:

                                print("\033[34m", end = "")
                                print("client ~ " + decoded_client)

                                encoded_username = keys['username'].encode('utf-8')
                                encoded_password = keys['password'].encode('utf-8')
                                encoded_url = keys['url'].encode('utf-8')

                                decrypted_username = cipher.decrypt(encoded_username)
                                decrypted_password = cipher.decrypt(encoded_password)
                                decrypted_url = cipher.decrypt(encoded_url)

                                decoded_username = decrypted_username.decode('utf-8')
                                decoded_password = decrypted_password.decode('utf-8')
                                decoded_url = decrypted_url.decode('utf-8')
                                
                                print("username ~ " + decoded_username)
                                print("password ~ " + decoded_password)
                                print("url ~ " + decoded_url)

                                print("\033[0m", end = "")
                                flag = True
                                

        if flag == False:
            
                print("error: could not locate client")

        print("")
                

def search_arg(path, arg, cipher):

        user_input = arg
        cleaned_input = user_input.replace(' ','')

        with open(path) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        encoded_client = keys['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        if cleaned_input == decoded_client:

                                print("\033[34m", end = "")
                                print("client ~ " + decoded_client)

                
                                encoded_username = keys['username'].encode('utf-8')
                                encoded_password = keys['password'].encode('utf-8')
                                encoded_url = keys['url'].encode('utf-8')

                                decrypted_username = cipher.decrypt(encoded_username)
                                decrypted_password = cipher.decrypt(encoded_password)
                                decrypted_url = cipher.decrypt(encoded_url)

                                decoded_username = decrypted_username.decode('utf-8')
                                decoded_password = decrypted_password.decode('utf-8')
                                decoded_url = decrypted_url.decode('utf-8')
                                
                                print("username ~ " + decoded_username)
                                print("password ~ " + decoded_password)
                                print("url ~ " + decoded_url)

                                print("\033[0m", end = "")
                                flag = True
                                

        if flag == False:
            
                print("error: could not locate client", end = "")

        print("")
                

def search_all(path, cipher) -> None:

        with open(path) as outfile:
                curr_data = json.load(outfile)
                
        for local_dicts in curr_data['data_entries']:

                for keys in local_dicts.values():

                        print("\033[34m", end = "")
                        print("")

                        encoded_client = keys['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        print("client ~ " + decoded_client)

                        encoded_username = keys['username'].encode('utf-8')
                        encoded_password = keys['password'].encode('utf-8')
                        encoded_url = keys['url'].encode('utf-8')

                        decrypted_username = cipher.decrypt(encoded_username)
                        decrypted_password = cipher.decrypt(encoded_password)
                        decrypted_url = cipher.decrypt(encoded_url)

                        decoded_username = decrypted_username.decode('utf-8')
                        decoded_password = decrypted_password.decode('utf-8')
                        decoded_url = decrypted_url.decode('utf-8')
                                
                        print("username ~ " + decoded_username)
                        print("password ~ " + decoded_password)
                        print("url ~ " + decoded_url)

                        print("\033[0m", end = "")
        print("")


def create(path, cipher, log) -> None:
        

        flag = False
        size = 0

        with open(path) as check_file:
                check_data = json.load(check_file)
        
        new_client = input("client > ")
        cleaned_client = new_client.replace(' ', '')
        

        for entry in check_data['data_entries']:

                for i in entry.values():
                        
                        size = size + 1

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

                encoded_client = cleaned_client.encode('utf-8')
                encrypted_client = cipher.encrypt(encoded_client)
                decoded_client = encrypted_client.decode('utf-8')

                encoded_username = cleaned_username.encode('utf-8')
                encoded_password = cleaned_password.encode('utf-8')
                encoded_url = new_url.encode('utf-8')

                encrypted_username = cipher.encrypt(encoded_username)
                encrypted_password = cipher.encrypt(encoded_password)
                encrypted_url = cipher.encrypt(encoded_url)

                decoded_username = encrypted_username.decode('utf-8')
                decoded_password = encrypted_password.decode('utf-8')
                decoded_url = encrypted_url.decode('utf-8')

                encoded_date = (str(datetime.datetime.now())).encode('utf-8')
                encrypted_date = cipher.encrypt(encoded_date)
                decoded_date = encrypted_date.decode('utf-8')
                
                new_entry = {"client" : decoded_client, "username" : decoded_username, "password" : decoded_password, "url" : decoded_url}
                new_dict = {decoded_date: new_entry}
        
                with open(path, 'r+') as outfile:
                        
                        outfile_data = json.load(outfile)
                        outfile_data['data_entries'].append(new_dict)
                        outfile.seek(0)
                        json.dump(outfile_data, outfile, indent=4)

                        log.append("\ncreated new client " + cleaned_client + " at " + str(datetime.datetime.now()))
                
        else:

                print("error: client already exists in directory")

def remove(path, cipher, log) -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ','')
        
        with open(path) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

        for entry in curr_data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        if cleaned_input == decoded_client:

                                removed_value = decoded_client
                                curr_data['data_entries'].remove(entry)
                                flag = True

                                log.append("\nremoved client " + decoded_client + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
                json.dump(curr_data, json_file, indent=4)
            
        
        if flag == False:
                print("error: could not locate client")

        
def remove_arg(path, arg, cipher, log) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')
        
        with open(path) as outfile:
                curr_data = json.load(outfile)
                
        flag = False

        for entry in curr_data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        if cleaned_input == decoded_client:

                                removed_value = decoded_client
                                curr_data['data_entries'].remove(entry)
                                flag = True

                                log.append("\nremoved client " + decoded_client + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
                json.dump(curr_data, json_file, indent=4)
            
        
        if flag == False:
                print("error: could not locate client")



def edit_username(path, cipher, log) -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')
                        
                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)

                                encoded_username_old = i['username'].encode('utf-8')
                                decrypted_username_old = cipher.decrypt(encoded_username_old)
                                decoded_username_old = decrypted_username_old.decode('utf-8')
                                
                                new_pass = input("username > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_username_new = clean_pass.encode('utf-8')
                                encrypted_username_new = cipher.encrypt(encoded_username_new)
                                decoded_username_new = encrypted_username_new.decode('utf-8')

                                i['username'] = decoded_username_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " username from " + decoded_username_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_username_arg(path, arg, cipher, log) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')
                        
                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)

                                encoded_username_old = i['username'].encode('utf-8')
                                decrypted_username_old = cipher.decrypt(encoded_username_old)
                                decoded_username_old = decrypted_username_old.decode('utf-8')
                                
                                new_pass = input("username > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_username_new = clean_pass.encode('utf-8')
                                encrypted_username_new = cipher.encrypt(encoded_username_new)
                                decoded_username_new = encrypted_username_new.decode('utf-8')

                                i['username'] = decoded_username_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " username from " + decoded_username_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))
                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")
        
def edit_password(path, cipher, log) -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False


        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():
                        
                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')

                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)

                                encoded_username_old = i['password'].encode('utf-8')
                                decrypted_username_old = cipher.decrypt(encoded_username_old)
                                decoded_password_old = decrypted_username_old.decode('utf-8')

                                new_pass = input("password > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_username_new = clean_pass.encode('utf-8')
                                encrypted_username_new = cipher.encrypt(encoded_username_new)
                                decoded_password_new = encrypted_username_new.decode('utf-8')

                                i['password'] = decoded_password_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " password from " + decoded_password_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_password_arg(path, arg, cipher, log) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')
                        
                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)

                                encoded_username_old = i['password'].encode('utf-8')
                                decrypted_username_old = cipher.decrypt(encoded_username_old)
                                decoded_password_old = decrypted_username_old.decode('utf-8')

                                new_pass = input("password > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_username_new = clean_pass.encode('utf-8')
                                encrypted_username_new = cipher.encrypt(encoded_username_new)
                                decoded_password_new = encrypted_username_new.decode('utf-8')

                                i['password'] = decoded_password_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " password from " + decoded_password_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")

def edit_url(path, cipher, log) -> None:

        user_input = input("client > ")
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')
                        
                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)
                                
                                encoded_url_old = i['url'].encode('utf-8')
                                decrypted_url_old = cipher.decrypt(encoded_url_old)
                                decoded_url_old = decrypted_url_old.decode('utf-8')

                                new_pass = input("url > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_url_new = clean_pass.encode('utf-8')
                                encrypted_url_new = cipher.encrypt(encoded_url_new)
                                decoded_url_new = encrypted_url_new.decode('utf-8')

                                i['url'] = decoded_url_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " URL from " + decoded_url_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))
                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def edit_url_arg(path, arg, cipher, log) -> None:

        user_input = arg
        cleaned_input = user_input.replace(' ', '')

        flag = False

        with open(path) as file:

                data = json.load(file)

        for entry in data['data_entries']:
                
                for i in entry.values():

                        encoded_client = i['client'].encode('utf-8')
                        decrypted_client = cipher.decrypt(encoded_client)
                        decoded_client = decrypted_client.decode('utf-8')
                        
                        if cleaned_input == decoded_client:
                                
                                print(decoded_client)
                                
                                encoded_url_old = i['url'].encode('utf-8')
                                decrypted_url_old = cipher.decrypt(encoded_url_old)
                                decoded_url_old = decrypted_url_old.decode('utf-8')

                                new_pass = input("url > ")
                                clean_pass = new_pass.replace(' ', '')

                                encoded_url_new = clean_pass.encode('utf-8')
                                encrypted_url_new = cipher.encrypt(encoded_url_new)
                                decoded_url_new = encrypted_url_new.decode('utf-8')

                                i['url'] = decoded_url_new
                                flag = True

                                log.append("\nedited " + cleaned_input + " URL from " + decoded_url_old + " to " + clean_pass + " at " + str(datetime.datetime.now()))

                                break

        with open(path, 'w') as json_file:
            
            json.dump(data, json_file, indent=4)
       
        
        if flag == False:

                print("error: could not locate client")


def reset(path, log) -> None:
        
        user_input = input("delete all entries? (y/n) ")
        cleaned_input = user_input.replace(' ', '')
        flag = False

        with open(path) as outfile:

                data = json.load(outfile)

        if cleaned_input == 'y':

                for entry in data['data_entries']:

                        for i in entry.values():
                                data['data_entries'].clear()
                                flag = True
                                break
                        
        with open(path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

        
        if flag == True:
                
                print("deleted everything")
                log.append("\ndeleted all entries at " + str(datetime.datetime.now()))

        else:
                print("process aborted")


def backup(dpath, fcipher, log) -> None:

        with open(dpath) as file: # opens data.json to read from file and store in dictionary 'data'

                data = json.load(file)
                

        new_id = int(data['ID'])      # stores the current backup ID in new_id
        new_id+=1                               # increments ID by 1
        data['ID'] = str(new_id)      # casts new_id to string
        

        with open(dpath, 'w') as update_id:       # opens data.json to write to file and dumps data, the only difference being 
                                                        # the incremented ID
                        
                json.dump(data, update_id, indent=4)

        

        bpath = data['backup_path']                      # gets path of backup folder

        if not os.path.exists(bpath):

                print('error: backups folder does not exist or cannot be located')
                return 

        data['date_created'] = str(datetime.datetime.now())     # stores the date of creation in 'date_created' as a string
        

        if os.path.exists(bpath +  str(new_id) + '.json'):

                new_json = open(bpath + '/backup(' + str(datetime.datetime.now()) + ').json', 'x').close()
            
                with open(bpath + 'backup(' + str(datetime.datetime.now()) + ').json', 'w') as json_file:

                        json.dump(data, json_file, indent=4)

                encrypt_file(bpath +  str(new_id) + '.json', fcipher)

        else:
            
                new_json = open(bpath + '/backup(' + str(new_id) + ').json', 'x').close()
            
                with open(bpath + '/backup(' + str(new_id) + ').json', 'w') as json_file:

                        json.dump(data, json_file, indent=4)
                
                encrypt_file(bpath + '/backup(' + str(new_id) + ').json', fcipher)

        
        log.append("\ndata backup at " + str(datetime.datetime.now()))

def restore(dpath, fcipher, log) -> None:

        with open(dpath) as get_path:
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

        try:
                decrypt_file(path_data['backup_path'] + '/' + backup_file, fcipher)

                with open(path_data['backup_path'] + '/' + backup_file) as json_file:
                        backup_data = json.load(json_file)
                        log.append("\nrestored data from " + backup_file + " at " + str(datetime.datetime.now()))
                        
                backup_data['ID'] = str(new_master)

                encrypt_file(path_data['backup_path'] + '/' + backup_file, fcipher)
                
                with open(dpath, 'w') as restored_file:
                        json.dump(backup_data, restored_file, indent=4)
                        
                print("restored from file")

        except:
                
                print("error: file error")


def restore_arg(dpath, arg, fcipher, log) -> None:

        with open(dpath) as get_path:

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
                decrypt_file(path_data['backup_path'] + '/' + backup_file, fcipher)

                with open(path_data['backup_path'] + '/' + backup_file) as json_file:
                        backup_data = json.load(json_file)
                        log.append("\nrestored data from " + backup_file + " at " + str(datetime.datetime.now()))
                        
                backup_data['ID'] = str(new_master)

                encrypt_file(path_data['backup_path'] + '/' + backup_file, fcipher)
                
                with open(dpath, 'w') as restored_file:
                        json.dump(backup_data, restored_file, indent=4)
                        
                print("restored from file")

        except:
                
                print("error: file error")

        

def enable(path) -> None:

    with open(path) as enable_logs:

        e = json.load(enable_logs)

    e['LOGS'] = "T"
    print("logs enabled")
    
    with open(path, 'w') as finish_enable:

        json.dump(e, finish_enable, indent=4)
        

def disable(path) -> None:

    with open(path) as disable_logs:

        d = json.load(disable_logs)

    d['LOGS'] = "F"
    print("logs disabled")
    

    with open(path, 'w') as finish_disable:

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

def check_argument(path, string, cipher, fcipher, log) -> None:

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
                        remove_arg(path, arg, cipher, log)
                case 'fetch':
                        search_arg(path, arg, cipher)
                case 'restore':
                        restore_arg(path, arg, fcipher, log)
                case 'edit-username':
                        edit_username_arg(path, arg, cipher, log)
                case 'edit-password':
                        edit_password_arg(path, arg, cipher, log)
                case 'edit-url':
                        edit_url_arg(path, arg, cipher, log)
                case _:
                        invalid_argument()
        

def invalid_argument() -> None:
        
        print("error: command not found. For a list of supported comamnds, enter 'help' to console.")
