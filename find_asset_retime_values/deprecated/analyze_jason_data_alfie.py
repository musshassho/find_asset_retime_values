import json
import os
import glob
import shutil

log1file = 'C:\LOGS\log1_1.json'
log2file = 'C:\LOGS\log2_2.json'

log1 = None
log2 = None

if os.path.isfile(log1file):
    with open(log1file) as data_file:
        log1 = json.loads(data_file.read())
if os.path.isfile(log2file):
    with open(log2file) as data_file:
        log2 = json.loads(data_file.read())

newlog = log1.copy()

for plate, shots in log2.iteritems():
    if not newlog.has_key(plate):
        print plate
        newlog[plate] = dict()
    for shot, values in shots.iteritems():
        # add shots to plate
        newlog[plate][shot] = values

print len(log1.keys())
print len(log2.keys())
print len(newlog.keys())
newlog == log1