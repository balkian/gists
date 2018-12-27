from scapy.all import *
from yeelight import Bulb

MAC_ADDRESS = 'ac:63:be:52:8b:4a' # enter Dash Button's MAC Address here.

on = False
b = Bulb('192.168.2.240')

def detect_button(pkt):
    print(pkt[Ether].src)
    if pkt.haslayer(DHCP) and pkt[Ether].src == MAC_ADDRESS:
        global on
        print("Button Press Detected")
        if on:
            b.turn_off()
        else:
            b.turn_on()
        on = on ^ True
        #Do stuff

sniff(prn=detect_button, filter="(udp and (port 67 or 68))", store=0)
