Her er en komplett **README.md for switchkonfigurasjon** med Python-skriptet integrert og tilpasset ditt eksisterende oppsett:

---

# Switch Konfigurasjon med Ansible og Python

## Forutsetninger
- Ansible installert
- Python 3.x med `pyserial` bibliotek (`pip install pyserial`)
- Seriell tilgang til switch (konsollkabel)
- SSH tilgang etter første oppsett

## Filstruktur
```
switch_config/
├── ansible.cfg
├── inventory.ini
├── Setup_ssh.py          # Python-skript for førstegangsoppsett
├── playbooks/
│   ├── switch_setup.yml  # Ansible playbook
└── vars/
    └── switch_vars.yml   # VLAN og portkonfigurasjon
```

## 1. Førstegangsoppsett med Python

Kjør dette skriptet via seriellport for å aktivere SSH:

```python
import serial
import time

# Konfigurer disse verdiene
ser_port = "COM3"               # Endre til riktig port (f.eks. /dev/ttyUSB0 på Linux)
username = "admin"
password = "cisco123"
ip_address = "192.168.1.2"
subnet_mask = "255.255.255.0"

# Åpner seriell tilkobling
ser = serial.Serial(ser_port, baudrate=9600, timeout=1)
time.sleep(1)

# Konfigurasjonskommandoer
commands = [
    "enable",
    "configure terminal",
    "hostname Switch1",
    "interface vlan 1",
    f"ip address {ip_address} {subnet_mask}",
    "no shutdown",
    "exit",
    f"username {username} privilege 15 secret {password}",
    "ip domain-name lokalnet.local",
    "crypto key generate rsa",
    "2048",  # RSA-nøkkelstørrelse
    "ip ssh version 2",
    "line vty 0 4",
    "login local",
    "transport input ssh",
    "exit",
    "write memory"
]

# Utfører konfigurasjon
for cmd in commands:
    ser.write(f"{cmd}\n".encode())
    time.sleep(0.5)

ser.close()
print("\n✅ SSH er nå aktivert på switchen!")
```

**Kjør slik:**
```bash
python3 Setup_ssh.py
```

## 2. Ansible-konfigurasjon

### inventory.ini
```ini
[switches]
switch1 ansible_host=192.168.1.2 ansible_user=admin ansible_password=cisco123

[switches:vars]
ansible_connection=ansible.netcommon.network_cli
ansible_network_os=cisco.ios.ios
```

### Kjør playbook
```bash
ansible-playbook -i inventory.ini playbooks/switch_setup.yml
```

## Verifisering
Kjør på switchen:
```
show ip interface brief
show vlan brief
show running-config
```

---

**Tips:**  
- For Windows: Bytt `COM3` til riktig seriellport  
- For Linux: Sjekk port med `ls /dev/tty*`  
- Vent 1-2 minutter etter SSH-oppsett før Ansible-kjøring  
