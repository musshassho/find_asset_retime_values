# IMPORTS

import os
import json
import os
import pprint

# VARIABLES

log1_path = "C:/LOGS/log1.json"
log1_path2 = "C:/LOGS/log2.json"
log1_path3 = "C:/LOGS/log4.json"
log1_path4 = "C:/LOGS/log4.json"
log1_formatted = "C:/LOGS/combined_logs_min_max_formatted.json"
log1_combined = "C:/LOGS/combined_logs.json"
COMBINED_JSON = "C:\LOGS\combined_logs.json"

NEW_MIX_MAX_FORMATTED = "C:/LOGS/combined_logs_min_max_formatted_new.json"

suffix = ".mov"

#FUNCTIONS

def get_jason(path):
    if os.path.isfile(path):
        with open(path) as data_file:
            log1 = json.loads(data_file.read())
    return log1


def write_jason(path,data):
    jason = path
    data = data
    with open(jason, "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
    return data


def detect_not_movs(iterable):

    for i in iterable.keys():
        print i
        if i.endswith(suffix):
            print "gut"

        else:
            print "UPS"
            break


def combine_dics(mydict2, mydict):

    my_dict_copy = mydict.copy()

    for plate, shots in mydict2.iteritems():
        if not my_dict_copy.has_key(plate):
            my_dict_copy[plate] = dict()
        for shot, values in shots.iteritems():
            # add shots to plate
            my_dict_copy[plate][shot] = values

    return my_dict_copy


def write_max_min(dct):
    blacklist = ["max", "min"]
    new_list = {}
    for i in dct.keys():
        dct[i]["min"] = 0
        dct[i]["max"] = 0
        min_ = dct[i]["min"]
        max_ = dct[i]["max"]
        for e in dct[i]:
            if e not in blacklist:
                in_ = dct[i][e][0]
                out_= dct[i][e][1]
                if min_ == 0:
                    min_ = in_
                elif min_ > in_:
                    min_ = in_
                if max_ == 0:
                    max_ = out_
                elif max_ < out_:
                    max_ = out_

        dct[i]["min"] = min_
        dct[i]["max"] = max_

        new_list[i] = dct[i]

    return new_list


#DATA CREATION

#log_formatted = get_jason(log1_formatted)

log_1 = get_jason(log1_path)
log_2 = get_jason(log1_path2)
log_3 = get_jason(log1_path3)
log_4 = get_jason(log1_path4)

#DATA COMBINATION

combi = combine_dics(log_1, log_2)
combi2 = combine_dics(combi, log_3)
combi3 = combine_dics(combi2, log_4)


# DATA COMBINATION WRITING

#new_shiny_json = write_jason(COMBINED_JSON,combi3)

# OMBINED WRITTEN DATA DATA CHECKING!

#detect_not_movs(new_shiny_json)

# COMBINED DATA  -> MIX MAX ADDING

#combined_mix_max = write_max_min(new_shiny_json)

# COMBINED DATA  -> MIX MAX ADDING CHECKING!

#detect_not_movs(combined_mix_max)

# DATA COMBINATION MIX MAX FORMATTED WRITING

#combined_mix_max_formatted = write_jason(NEW_MIX_MAX_FORMATTED,combined_mix_max)

# DATA COMBINATION MIX MAX FORMATTED CHECKING!

combined_mix_max_formatted_written = get_jason(NEW_MIX_MAX_FORMATTED)
#detect_not_movs(combined_mix_max_formatted_written)

#print len(combined_mix_max_formatted_written.keys())

#pprint.pprint(combined_mix_max_formatted_written)

def troubleshoot_framerange_exceeding_files(log_):

    for i in log_.keys():
        #print i
        if i == "003_Plate1-03 B.mov":
            print 'FOUND'
            pprint.pprint(log_[i])
            break

troubleshoot_framerange_exceeding_files(combined_mix_max_formatted_written)