# Routerkonfigurasjon med Ansible

## Forutsetninger
- Ansible installert (versjon 2.9 eller nyere)
- Python 3.x
- Cisco IOS Collection (`ansible-galaxy collection install cisco.ios`)
- Seriell tilgang til router for første oppsett

## Filstruktur
```
router_config/
├── ansible.cfg
├── inventory.ini
├── python_scripts/
│   └── configure_router.py
├── playbooks/
│   ├── base_config.yml
│   └── dhcp.yml
└── vars/
    └── router_vars.yml
```

## Kommandoer for konfigurasjon

### Første oppsett via seriellport
```bash
python3 python_scripts/configure_router.py --port /dev/ttyUSB0
```
*Merk:* Bytt `/dev/ttyUSB0` med riktig port (f.eks. `COM3` på Windows)

### Ansible-konfigurasjon
```bash
# Grunnleggende oppsett
ansible-playbook -i inventory.ini playbooks/base_config.yml

# DHCP-konfigurasjon
ansible-playbook -i inventory.ini playbooks/dhcp.yml
```

## Konfigurasjonsfiler

### inventory.ini
```ini
[routers]
router1 ansible_host=192.168.1.1

[all:vars]
ansible_user=admin
ansible_password=cisco123
ansible_connection=ansible.netcommon.network_cli
ansible_network_os=ios
```

### router_vars.yml
```yaml
dhcp_pools:
  - name: VLAN10
    network: 192.168.10.0
    gateway: 192.168.10.1
    dns: [8.8.8.8, 8.8.4.4]

ospf_networks:
  - network: 192.168.0.0
    mask: 0.0.255.255
    area: 0
```

## Verifisering
Etter konfigurasjon, kjør følgende på routeren:
```
show running-config
show ip dhcp pool
show ip ospf interface
```
