#!/bin/bash

target="$1"
echo "Running first full tcp port scan (-p-) against: $taregt"
ports=$(nmap -p- --min-rate 1000 "$target" -v -oA full_port_scan | grep "^ *[0-9]" | grep "open" | cut -d '/' -f 1 | tr '\n' ',' | sed 's/,$//')

echo "Running second nmap service scan (-sC -sV -A) on open ports: $ports"
nmap -p "$ports" -sC -sV -A "$target" -v -oA service_scan

echo "Running UDP Scan (-sU --top-ports 1000) against: $target"
nmap -sU --top-ports 1000 "$target" -v -oA udp_top-1000

echo "Running third nmap vuln scan (-sV --script 'vuln') on open ports: $ports"
nmap -p "$ports" -sV --script "vuln" "$target" -v  -oA vuln_scan
