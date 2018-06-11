

# IMPORTS
import os
import json
import pprint
# import nuke
import re

# CONSTANTS

PATH = "//fbbblue/00_jobs/baj_benjamin/prod/plates/footage_vfx_plates/vfx_plates_QTref/Generic Plate11-01 B.mov"
MOV = "Generic Plate11-01 B.mov"
LOGS = "C:\LOGS"

FULLPATH = "C:\LOGS\log1_1.json"
FULLPATH2 = "C:\LOGS\log2_2.json"
FULLPATH3 = "C:\LOGS\log3_3.json"
FULLPATH4 = "C:\LOGS\log4_4.json"

COMBINED_JSON = "C:\LOGS\combined_logs.json"
COMBINED_JSON_MIN_MAX_FORMATTED = "C:\LOGS\combined_logs_min_max_formatted.json"

FILE_1 = "log1"
FILE_1_1 = "log1_1"

FILE_2 = "log2"
FILE_2_2 = "log2_2"

FILE_3 = "log3"
FILE_3_3 = "log3_3"

FILE_4 = "log4"
FILE_4_4 = "log4_4"

# MAIN FUNCTIONS

def write_jason(path,data):
    jason = path
    data = data
    with open(jason, "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return data

def analyze_data(path):
    in_points = []
    out_points = []
    data = get_json(path)[0]
    for i in data.keys():
        for e in d[i]:
            in_= d[i][e][0]
            out_ = d[i][e][1]
            in_points.append(in_)
            out_points.append(out_)
    min_in= min(in_points)
    max_out = max(out_points)
    return  min_in,max_out


def get_json(path,file):

    path = "{}".format(path)
    jason_path = "{}\{}.json".format(path,file)
    _file = open(jason_path, "r")
    data = json.load(_file)

    return data


def print_log_keys_number(file):
    count = 0
    for i in range(len(file)):
       count +=1
    return count


def print_log_keys(file):
    key_list = []
    for i in file.keys():
        key_list.append(i)
    non_duplicates = list(set(key_list))
    return non_duplicates


def print_log_keys_number(file):
    count = 0
    for i in range(len(file)):
       count +=1
    return count


def print_pretty_jsonfiles(f):
    data = f.write(json.dumps(yourdictionary, indent=4, sort_keys=True))
    return data


def alf_function(mydict2,mydict):

    my_dict_copy = mydict.copy()

    for plate, shots in mydict2.iteritems():
        if not my_dict_copy.has_key(plate):
            my_dict_copy[plate] = dict()
        for shot, values in shots.iteritems():
            # add shots to plate
            my_dict_copy[plate][shot] = values

    return my_dict_copy


# FUNCTION CALLS VARIABLES


#print len(get_json(LOGS,"combined_logs_min_max_formatted").keys())
#pprint.pprint(get_json(LOGS,"combined_logs_min_max_formatted"))



#dictionaries

data_1 = get_json(LOGS,FILE_1)
data_1_1 = get_json(LOGS,FILE_1_1)#formatted dic

data_2 = get_json(LOGS,FILE_2)
data_2_2 = get_json(LOGS,FILE_2_2)#formatted dic

data_3 = get_json(LOGS,FILE_3)
data_3_3 = get_json(LOGS,FILE_3_3)#formatted dic

data_4 = get_json(LOGS,FILE_4)
data_4_4 = get_json(LOGS,FILE_4_4)#formatted dic


#combined dictionarie

combi = alf_function(data_2,data_1)
combi2 = alf_function(combi,data_3)
combi3 = alf_function(combi2,data_4)


new_shiny_json = write_jason(COMBINED_JSON,combi3)

#checkups

log_1_number = print_log_keys_number(print_log_keys(data_1))
log_1_keys = print_log_keys(data_1)

log_1_1_number = print_log_keys_number(print_log_keys(data_1_1))
log_1_1_keys = print_log_keys(data_1_1)

log_2_number = print_log_keys_number(print_log_keys(data_2))
log_2_keys = print_log_keys(data_2)

log_2_2_number = print_log_keys_number(print_log_keys(data_2_2))
log_2_2_keys = print_log_keys(data_2_2)

log_3_number = print_log_keys_number(print_log_keys(data_3))
log_3_keys = print_log_keys(data_3)

log_4_number = print_log_keys_number(print_log_keys(data_4))
log_4_keys = print_log_keys(data_4)


log_items = [log_1_number, log_2_number, log_3_number,log_4_number]
log_unique_keys = list(set(log_1_keys + log_2_keys + log_3_keys + log_4_keys))


