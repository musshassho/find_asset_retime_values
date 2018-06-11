# IMPORTS
import os
import json
# import nuke
import re

# CONSTANTS

PATH = "//fbbblue/00_jobs/baj_benjamin/prod/plates/footage_vfx_plates/vfx_plates_QTref/Generic Plate11-01 B.mov"
MOV = "Generic Plate11-01 B.mov"
MOV = "004_05-01 A MOS.mov"
LOGS = "C:\LOGS"


# HELPER FUNCTIONS

def confirm_filename(node, path):
    filename = get_file_name(node)
    return filename in path


def confirm_supplied_filename(asset_filename, path):
    filename = asset_filename
    # print filename
    return filename in path


def get_json(path):
    path = "{}".format(path)

    if not os.path.exists(path):
        os.makedirs(path)

    jason_path = "{}\log.json".format(path)

    if not os.path.exists(jason_path):
        data = {}
    else:
        _file = open(jason_path, "r")
        data = json.load(_file)

    return data, jason_path


def write_jason(mov_file, shot, in_, out_, path):
    jason = get_json(LOGS)
    data = jason[0]
    json_path = jason[1]
    # data[mov_file] = {shot: [in_, out_]}
    if data.get(mov_file):
        data[mov_file][shot] = [in_, out_]

    else:
        data[mov_file] = {shot: [in_, out_]}

    with open(json_path, "w") as f:
        json.dump(data, f)


# MAIN FUNCTIONS
script_path = nuke.root()['name'].value()
print script_path


def find_upstream_reads(asset_filename, nd_input=nuke.selectedNode()):
    global movfile
    movfile = asset_filename
    # print movfile
    retime_node = nuke.selectedNode().name()

    script_first_frame = int(nuke.root()['first_frame'].value())
    script_last_frame = int(nuke.root()['last_frame'].value())

    script_path = nuke.root()['name'].value()
    regex = re.search(r"//fbbblue/00_jobs/baj_benjamin/prod/work/shots/(\w+)_(\d+)/(\d+)", script_path)
    if regex:
        shot = "{}_{}_{}".format(regex.group(1), regex.group(2), regex.group(3))

    length = script_last_frame - script_first_frame

    if nuke.toNode(retime_node).Class() == "Retime":
        global out_first
        out_first = int(nuke.toNode(retime_node)["output.first"].value())
        out_last = int(nuke.toNode(retime_node)["output.last"].value())

    # print "OUT FIRST: ", out_first

    dep_node = nuke.dependencies(nuke.selectedNode())
    type = dep_node[0].Class()
    name = dep_node[0].name()

    nuke.selectedNode()['selected'].setValue(False)

    if type == "Read":
        read_name = dep_node[0].name()
        # print "read_name: ", read_name
        read_node = nuke.toNode(read_name)
        file = read_node["file"].value()
        # print file

        if confirm_supplied_filename(movfile, file):
            read_node['selected'].setValue(True)
            # offset_value = script_first_frame - out_first
            SHOT = shot
            IN = abs(out_first - script_first_frame)
            OUT = IN + length
            print "SHOT: ", shot
            print "IN: ", IN
            print "OUT: ", OUT
            return shot, IN, OUT

    else:
        sel = nuke.toNode(name)['selected'].setValue(True)
        x = find_upstream_reads(movfile, sel)
        sel = nuke.toNode(name)['selected'].setValue(False)
        return x


def iterate_retime_nodes(asset_filename):
    try:
        retime_nodes = nuke.allNodes("Retime")
        for node in retime_nodes:
            retime = nuke.toNode(node.name())['selected'].setValue(True)
            search = find_upstream_reads(asset_filename, retime)
            return search
    except:
        print "no Retime Node Found"


def caller_function(mov_file):
    data = iterate_retime_nodes(mov_file)
    mov_file = mov_file
    shot = data[0]
    in_ = data[1]
    out_ = data[2]
    path = get_json(LOGS)[1]
    write_jason(mov_file, shot, in_, out_, path)
    return "mission completed"


def analyze_data(path):
    in_points = []
    out_points = []
    data = get_json(path)[0]
    for i in data.keys():
        for e in d[i]:
            in_ = d[i][e][0]
            out_ = d[i][e][1]
            in_points.append(in_)
            out_points.append(out_)
    min_in = min(in_points)
    max_out = max(out_points)
    return min_in, max_out


# FUNCTION CALLS

print caller_function(MOV)


