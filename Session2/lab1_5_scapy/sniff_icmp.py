from scapy.all import sniff

IFACE = "Wi-Fi"  # nếu show_interfaces tên khác thì đổi đúng y vậy

def show(pkt):
    print(pkt.summary())

print(f"[*] Sniffing ICMP on iface: {IFACE} (capture 10 packets)")
print("    Now run: ping 172.16.30.1 in another terminal")

sniff(iface=IFACE, filter="icmp", prn=show, store=False, count=10)
