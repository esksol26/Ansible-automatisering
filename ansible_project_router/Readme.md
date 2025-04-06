# Konfigurasjonsguide for Cisco Router

## Nødvendige filer

### ansible.cfg
```ini
[defaults]
inventory = ./inventory          # Peker til inventory-mappen
host_key_checking = False        # Slår av SSH host key verifisering
timeout = 30                     # Timeout for Ansible-operasjoner
```

### inventory/routers.ini
```ini
[routers]
router1 ansible_host=192.168.1.1 ansible_user=admin ansible_password=cisco123

# Variabler som gjelder for alle routere
[routers:vars]
ansible_connection=ansible.netcommon.network_cli  # Bruker network_cli for Cisco-enheter
ansible_network_os=cisco.ios.ios                  # Spesifiserer IOS som operativsystem
```

### python_scripts/configure_router.py
```python
import serial
import time

def configure_router(port):
    try:
        # Åpner seriell tilkobling til routeren
        ser = serial.Serial(port, baudrate=9600, timeout=1)
        time.sleep(2)  # Vent på at tilkoblingen er stabil
        
        # Liste med konfigurasjonskommandoer
        commands = [
            "enable",                       # Går inn i enable-modus
            "configure terminal",           # Går inn i konfigurasjonsmodus
            "hostname ROUTER1",             # Setter hostname
            "ip domain-name example.com",   # Setter domenenavn for SSH
            "crypto key generate rsa modulus 2048",  # Generer SSH-nøkler
            "ip ssh version 2",             # Aktiverer SSH versjon 2
            "line vty 0 4",                 # Konfigurer virtuell terminallinjer
            "login local",                  # Krever lokal autentisering
            "transport input ssh",          # Tillater kun SSH-tilgang
            "end",                          # Avslutter konfigurasjonsmodus
            "write memory"                  # Lagrer konfigurasjonen
        ]
        
        # Sender alle kommandoene en etter en
        for cmd in commands:
            ser.write(f"{cmd}\n".encode())
            time.sleep(0.5)  # Kort pause mellom hver kommando
            
    finally:
        ser.close()  # Lukker alltid seriell tilkobling

# Kjører konfigurasjonen på standard seriellport
configure_router("/dev/ttyUSB0")  # Bytt til COM3 på Windows
```

### playbooks/01_base_config.yml
```yaml
---
- name: Grunnleggende routerkonfigurasjon
  hosts: routers  # Kjører på alle routere definert i inventory
  gather_facts: no  # Slår av facts-samling for raskere kjøring

  tasks:
    - name: Sett hostname
      cisco.ios.ios_hostname:
        hostname: "{{ inventory_hostname }}"  # Bruker inventory hostname
      tags: hostname  # Gir mulighet til å kjøre kun denne oppgaven
```

### playbooks/02_dhcp.yml
```yaml
---
- name: DHCP-konfigurasjon
  hosts: routers
  gather_facts: no
  vars_files:
    - ../vars/router_vars.yml  # Inkluderer DHCP-variabler

  tasks:
    - name: Konfigurer DHCP-pooler
      cisco.ios.ios_config:
        lines: |  # Multilinje-kommandoer for DHCP
          ip dhcp pool {{ item.name }}
          network {{ item.network }}
          default-router {{ item.gateway }}
          dns-server {{ item.dns | join(' ') }}
        loop: "{{ dhcp_pools }}"  # Gjentar for hver DHCP-pool
      tags: dhcp  # Lar deg kjøre kun DHCP-oppsett
```

### vars/router_vars.yml
```yaml
# DHCP-konfigurasjon
dhcp_pools:
  - name: VLAN10  # Navn på DHCP-pool
    network: 192.168.10.0  # Nettverk som skal servieres
    gateway: 192.168.10.1  # Standard gateway for klienter
    dns: [8.8.8.8, 8.8.4.4]  # DNS-servere
```

## Bruksanvisning

1. **Første konfigurasjon via seriellport:**
```bash
python3 python_scripts/configure_router.py
```

2. **Kjør Ansible-playbooks:**
```bash
# Grunnleggende konfigurasjon
ansible-playbook -i inventory/routers.ini playbooks/01_base_config.yml

# DHCP-konfigurasjon
ansible-playbook -i inventory/routers.ini playbooks/02_dhcp.yml
```

3. **Valgfritt: Kjør spesifikke deler med tags:**
```bash
ansible-playbook -i inventory/routers.ini playbooks/02_dhcp.yml --tags dhcp
```

## Viktige notater

- Endre IP-adresser og passord i inventory-filen før bruk
- På Windows-systemer, bytt "/dev/ttyUSB0" med riktig COM-port (f.eks. "COM3")
- For feilsøking, legg til "-vvv" for detaljert logging