# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 18:53:40 2022

@author: user
"""

#from sre_constants import AT_END_STRING
import os
import csv
import json


def split_chat(chat):
    """ 
    Takes as the argument a textual file chat. Each line
    has the following structure: <date>, <time> - <name>: <message_text>

    Returns a tuple (dates, times, texts, freqs):
        - dates is a list of all the dates the messages were sent
        - times is a list of all the times the messages were sent
        - texts is a list of all the textual contents of the messages, one by one
        - freqs is a tuple (<name1_frequency>, <name2_frequency>) of the number of messages each of the participants sent
    """
    dates, times, texts, freqs = [], [], [], {}
    with open(chat, 'r', encoding = 'utf-8') as file:
        next(file)
        for line in file:
            if("changed their phone number. You're currently chatting with their new number. Tap to add it to your contacts." in line):
                continue
            dash_split = line.split('-')
            datetime_check = len(dash_split[0]) > 11 and dash_split[0][-4] == ':' and dash_split[0][-8] == ',' and dash_split[0][-11] == '/'
            if(len(dash_split) == 2 and datetime_check):
                date_time = dash_split[0].split(',')
                for s in date_time:
                    s = s.strip()
                name_text = dash_split[1].split(':')
                for s in name_text:
                    s = s.strip()
                dates.append(date_time[0])
                times.append(date_time[1])
                texts.append(name_text[1])
                #print(texts)
                if name_text[0] in freqs:
                    freqs[name_text[0]] += 1
                else:
                    freqs[name_text[0]] = 1
            elif(len(dash_split) == 2):
                texts[-1] = texts[-1] + dash_split[0] + dash_split[1]
            else:
                texts[-1] = texts[-1] + dash_split[0]

            
            rows_list = [[dates[i], times[i], texts[i]] for i in range(len(dates))] #for the csv file 
    return (dates, times, texts, freqs, rows_list)

def chat_info(chat):
    (dates, times, texts, freqs, rows_list) = split_chat(chat)
    dates_dict = {}
    for date in dates:
        if date in dates_dict:
            dates_dict[date] += 1
        else:
            dates_dict[date] = 1
    return (dates_dict, times, texts, freqs, rows_list)


def fill_csvs(fields, chats):
    for chat in chats:
        if(chat[-1] != 't'):
            continue
        name = chat.split('.')
        name = name[0]
        with open('data_' + name + '.csv', 'w', encoding = 'utf-8') as datafile:
            write = csv.writer(datafile)
            (dates, times, texts, freqs, rows_list) = chat_info(chat)
            write.writerow(fields)
            for row in rows_list:
                write.writerow(row)


def fill_one(fields, chat):
    if(chat[-1] != 't'):
        return chat
    name = chat.split('.')
    name = name[0]
    with open('data_' + name + '.csv', 'w', encoding = 'utf-8') as datafile:
        write = csv.writer(datafile)
        (dates, times, texts, freqs, rows_list) = split_chat(chat)
        print('dates: ' + str(dates) + ' ,length: ' + str(len(dates)))
        print('times: ' + str(times) + ' ,length: ' + str(len(times)))
        print('freqs: ' + str(freqs))
        print('rows_list: ' + str(rows_list) + ' ,length: ' + str(len(rows_list)))
        write.writerow(fields)
        for row in rows_list:
            write.writerow(row)
        
chats = os.listdir()
fields = ['date', 'time', 'text']

#fill_one(fields, chats[-9])

#fill_csvs(fields, chats)

        













