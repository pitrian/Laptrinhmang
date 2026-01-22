from scapy.all import IP, ICMP, sr1

IFACE = "Wi-Fi"          # interface Wi-Fi của bạn
TARGET = "172.16.30.1"   # Default Gateway

print(f"[+] ICMP ping to {TARGET} via {IFACE}")

pkt = IP(dst=TARGET)/ICMP()
ans = sr1(pkt, timeout=2, verbose=False, iface=IFACE)

if ans:
    print("[+] Reply:", ans.summary())
else:
    print("[-] Timeout")
