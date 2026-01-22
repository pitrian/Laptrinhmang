from scapy.all import IP, TCP, sr1, RandShort

TARGET = "172.16.30.1"
DPORT = 80   # thử 80, nếu no response thì thử 443

print(f"[+] Sending TCP SYN to {TARGET}:{DPORT}")
pkt = IP(dst=TARGET)/TCP(sport=RandShort(), dport=DPORT, flags="S")

ans = sr1(pkt, timeout=2, verbose=False)
if ans:
    print("[+] Response:", ans.summary())
    if ans.haslayer(TCP):
        flags = ans[TCP].flags
        if flags == 0x12:
            print("[+] OPEN (SYN-ACK)")
        elif flags == 0x14:
            print("[+] CLOSED (RST-ACK)")
        else:
            print("[*] Flags:", flags)
else:
    print("[-] No response (may be filtered by firewall/router)")
