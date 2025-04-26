import threading
import tkinter as tk
from scapy.layers.http import HTTPRequest, Raw
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP

sniffing_active = False
suspicious_ips = []  # Add suspicious IPs here manually or dynamically
suspicious_ports = [22, 23, 445]  # Example suspicious ports (SSH, Telnet, SMB)

def packet_callback(packet, output_box):
    def update_output_box():
        output_box.config(state=tk.NORMAL)

        suspicious = False
        msg = ""

        if packet.haslayer(IP):
            ip_src = packet[IP].src
            ip_dst = packet[IP].dst
            proto = None
            port_src = ""
            port_dst = ""
            color = "#FFFFFF"

            if packet.haslayer(TCP):
                proto = "TCP"
                port_src = packet[TCP].sport
                port_dst = packet[TCP].dport
                color = "#39FF14"

            elif packet.haslayer(UDP):
                proto = "UDP"
                port_src = packet[UDP].sport
                port_dst = packet[UDP].dport
                color = "#00FFFF"

            elif packet.haslayer(ICMP):
                proto = "ICMP"
                color = "#FF3131"

            else:
                proto = packet.lastlayer().name

            # Build the message with ports
            if proto in ["TCP", "UDP"]:
                msg = f"{ip_src}:{port_src} -> {ip_dst}:{port_dst} | Protocol: {proto} | Length: {len(packet)}"
            else:
                msg = f"{ip_src} -> {ip_dst} | Protocol: {proto} | Length: {len(packet)}"

            # Suspicious detection
            if ip_src in suspicious_ips or ip_dst in suspicious_ips:
                suspicious = True
                msg += " ⚠ Suspicious IP"

            if proto in ["TCP", "UDP"] and (port_src in suspicious_ports or port_dst in suspicious_ports):
                suspicious = True
                msg += " ⚠ Suspicious Port"

            output_box.insert(tk.END, msg + "\n", "SUS" if suspicious else proto)
            output_box.tag_config(proto, foreground=color)
            if suspicious:
                output_box.tag_config("SUS", foreground="#FF4500")

            # --- HTTP Credential Sniffing ---
            if packet.haslayer(HTTPRequest) and packet.haslayer(Raw):
                try:
                    http_payload = packet[Raw].load.decode(errors="ignore")
                    if any(keyword in http_payload.lower() for keyword in ["username", "user", "login", "email", "pass", "password"]):
                        output_box.insert(tk.END, f"🔐 Possible credentials in HTTP POST: {http_payload}\n", "CRED")
                        output_box.tag_config("CRED", foreground="#FFD700")
                except Exception as e:
                    print(f"Decode error: {e}")

        elif packet.haslayer(ARP):
            output_box.insert(tk.END, f"ARP Packet: {packet.summary()}\n", "ARP")
            output_box.tag_config("ARP", foreground="#FFA500")

        else:
            output_box.insert(tk.END, f"Other Packet: {packet.summary()}\n", "OTHER")
            output_box.tag_config("OTHER", foreground="#AAAAAA")

        output_box.config(state=tk.DISABLED)

    # Schedule the update of the GUI in the main thread
    output_box.after(0, update_output_box)

# Start sniffing packets
def start_sniffer(output_box):
    """Function to start packet sniffing."""
    global sniffing_active
    sniffing_active = True

    def stop_condition(packet):
        return not sniffing_active

    sniff(prn=lambda packet: packet_callback(packet, output_box), store=False, stop_filter=stop_condition)

# Stop sniffing packets
def stop_sniffer():
    """Function to stop packet sniffing."""
    global sniffing_active
    sniffing_active = False
    print("Sniffer stopped.")  # Or you can use a more elegant method to stop sniffing

# Toggle sniffing functionality
def toggle_sniffer(output_box):
    """Toggle the sniffer's start/stop functionality."""
    global sniffing_active
    if sniffing_active:
        stop_sniffer()
    else:
        # Start sniffer in a new thread so the GUI doesn't freeze
        threading.Thread(target=start_sniffer, args=(output_box,), daemon=True).start()
    return sniffing_active
