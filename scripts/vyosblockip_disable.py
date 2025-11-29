#!/usr/bin/env python3
# vyosblockip_disable.py
# Désactive l’application (supprime forward rule 100), conserve BlockIP et IP2Block5

from netmiko import ConnectHandler
import logging, sys

VYOS = {
    "device_type": "vyos",
    "host": "192.168.81.254",
    "username": "vyos",
    "password": "vyos",
    "port": 22,
    "fast_cli": False,
    "global_delay_factor": 1.5,
}

LOG_FILE = "./vyos_firewall_disable.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

def ensure_conf_mode(conn):
    if not conn.check_config_mode():
        conn.config_mode()

def interactive_save(conn):
    ensure_conf_mode(conn)
    out = conn.send_command_timing("save", strip_prompt=False, strip_command=False)
    if any(m in out for m in ("Saving configuration to", "Done", "Configuration saved")):
        return True
    return False

def compare_is_clean(conn):
    ensure_conf_mode(conn)
    out = conn.send_command_timing("compare", strip_prompt=False, strip_command=False)
    logger.info(f"compare:\n{out}")
    return (out.strip() == "") or ("No changes between working and active configurations" in out)

def main():
    logger.info("="*80); logger.info("DEMARRAGE: DESACTIVER filtrage IP"); logger.info("="*80)
    try:
        conn = ConnectHandler(**VYOS)
        logger.info("Connexion SSH établie")
        ensure_conf_mode(conn)

        cfg_cmds = ["delete firewall ipv4 forward filter rule 100"]
        conn.send_config_set(cfg_cmds, exit_config_mode=False)

        logger.info("Commit…")
        conn.commit(delay_factor=2.0)
        logger.info("Commit OK")

        if not interactive_save(conn):
            if compare_is_clean(conn):
                logger.info("Aucun diff après commit; on considère l’opération cohérente")
            else:
                raise ValueError("Save non confirmé et compare indique des diffs")

        if conn.check_config_mode():
            conn.exit_config_mode()
        conn.disconnect()
        logger.info("✅ Désactivation terminée avec succès")
        return 0
    except Exception as e:
        logger.exception(f"❌ Échec désactivation: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

