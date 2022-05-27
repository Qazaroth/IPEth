import subprocess

try:
    import netifaces
except ModuleNotFoundError:
    subprocess.run(["pip install netifaces"])

import winreg
import os

separator = "=" * 66

def clear():
    command = "clear"
    if os.name in ("nt", "dos"):  # If Machine is running on Windows, use cls
        command = "cls"

    os.system(command)

def getConnectionNameFromGUID(ifaceGuids):
    ifaceNames = ["(Unknown)" for i in range(len(ifaceGuids))]
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    reg_key  = winreg.OpenKey(reg, r"SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}")

    for i in range(len(ifaceGuids)):
        try:
            reg_subkey = winreg.OpenKey(reg_key, ifaceGuids[i] + r"\Connection")
            ifaceNames[i] = winreg.QueryValueEx(reg_subkey, "Name")[0]
        except FileNotFoundError:
            pass
    
    return ifaceNames

netInterfaces = netifaces.interfaces()
netInterfaceStr = getConnectionNameFromGUID(netInterfaces)

clear()

def main():
    print(separator)
    print("List of Network Interface Cards. (Physical and VM Included)")
    print(separator)
    for a in netInterfaceStr:
        if a.lower() != "(unknown)":
            index = netInterfaceStr.index(a)
            print("{} - {}".format(index, a))
    print(separator)
    choice = input("Select a Network Interface Card (Numerical): ")

    try:
        choice = int(choice)
    except ValueError:
        print("Invalid choice.")

    if isinstance(choice, int):
       if choice >= 0 and choice < len(netInterfaces):
            nic = netInterfaces[choice]
            nicName = netInterfaceStr[choice]

            if nicName.lower() != "(unknown)":
                try:
                    ip = netifaces.ifaddresses(nic)[netifaces.AF_INET]
                except KeyError:
                    print("Error occured trying to retrieve NIC ({}), maybe it's not used or disabled.".format(nicName))
                else:
                    if len(ip) > 0:
                        ip = ip[0].get("addr", "0.0.0.0")
                        print("IP Address for Interface {} ({}): {}".format(nicName, nic, ip))
                    else:
                        print("NIC ({}) provided with no data!".format(nicName))

main()
