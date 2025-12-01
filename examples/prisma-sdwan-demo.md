# Prisma SD-WAN Auto-Remediation Demo

## Objective

Demonstrate Prisma SD-WAN's ability to detect and automatically remediate connectivity issues when traffic fails to reach its destination.

## Lab Topology

[Branch Site] --- [Prisma SD-WAN] --- [VyOS Router] --- [Application/Datacenter]
|
(Blackhole simulation)

## Demo Workflow

### Phase 1: Baseline

1. Verify normal connectivity from branch to application
2. Show traffic flowing through primary path
3. Display metrics in Prisma SD-WAN dashboard

### Phase 2: Failure Simulation

1. Execute `vyosblockip_enable.py`
2. Traffic to specific IP ranges is now dropped
3. Simulate datacenter/ISP blackhole scenario

### Phase 3: Detection & Remediation

1. Prisma SD-WAN detects increased latency/packet loss
2. Automatic path selection triggers
3. Traffic reroutes to alternative path
4. Show metrics and alerts in dashboard

### Phase 4: Recovery

1. Execute `vyosblockip_disable.py`
2. Primary path restored
3. Traffic may rebalance based on policy

## Key Points to Highlight

- **Real-world scenario**: Network teams face these issues daily
- **Detection speed**: How quickly Prisma identifies the problem
- **Zero-touch remediation**: No manual intervention required
- **Application awareness**: Traffic classified and routed intelligently
- **Visibility**: Complete insight into path quality and decisions

## Metrics to Monitor

- Latency (ms)
- Packet loss (%)
- Jitter
- Path changes
- Application performance scores
