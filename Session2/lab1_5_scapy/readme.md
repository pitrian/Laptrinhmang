# Lab 1.5 – Packet Crafting with Scapy

## ICMP Packet Crafting
- Sent ICMP Echo Request to 172.16.30.1
- Received Echo Reply successfully

## TCP SYN Packet Crafting
- Sent TCP SYN to 172.16.30.1:80
- No response observed (likely filtered by firewall/router)

## Packet Sniffing and Filtering
- Captured ICMP packets using Scapy sniff()
- BPF filter: icmp
- Observed echo-request and echo-reply packets in real time
