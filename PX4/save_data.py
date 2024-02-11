import os
import json
from datetime import datetime

SAVE_PATH = "./saved_data"

def _create_save_dir(test_id):
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    
    if not os.path.exists(SAVE_PATH + "/" + test_id):
        os.mkdir(SAVE_PATH + "/" + test_id)

def dump_command_log(filename, test_id):
    _create_save_dir(test_id)
    
    filename = SAVE_PATH + "/" + test_id + "/" + filename
    f1 = open("mutated_log.txt", "r")
    lines = f1.readlines()

    f2 = open(filename, "w")
    f2.writelines(lines)
    f1.close()
    f2.close()

    mutated_log = open("mutated_log.txt", "w")
    mutated_log.close()

def save_run_information(test_id, metadata):
    _create_save_dir(test_id)
    
    current_datetime = datetime.now()
    ulg_end_time = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")

    # Save metadata file
    with open(SAVE_PATH + "/" + test_id + "/metadata.json", 'w+') as json_file:
        json.dump(metadata, json_file)
    
    # Save commands file
    file_name = "commands.txt"
    dump_command_log(file_name, test_id)

    # Update ulg file mappings
    mapping_file = open(SAVE_PATH + "/ulg_mappings.txt", "a")
    mapping_file.write("\ntest_id: "+test_id+" - ulg_end_time: "+ ulg_end_time)
    mapping_file.close()
        