!/usr/bin/env python

# ----------------------------------------------------------------------
# Mac Address Changer 
# ----------------------------------------------------------------------


import subprocess
from optparse import OptionParser
import re

color = dict(
    FAIL="\033[91m",
    OKGREEN="\033[92m",
    OKBLUE="\033[94m",
    END="\033[0m",
)


def validateMacAddress(mac_input):
    value = mac_input.replace(":", "")
    if len(value) == 12:
        return True
    else:
        return False


def getParameter():
    parser = OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface name whose Mac needs to be change")
    parser.add_option("-m", "--mac", dest="MAC", help="New mac address")
    (option, args) = parser.parse_args()
    if not option.interface:
        parser.error(f"{color['FAIL']}[-] Please specify Interface Name, For more details try --help {color['END']} ")
    if not option.MAC:
        parser.error(f"{color['FAIL']}[-] Please specify a new MAC , For more details try --help {color['END']} ")
    if not validateMacAddress(option.MAC):
        parser.error(f"{color['FAIL']}[-] Wrong format of MAC Address, MAC address is like XX:XX:XX:XX:XX:XX "
                     f"{color['END']} ")
    return option


def changeMacAddress(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


def getMacAddress(interface):
    ifconfig_result = str(subprocess.check_output(["ifconfig", interface]))
    mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    return mac_address.group(0)


options = getParameter()
old_mac_address = getMacAddress(options.interface)
print(f"{color['OKGREEN']}[-] Changing MAC address from {color['OKBLUE']}" + old_mac_address +
      f"{color['OKGREEN']} to {color['OKBLUE']}" + options.MAC +
      f"{color['OKGREEN']} for Interface {color['OKBLUE']}" + options.interface +
      f"{color['END']}")
changeMacAddress(options.interface, options.MAC)
new_mac_Address = getMacAddress(options.interface)
print(f"{color['OKGREEN']}[-] MAC address successfully changed to {color['OKBLUE']}" + new_mac_Address +
      f"{color['END']}")
