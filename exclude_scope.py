import os, argparse
from argparse import RawTextHelpFormatter

def menu():
    print ("\n")
    print (" _______  ______ _    _   _ ____  _____   ____   ____ ___  ____  _____ ")
    print ("| ____\ \/ / ___| |  | | | |  _ \| ____| / ___| / ___/ _ \|  _ \| ____|")
    print ("|  _|  \  / |   | |  | | | | | | |  _|   \___ \| |  | | | | |_) |  _|  ")
    print ("| |___ /  \ |___| |__| |_| | |_| | |___   ___) | |__| |_| |  __/| |___ ")
    print ("|_____/_/\_\____|_____\___/|____/|_____| |____/ \____\___/|_|   |_____|")
    print ("\n")

def get_cli_arguments():
    parser = argparse.ArgumentParser(description=menu(),formatter_class=RawTextHelpFormatter, usage="sudo python3 exclude_scope.py -f --file <input_filename>\n\nThe following formats are allowed: Single IP, CIDR Mask.\n ")
    parser.add_argument('-f','--file', dest='file', action='store', type=str, help='Source file to create UFW block rules from. Valid Formats: Single IP, CIDR MASK.', required=True)
    args = parser.parse_args()
    return args

def main():
    args = get_cli_arguments()
    input_file = args.file

    ufw_status = "sudo ufw status"

    f = open(input_file,'r')
    try:
        for ip in f:
            # CHANGE THIS COMMAND:
            payload = "ufw deny from any to "+ip.strip()
            os.system(payload)
            print(payload)

    except KeyboardInterrupt:
            print("abborted loop")

    os.system(ufw_status)

main()