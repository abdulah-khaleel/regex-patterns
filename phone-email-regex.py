#! python3

import re
from sys import path_importer_cache
from attr import has
import pyperclip
import os
import pathlib
import csv


# Getting text off the clipboard
clipboard_text = pyperclip.paste()

#Display program options:
def menu():
    print(''' 
  _______        _     ______      _                  _             
 |__   __|      | |   |  ____|    | |                | |            
    | | _____  _| |_  | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __ 
    | |/ _ \ \/ | __| |  __| \ \/ | __| '__/ _` |/ __| __/ _ \| '__|
    | |  __/>  <| |_  | |____ >  <| |_| | | (_| | (__| || (_) | |   
    |_|\___/_/\_\\__| |______/_/\_\\__|_|  \__,_|\___|\__\___/|_|   
                                                                    
''')
    print('''What would you like to do? Choose a program number from the options below:

        1) Extract emails from text
        2) Extract URLs from text
        3) Extract mobile numbers from text (Afghanistan numbers)
        4) Remove whitespaces from text
        0) Exit Program

    ''')

# Clear screen
clear = lambda: os.system('clear')

# Generate a text file with the output of program:
def gen_text_file(formatted_text):
    with open('data.txt', 'w') as f:
        f.write(formatted_text)
    path_text_file = str(pathlib.Path().resolve())
    input('\n\nThe data was saved into \'data.txt\' which can be found at: ' + path_text_file + '\n\n')
    clear()

# Generate a csv file with the output of program:
def gen_csv_file(extracted_text,item_type):
    with open('data.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow([item_type])
        # write the data
        for text in extracted_text:
            writer.writerow([text])
        f.close()
    path_text_file = str(pathlib.Path().resolve())
    input('\n\nThe data was saved into \'data.csv\' which can be found at: ' + path_text_file + '\n\n')
    clear()

# Function to ask for exporting data to txt or csv
def ask_for_export(item_type, extracted_data, formatted_data):
    export_data = input(f'Your formatted data was pasted to your clipoboard. Would you like to store this data into a file as well? (Y/N)\n\n')
    if export_data in ['Y','y','Yes','yes','YES']:
        export_option = input('''
        Enter 1 for exporting data to a .txt file 
        Enter 2 for exporting data to a .csv file
        ''')
        if export_option == '1':
            # Writing to a .txt file
            gen_text_file(formatted_data)
        elif export_option == '2':
            # Writing to a .csv file
            gen_csv_file(extracted_data,item_type)
        else:
            pass

# Regexes here:
v_email_regex = re.compile(r''' 
        [a-zA-Z0-9-_.+]+     # first part of email
        @                    # @ separator
        [a-zA-Z0-9-_.+]+     # domain part of the email
        ''', re.VERBOSE)
v_url_regex = re.compile(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
v_phone_regex = re.compile(r''' 
        (                    # container group
        ((07)|(\+937)|(00937)) # first part of phone - with country code + 07 key
        (\d\d\d\d\d\d\d\d)     # remainder 8 digits
        )
        ''', re.VERBOSE)

# Function to apply regex and output extracted text:
def extract_text(reg, clipboard_text, selected_program, has_list):
    extracted_text = reg.findall(clipboard_text)
    formatted_text = ''
    my_list = []
    count = 0
    if has_list:
        for item in extracted_text:
            formatted_text += item[0] + '\n'
            my_list.append(item[0])
            count += 1
    else:
        for item in extracted_text:
            formatted_text += item + '\n'
            count += 1
    
    pyperclip.copy(formatted_text)


    # prompting user for export option:
    if has_list:
        ask_for_export(selected_program,my_list,formatted_text)
    else:
        ask_for_export(selected_program,extracted_text,formatted_text)

# Display copy reminder message:
def display_copy_message():
    input('\n\nHave you copied the source text to your clipboard? If not, please copy and press Enter to proceed.\n\n')

####################
# Starting program:#
####################

clear()
menu()

program = input('Please select a program: (e.g. Enter 1 for emails) \t')

while program != '0':
    # Extract emails:
    if program == '1':

        display_copy_message()
        extract_text(v_email_regex,clipboard_text,'Email',False)
        
    # Extract URLs:
    elif program == '2':
        
        display_copy_message()
        extract_text(v_url_regex,clipboard_text,'URL',True)
        
    # Extract phone numbers
    elif program == '3':
     
        display_copy_message()
        extract_text(v_phone_regex,clipboard_text,'Phone Number',True)

    elif program == '4':
        
        input('\n\nHave you copied the source text to your clipboard? If not, please copy and press Enter to proceed.\n\n')
        clipboard_text = pyperclip.paste()
        
        pyperclip.copy(re.sub(' +',' ',clipboard_text))
        input('Whitespaces have now been removed and the new text is copied to your clipboard. Press Enter to get back to the program menu.')
        clear()

    else:
        
        input('\n\nSorry, no such option is available. Try again with a program number!\t')
        clear()
    
    menu()
    program = input('Please select a program: (e.g. 1 for emails) \t')

print('\n\nThank you for using this program!\n\n')


             