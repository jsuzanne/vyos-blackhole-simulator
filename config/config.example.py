# Example configuration file
# Copy this to config.py and modify with your settings

VYOS_CONFIG = {
    "device_type": "vyos",
    "host": "192.168.81.254",      # Change to your VyOS IP
    "username": "vyos",             # Change to your username
    "password": "vyos",             # Change to your password
    "port": 22,
    "fast_cli": False,
    "global_delay_factor": 1.0,
}

# IP ranges to block (customize as needed)
BLOCKED_IP_RANGES = [
    "188.114.0.0/16",
    "173.245.48.0/20",
    "103.21.244.0/22",
    # Add more ranges here
]

