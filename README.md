mbed uploader
=============

A script that monitors a directory for .bin files and automatically uploads them to MBED devices.

Works both on Windows and Linux.

#### Dependencies
* watchdog - to install run `pip install watchdog`
    
#### Usage
Substitute for your download directory and MBED drive letter:

`python mbed_uploader.py -i "C:\Users\XXX\Downloads\" -o "H:"`

If pygame is installed then the script can play a bell sound after a successful upload:

`python mbed_uploader.py -i "C:\Users\XXX\Downloads\" -o "H:" -s`
    
#### Known bugs
* Sometimes incorrectly reports failure to upload on Windows.

