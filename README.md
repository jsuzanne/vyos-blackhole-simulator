# VyOS Blackhole Simulator for Prisma SD-WAN Demonstrations

## 📋 Overview

Python toolkit for simulating network blackhole scenarios on a VyOS 1.5 router in the context of demonstrating Prisma SD-WAN auto-remediation capabilities.

This project enables demonstrations of how Prisma SD-WAN automatically detects connectivity issues when user traffic from a site to an application (SaaS, on-premise, or other) fails to reach its destination, regardless of the network path taken.

### 🎯 Use Cases

- **Auto-remediation demonstration**: Showcase Prisma SD-WAN's ability to detect and respond to network failures
- **Datacenter down simulation**: Reproduce a blackhole scenario affecting a client datacenter
- **Resilience testing**: Validate automatic detection of connectivity problems
- **Training**: Lab environment for understanding network detection mechanisms

### ✨ Features

- ✅ Enable/disable IP filtering via VyOS firewall
- ✅ Targeted blocking of specific IP ranges (simulating Cloudflare, datacenters, etc.)
- ✅ Detailed operation logging
- ✅ Automatic VyOS configuration mode management
- ✅ Change validation with commit/save

## 🏗️ Architecture

The project consists of two main scripts:

1. **vyosblockip_enable.py**: Activates IP filtering to simulate a blackhole
2. **vyosblockip_disable.py**: Deactivates filtering to restore connectivity

Scripts use Netmiko to SSH into the VyOS router and configure IPv4 firewall rules that block transit (forward) traffic to defined IP ranges.

## 📦 Prerequisites

### Required Software

- Python 3.7 or higher
- SSH access to a VyOS 1.5 router
- Network connectivity between execution machine and VyOS

### Recommended Lab Environment

- **VyOS Router**: Version 1.5 (configured as transit for SD-WAN traffic)
- **Prisma SD-WAN**: Controller configured with active monitoring
- **Network Interface**: eth1 configured for inbound traffic (adjustable)

### Python Dependencies

Dependencies are listed in `requirements.txt`:
