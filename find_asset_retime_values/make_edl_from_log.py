import json
import os
from timecode_converter import TimecodeConverter
tc = TimecodeConverter.TimecodeConverter(24)

# json file
minmaxvals = '//fbbblue/TEMP/_Boris_Exchange/Logs/formatted_json_logs/combined_logs_min_max_formatted_values_in_range_02.json'

# excel sheet exported as csv
datacsv = '//fbbblue/TEMP/_Boris_Exchange/Logs/BB_PlatesFromShoot_Total_toFBB_180525.txt'

# out edls
movedlfile = '//fbbblue/TEMP/_Boris_Exchange/Logs/temp/movedl.edl'
takeedlfile = '//fbbblue/TEMP/_Boris_Exchange/Logs/temp/takeedl.edl'

values = None
if os.path.isfile(minmaxvals):
    with open(minmaxvals) as data_file:
        values = json.loads(data_file.read())

csvvalues = list()
csvfile = open(datacsv)
for line in csvfile.readlines():
    csvvalues.append(line)
csvfile.close()

movedlentries = dict()
takeedlentries = dict()
edit_in = '00:00:00:00'
edit_out = '00:00:00:00'
missing = list()
for csvval in csvvalues:
    items = csvval.split(',')
    mov = items[2]
    take = items[3]
    src_frame_in = int(items[7])
    src_frame_out = int(items[8])
    if not values.has_key(mov):
        missing.append('%s - %s' % (take, mov))
        continue
    v = values[mov]
    source_in = tc.frames_to_timecode(src_frame_in + v['min'] - 10)
    source_out = tc.frames_to_timecode(src_frame_in + v['max'] + 10)
    edit_out = tc.frames_to_timecode(tc.timecode_to_frames(edit_in) + v['max'] - v['min'] + 20)
    spaces = 33-len(mov)
    movedlentry = '  %s%sV     C        %s %s %s %s \n' % (mov, ' ' * spaces, source_in, source_out, edit_in, edit_out)
    movedlentries[tc.timecode_to_frames(edit_in)] = movedlentry
    spaces = 33-len(take)
    takeedlentry = '  %s%sV     C        %s %s %s %s \n' % (take, ' ' * spaces, source_in, source_out, edit_in, edit_out)
    takeedlentries[tc.timecode_to_frames(edit_in)] = takeedlentry
    edit_in = edit_out

# add title and numbers to EDL
movedl = 'TITLE:   180530_test\nFCM: NON-DROP FRAME\n'
takeedl = 'TITLE:   180530_test\nFCM: NON-DROP FRAME\n'
counter = 1
for timecode, value in sorted(movedlentries.iteritems()):
    entry_numbered = '%06d%s' % (counter, value)
    movedl += entry_numbered
    counter += 1
counter = 1
for timecode, value in sorted(takeedlentries.iteritems()):
    entry_numbered = '%06d%s' % (counter, value)
    takeedl += entry_numbered
    counter += 1

# write EDLs
outfile = open(movedlfile, 'w')
outfile.write(movedl)
outfile.close()

outfile = open(takeedlfile, 'w')
outfile.write(takeedl)
outfile.close()

# check if any of the keys are not in the excel file
notinexcel = list()
for key in values.keys():
    keyfound = False
    for csvval in csvvalues:
        items = csvval.split(',')
        mov = items[2]
        if mov == key:
            keyfound = True
    if not keyfound:
        notinexcel.append(key)

for n in notinexcel:
    print n