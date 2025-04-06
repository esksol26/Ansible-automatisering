# README - Cisco Switch Konfigurasjon

## Innholdsfortegnelse
1. [Forutsetninger](#forutsetninger)
2. [Filstruktur](#filstruktur)
3. [Brukerguide](#brukerguide)
4. [Variabeltilpasning](#variabeltilpasning)
5. [Feilsøking](#feilsøking)

## Forutsetninger

Før du starter, sørg for at du har følgende installert:
- Ansible (versjon 2.9 eller nyere)
- Python 3.x
- Cisco IOS Collection for Ansible (`ansible-galaxy collection install cisco.ios`)

## Filstruktur

```
cisco_switch/
├── ansible.cfg               # Ansible konfigurasjon
├── inventory.ini            # Enhetsliste og tilgangsinformasjon
├── switch_setup.yaml        # Hovedplaybook for switchkonfigurasjon
├── test_ios.yaml            # Testplaybook for tilkobling
└── vars/
    └── switch_vars.yaml     # Variabler for switchkonfigurasjon
```

## Brukerguide

### 1. Test tilkobling til switch

Før full konfigurasjon, test tilkoblingen med:

```bash
ansible-playbook -i inventory.ini test_ios.yaml
```

Forventet output viser switchens versjonsinformasjon.

### 2. Kjør full konfigurasjon

```bash
ansible-playbook -i inventory.ini switch_setup.yaml
```

Denne kommandoen vil utføre:
- Sett hostname
- Opprette VLAN-er
- Konfigurere tilknyttede porter

### 3. Verifiser konfigurasjon

Logg inn på switchen manuelt og kjør:
```
show vlan brief
show interfaces status
```

## Variabeltilpasning

Rediger `vars/switch_vars.yaml` for å tilpasse konfigurasjonen:

```yaml
# Eksempel på VLAN-definisjoner
vlan_config:
  - vlan_id: 10               # VLAN ID
    name: VLAN10              # VLAN navn
    state: active             # VLAN status

# Eksempel på portkonfigurasjon
l2_interfaces:
  - name: GigabitEthernet1/0/1  # Portnavn
    mode: "access"              # Portmodus (access/trunk)
    access:
      vlan: 10                 # Tilknyttet VLAN for access-port
```

## Feilsøking

### Vanlige problemer og løsninger

1. **Tilkoblingsfeil**:
   - Sjekk at IP-adressen i `inventory.ini` er riktig
   - Verifiser at brukernavn/passord er korrekt
   - Test med `ping` og manuell SSH-tilkobling først

2. **VLAN opprettes ikke**:
   - Sjekk at `vlan_config` i switch_vars.yaml er korrekt formatert
   - Kjør med `-vvv` for detaljert feilsøking:
     ```bash
     ansible-playbook -i inventory.ini switch_setup.yaml -vvv
     ```

3. **Portkonfigurasjon feiler**:
   - Bekreft at portnavnene matcher faktisk hardware
   - Sjekk at VLAN-ene er opprettet før porttilordning

## Eksempelkjøring

```bash
$ ansible-playbook -i inventory.ini switch_setup.yaml

PLAY [Configure Cisco Switch] *******************************************

TASK [Configure hostname] **********************************************
changed: [switch1]

TASK [Configure VLANs] *************************************************
changed: [switch1]

TASK [Configure interfaces] ********************************************
changed: [switch1]

PLAY RECAP *************************************************************
switch1 : ok=3 changed=3 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

## Viktige notater

- Skriptet er testet med Cisco IOS 15.x
- Endre passord i `inventory.ini` før bruk i produksjon
- For trunk-konfigurasjon, endre `mode: "access"` til `mode: "trunk"` og legg til `trunk:`-parametere