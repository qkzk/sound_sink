#! /usr/bin/python

"""
title: Change sound sink from command line easily
author: qkzk
date: 2022/08/20

source: 
https://askubuntu.com/questions/14077/how-can-i-change-the-default-audio-device-from-command-line
"""

import subprocess
import sys

HELP = """Change your sound sink from command line.

usage :

sound_sink DEVICE

where DEVICE in ["corsair", "analog"]
"""


def get_pacmd_sinks() -> str:
    """
    Returns a filtered output of `pacmd list-sinks`.
    We filter the lines to only keep name and index.
    Returned output looks like :

    * index: 0
          name: <alsa_output.pci-0000_00_1f.3.analog-stereo>
      index: 5
          name: <alsa_output.usb-Corsair_CORSAIR_HS70_Pro_Wireless_Gaming_Headset-
      index: 20
          name: <alsa_output.pci-0000_03_00.1.hdmi-stereo>

    """

    p = subprocess.Popen(
        'pacmd list-sinks | grep -e "name:" -e "index:"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    return p.stdout.read().decode("utf-8")


def extract_sink_indexes(sink_string: str, device) -> int:
    """
    Iterate through pacmd output looking for the required device.
    Since the index one line above the name.
    """
    lines = sink_string.splitlines()
    i = 0
    while i < len(lines):
        if device.lower() in lines[i].lower():
            return int(lines[i - 1].split("index:")[1].strip())
        i += 1
    return -1


def change_sink(index: int) -> None:
    """
    Change the sound sink to the given device index.
    Print the stderr if any.
    """
    p = subprocess.Popen(
        f"pacmd set-default-sink {index}",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p_stderr = p.stderr.read()
    if p_stderr:
        print(p_stderr.decode("utf-8"))
    p_stdout = p.stdout.read()


def main():
    """
    Main program.
    if no argument is given, print help and exit 1.
    if the device is found, change to it.
    Else exit 2.
    """
    if len(sys.argv) == 1:
        print(HELP)
        exit(1)
    required_device = sys.argv[1]
    sink_string = get_pacmd_sinks()
    # print(sink_string)
    required_index = extract_sink_indexes(sink_string, required_device)
    # print(required_index)
    if required_device == -1:
        print(f"Device {required_device} unknown")
        print("known devices :")
        print(sink_string)
        print(HELP)
        exit(2)
    print(f"Found sink {required_device}, index {required_index}")
    change_sink(required_index)
    print(f"Changed sink to {required_device}, index {required_index}")


if __name__ == "__main__":
    main()
