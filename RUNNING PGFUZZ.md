
## VM Setup and Running PGFuzz

### Step 1: Import VM and Login

This VM is provided as an .ovf file plus a .vmdk which is supported by virtually every VM host. I reccomend using either VMWare Player (free) or VirtualBox (free).

To import an .ovf file using VMWare Player or VirtualBox, follow these guides:
* [Virtual Box](https://docs.oracle.com/en/virtualization/virtualbox/6.0/user/ovf.html)
* [VMWare Player](https://docs.vmware.com/en/VMware-Workstation-Player-for-Linux/17.0/com.vmware.player.linux.using.doc/GUID-DDCBE9C0-0EC9-4D09-8042-18436DA62F7A.html)


**Login Details**
```
Username: pgfuzz
Password: pgfuzz
```

### 2. Make PX4 and JMavsim

>💡*Efforts to automate running PGFuzz, and data collection are ongoing. For now, please follow these steps.*


> ⚠️
> **Cleaning between runs is required whenever restarting the PX4 after a crash / error / etc. Otherwise PX4/Jmavsim will restart with the drone still in the crashed / errored / etc. state.**

Run the following commands:
```
cd pgfuzz/px4_pgfuzz
make clean distclean
make px4_sitl_default jmavsim
```

Wait until the Jmavsim window appears. It should look like this:
![JmavSim Window](img/image.png)

### 3. Open QGroundControl

Open a new terminal tab/window and run the following command:
`~/Downloads/QGroundControl.AppImage`

The QGroundControl window should now open. There may be scary / confusing log outputs from QGroundControl but these are normal.

### 4. Run Fuzzing

Open a new terminal tab / window and run the following commands
```
cd ~/pgfuzz/PX4
python2 fuzzing.py
```

After a few seconds, fuzzing should start and the drone should move on JMavSim. The flight path of the drone according to the current mission should be visible in QGroundControl:
![Alt text](img/image-1.png)

The mission will eventually finish after a few minutes with the drone remaining in the air. PGFuzz may output an exception on shutdown but this will not affect the data produced.

To start another fuzzing run, repeat steps 2 through 4. 

## Collecting Flight Logs

.Ulg files containing flight logs can be downloaded from QGroundControl.

1. Select the Q icon on the top left of the QGroundControl window
![Alt text](img/image-2.png)

2. Select "Analyze Tools" in the popup menu

3. Select the "Refresh" button on the right hand menu to collect the latest flight logs
![Alt text](img/image-3.png)

4. Select the relevant flight log from the table and click the download button

## Collecting Metadata
Any metadata about the fuzzing run can be found in `~/pgfuzz/PX4/saved_data` 

Each run is identified with a unique ID used to group files belonging to each run. The run ID is outputted in the terminal at completion of a fuzzing run. 

Two files are outputted per fuzzing run:
* (id)_metadata.json
  * Contains the run configuration used by PGFuzz (currently saved in `fuzzing.py`)
* (id)_commands.txt
  * Contains the commands sent to PX4 during the fuzzing run

There is an additional file ulg_mappings.txt that maps the .ulg file end time with the run Id. This should come useful in collecting relevant run data in the future. 



