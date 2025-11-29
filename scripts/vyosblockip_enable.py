#!/usr/bin/env python3
# vyosblockip_enable.py
# Active le blocage IP sur le trafic de transit (forward) via VyOS 1.5

from netmiko import ConnectHandler
import logging, sys

VYOS = {
    "device_type": "vyos",
    "host": "192.168.81.254",      # adapte si besoin
    "username": "vyos",
    "password": "vyos",
    "port": 22,
    "fast_cli": False,
    "global_delay_factor": 1.0,
}

LOG_FILE = "./vyos_firewall_enable.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

IP_BLOCKS = [
    "188.114.0.0/16","173.245.48.0/20","103.21.244.0/22","103.22.200.0/22",
    "103.31.4.0/22","141.101.64.0/18","108.162.192.0/18","190.93.240.0/20",
    "188.114.96.0/20","197.234.240.0/22","198.41.128.0/17","162.158.0.0/15",
    "104.16.0.0/13","104.24.0.0/14","172.64.0.0/13","131.0.72.0/22",
    "136.243.124.156/32","142.132.193.157/32",
]

def ensure_conf_mode(conn):
    if not conn.check_config_mode():
        conn.config_mode()

def interactive_save(conn):
    ensure_conf_mode(conn)
    out = conn.send_command_timing("save", strip_prompt=False, strip_command=False)
    if any(m in out for m in ("Saving configuration to", "Done", "Configuration saved")):
        return True
    return False

def main():
    logger.info("="*80); logger.info("DEMARRAGE: ACTIVER filtrage IP (VyOS 1.5)"); logger.info("="*80)
    try:
        conn = ConnectHandler(**VYOS)
        logger.info("Connexion SSH établie")
        ensure_conf_mode(conn)

        cfg_cmds = []
        for ipn in IP_BLOCKS:
            cfg_cmds.append(f"set firewall group network-group IP2Block5 network '{ipn}'")

        cfg_cmds += [
            "set firewall ipv4 name BlockIP default-action 'return'",
            "set firewall ipv4 name BlockIP description 'Blocage IPs malveillantes'",
            "set firewall ipv4 name BlockIP rule 10 action 'drop'",
            "set firewall ipv4 name BlockIP rule 10 destination group network-group 'IP2Block5'",
            "set firewall ipv4 name BlockIP rule 10 description 'Drop traffic vers IP2Block5'",
            "set firewall ipv4 forward filter rule 100 action 'jump'",
            "set firewall ipv4 forward filter rule 100 jump-target 'BlockIP'",
            "set firewall ipv4 forward filter rule 100 inbound-interface name 'eth1'",
            "set firewall ipv4 forward filter rule 100 description 'Apply BlockIP to eth1 inbound'",
        ]

        conn.send_config_set(cfg_cmds, exit_config_mode=False)
        logger.info("Commit…")
        conn.commit(delay_factor=2.0)
        logger.info("Commit OK")

        if not interactive_save(conn):
            logger.warning("Save interactif sans marqueurs explicites, on continue si compare = vide")
        # Optionnel: vérifier compare
        cmp_out = conn.send_command_timing("compare", strip_prompt=False, strip_command=False)
        logger.info(f"compare:\n{cmp_out}")

        if conn.check_config_mode():
            conn.exit_config_mode()
        conn.disconnect()
        logger.info("✅ Activation terminée avec succès")
        return 0
    except Exception as e:
        logger.exception(f"❌ Échec activation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

