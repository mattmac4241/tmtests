#!/usr/bin/env python

import csv
import re
import sys

def get_contents(file_name):
    emails = {}
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(reader)
        for row in reader:
            number = row[0]
            found = emails.get(number)
            message = row[6].strip()

            find_emails = proccess_message(message)
            find_codes = find_code(message)

            if found is None:
                message = []

                if len(find_emails) > 0:
                    message.append(find_emails[0])
                if len(find_codes) > 0:
                    message.append(find_codes[0])
                emails[number] = message

            elif message not in found:
                if len(find_emails) > 0:
                    found.append(find_emails[0])
                if len(find_codes) > 0:
                    found.append(find_codes[0])
                found.sort()
                emails[number] = found

    return emails

def write_results(file_name, contents, names):
    fields = ['phone_number', 'emails', 'codes', 'matching_emails']

    with open(file_name, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

        for number in contents:
            info = contents[number]
            codes, emails = format_contents(info)
            discovered_emails = []
            for e in emails:
                found_name = names.get(e)
                if found_name:
                    discovered_emails.append(found_name[0])

            row = [number, emails, codes, discovered_emails]
            csvwriter.writerow(row)


def read_names(file_name):
    names = {}
    with open(file_name) as name_file:
        lines = name_file.readlines()

        for line in lines:
            name = convert_name(line)
            name_found = names.get(name)

            # incase emails are similar
            if name_found is None:
                names[name] = [line.strip()]
            else:
                name_found.append(line.strip())
                names[name] = name_found
    return names

def convert_name(name):
    parts = name.split('@')
    first_part = parts[0]
    middle = first_part[1:len(first_part)-1]
    new_string = first_part[0]

    for c in middle:
        new_string += "*"
    new_string = f"{new_string}{first_part[len(first_part)-1]}@{parts[1]}".strip()

    return new_string


def format_contents(row):
    codes = []
    emails = []
    for r in row:
        if is_code(r):
            codes.append(r)
        else:
            emails.append(r)
    return (codes, emails)


def is_code(message):
    return len(message) == 7

def proccess_message(message):
    email = re.findall("([a-zA-Z0-9\*_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", message)
    return email

def find_code(message):
    code = re.findall("([A-Z0-9]{7})", message)
    return code


if __name__ == '__main__':
    print('Hello!')
    csv_file = input("What is the name of the csv file you\'d like me to read: ")
    account_file = input('What is the name of the account list you\'d like me to read: ')
    emails = get_contents(csv_file)
    names = read_names(account_file)
    write_results('results.csv', emails, names)
