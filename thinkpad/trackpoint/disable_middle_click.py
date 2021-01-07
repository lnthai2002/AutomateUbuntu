import re
import subprocess

trackpoint_names = ("TPPS/2 IBM TrackPoint", "ThinkPad Compact Bluetooth Keyboard with TrackPoint")
unmodified_trackpoint_buttons = "1 2 3 4 5 6 7"
device_id_pattern = r"^.*id=(\d*).*"


def trackpoint_should_be_modified(device_id):
    result = subprocess.run(["xinput", "get-button-map", device_id], capture_output=True)
    buttons = result.stdout.decode("utf-8").strip()
    if result.returncode == 0 and buttons == unmodified_trackpoint_buttons:
        return True
    return False


def modify_trackpoint(device_id):
    print(f"Disabling middle button of device {device_id}")
    # xinput only change the first values provided
    subprocess.run(["xinput", "set-button-map", device_id, "1", "0", "3"])


def lookup_unmodified_trackpoint_id(device_name, id_regex):
    print(f'Looking for device {device_name}')

    found = []
    result = subprocess.run(["xinput", "list"], capture_output=True)
    for line in result.stdout.splitlines(False):
        utf8line = line.decode('utf-8')  # because stdout return bytes
        if device_name in utf8line:
            matched = id_regex.match(str(utf8line))
            if matched:
                found.append(matched.group(1))
    return found


device_id_regex = re.compile(device_id_pattern)
for trackpoint_name in trackpoint_names:
    device_ids = lookup_unmodified_trackpoint_id(trackpoint_name, device_id_regex)
    for device_id in device_ids:
        if trackpoint_should_be_modified(device_id):
            modify_trackpoint(device_id)
        else:
            print(f"No modification done for device {device_id}")
