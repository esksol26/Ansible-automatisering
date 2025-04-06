#!/usr/bin/env python3
import serial
import time
import argparse

def send_config(ser, commands, delay=0.5):
    for cmd in commands:
        ser.write(f"{cmd}\n".encode())
        time.sleep(delay)
        print(f"Executed: {cmd}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Serial port (COM3 or /dev/ttyS0)")
    args = parser.parse_args()

    try:
        ser = serial.Serial(args.port, baudrate=9600, timeout=1)
        time.sleep(2)

        config = [
            "enable",
            "configure terminal",
            # VLAN & Subinterfaces
            "interface Gig0/1.10", "encapsulation dot1Q 10", "ip address 192.168.10.1 255.255.255.0",
            "interface Gig0/1.20", "encapsulation dot1Q 20", "ip address 192.168.20.1 255.255.255.0",
            # DHCP
            "ip dhcp pool VLAN10", "network 192.168.10.0 255.255.255.0", "default-router 192.168.10.1", "exit",
            "ip dhcp excluded-address 192.168.10.1 192.168.10.10",
            # OSPF
            "router ospf 1", "network 192.168.0.0 0.0.255.255 area 0",
            # HSRP
            "interface Gig0/1.10", "standby 10 ip 192.168.10.254", "standby 10 priority 110",
            "end", "write memory"
        ]

        send_config(ser, config)
        print("\n✅ Router configuration complete!")
    finally:
        ser.close()

if __name__ == "__main__":
    main()