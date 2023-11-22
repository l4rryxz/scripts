import os, argparse
from argparse import RawTextHelpFormatter

def menu():
    print ("\n")
    print (" _     ___   ___  ____  ")
    print ("| |   / _ \ / _ \|  _ \ ")
    print ("| |  | | | | | | | |_) |")
    print ("| |__| |_| | |_| |  __/ ")
    print ("|_____\___/ \___/|_|    ")
    print ("\n")

def get_cli_arguments():
    parser = argparse.ArgumentParser(description=menu(),formatter_class=RawTextHelpFormatter, usage="python loop_command.py -f --file <input_filename> -c --command a custom command to run")
    parser.add_argument('-f','--file', dest='file', action='store', type=str, help='reference a source file as input for the command to loop trough', required=True)
    #parser.add_argument('-c','--command', dest='file', action='store', type=str, help='example command: ping -c 1 {ip}', required=True)
    args = parser.parse_args()
    return args

def main():
    args = get_cli_arguments()
    input_file = args.file

    f = open(input_file,'r')
    try:
        for ip in f:
            # CHANGE THIS COMMAND:
            payload = "snmpbulkwalk -c public -v 2c "+ip.strip()+" . > "+ip.strip()+".log"
            os.system(payload)
            print(payload)

    except KeyboardInterrupt:
            print("abborted loop")

main()
