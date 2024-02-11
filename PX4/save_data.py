import os
import json
from datetime import datetime

def _create_save_dir():
    if not os.path.exists("./saved_data"):
        os.mkdir("./saved_data")

def dump_command_log(filename):
    _create_save_dir()
    
    filename = "./saved_data/" + filename
    f1 = open("mutated_log.txt", "r")
    lines = f1.readlines()

    f2 = open(filename, "w")
    f2.writelines(lines)
    f1.close()
    f2.close()

    mutated_log = open("mutated_log.txt", "w")
    mutated_log.close()

def save_run_information(test_id, metadata):
    _create_save_dir()

    current_datetime = datetime.now()
    ulg_end_time = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

    # Save metadata file
    with open("./saved_data/"+test_id+"_metadata.json", 'w+') as json_file:
        json.dump(metadata, json_file)

    # Save commands file
    file_name = test_id+"_commands"
    file_name += ".txt"
    dump_command_log(file_name)

    # Update ulg file mappings
    mapping_file = open("./saved_data/ulg_mappings.txt", "a")
    mapping_file.write("\ntest_id: "+test_id+" - ulg_end_time: "+ulg_end_time)
    mapping_file.close()
        