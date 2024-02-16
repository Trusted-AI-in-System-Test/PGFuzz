import os
import json
import shutil
from datetime import datetime
from subprocess import call

SAVE_PATH = "./saved_data"
ISILON_PATH = "/mnt/isilon/PGFuzz_Runs"

def _create_save_dir(test_id):
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    
    if not os.path.exists(SAVE_PATH + "/" + test_id):
        os.mkdir(SAVE_PATH + "/" + test_id)

def extract_ulg(test_id, output_folder):
    # Find most recently created ulg i.e. the one created from the most recent (our) run
    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%Y-%m-%d")
    filepath = "/home/pgfuzz/pgfuzz/px4_pgfuzz/build/px4_sitl_default/rootfs/log/" + current_day
    files = [os.path.join(filepath, f) for f in os.listdir(filepath)]

    ulg_file_path =  max(files, key=os.path.getmtime)
    ulg_copy_location = SAVE_PATH + "/" + test_id + "/run_log.ulg"
    shutil.copyfile(ulg_file_path, ulg_copy_location)   
    
    command = "ulog2csv " + ulg_copy_location + " -o " + SAVE_PATH + "/" + test_id + "/" + output_folder
    call(command, shell=True)

    os.remove(ulg_copy_location)


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

    print("Saving commands and run metadata")   
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
    
    print("Saving ULG file")
    extract_ulg(test_id, "ulg_logs")

    current_day = current_datetime.strftime("%Y-%m-%d")

    if not metadata["copy_to_isilon"]:
        return
    
    if not os.path.isdir(ISILON_PATH):
        print("***CANNOT SAVE TO ISILON - ISILON SHARE IS NOT MOUNTED")
        print("Have you made sure to add your username and password to /etc/fstab?")
        return
    
    isilon_save_path = ISILON_PATH + "/" + current_day + "/" + test_id
    print(isilon_save_path)
    shutil.copytree(SAVE_PATH + "/" + test_id, isilon_save_path)