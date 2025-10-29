import ipaddress
from typing import List, Dict, Any


def validate_ipv4(ip: str) -> bool:
    try:
        ipaddress.IPv4Address(ip)
        return True
    except Exception:
        return False


def validate_prefix(p) -> bool:
    try:
        p = int(p)
        return 0 <= p <= 32
    except Exception:
        return False


def prefix_to_mask(prefix: int) -> str:
    return str(ipaddress.IPv4Network(f"0.0.0.0/{prefix}").netmask)


def network_base(ip: str, prefix: int) -> ipaddress.IPv4Network:
    """Return a normalized IPv4 network object."""
    return ipaddress.IPv4Network(f"{ip}/{prefix}", strict=False)


# ---------------- SUBNETTING ----------------
def subnetting(network_ip: str, current_prefix: int, new_prefix: int) -> Dict[str, Any]:
    """
    Split a given network into smaller subnets.
    """
    if not (validate_ipv4(network_ip) and validate_prefix(current_prefix) and validate_prefix(new_prefix)):
        raise ValueError("Invalid IP or prefix")
    if int(new_prefix) <= int(current_prefix):
        raise ValueError("New prefix must be larger (e.g. /26 > /24)")

    base_net = network_base(network_ip, int(current_prefix))
    subnets = list(base_net.subnets(new_prefix=int(new_prefix)))

    result = {
        "original_network": f"{base_net.network_address}/{current_prefix}",
        "original_mask": prefix_to_mask(int(current_prefix)),
        "new_prefix": int(new_prefix),
        "new_mask": prefix_to_mask(int(new_prefix)),
        "num_subnets": len(subnets),
        "hosts_per_subnet": (2 ** (32 - int(new_prefix))) - 2 if new_prefix < 31 else (1 if new_prefix == 31 else 0),
        "subnets": []
    }

    for net in subnets:
        broadcast = net.broadcast_address
        network_addr = net.network_address

        # Determine usable hosts
        if net.prefixlen < 31:
            first_host = ipaddress.IPv4Address(int(network_addr) + 1)
            last_host = ipaddress.IPv4Address(int(broadcast) - 1)
            usable = [str(first_host), str(last_host)]
        elif net.prefixlen == 31:
            usable = [str(network_addr), str(broadcast)]
        else:
            usable = [str(network_addr)]

        result["subnets"].append({
            "network": f"{network_addr}/{net.prefixlen}",
            "broadcast_address": str(broadcast),
            "mask": str(net.netmask),
            "host_range": usable
        })

    return result


# ---------------- SUPERNETTING ----------------
# app/utils/subnet_tools.py (replace the existing supernetting function)

def supernetting(networks: List[str]) -> Dict[str, Any]:
    """
    Combine multiple networks into collapsed supernets, return canonical (network/prefix).
    Accepts inputs like:
      ["192.168.1.0/24", "192.168.2.0/24"]  or ["1.1.1.1/25"]
    Normalizes host addresses to their network (strict=False), collapses, and dedups.
    """
    if not networks:
        raise ValueError("No networks provided")

    parsed = []
    for item in networks:
        if not item:
            continue
        s = item.strip()
        if not s:
            continue
        # ensure s contains a /prefix
        if "/" not in s:
            raise ValueError(f"Each network must include a prefix (CIDR): {s}")
        try:
            net = ipaddress.IPv4Network(s, strict=False)  # normalizes host addresses
            parsed.append(net)
        except Exception:
            raise ValueError(f"Invalid network: {s}")

    if not parsed:
        raise ValueError("No valid networks provided")

    # Collapse contiguous/overlapping networks
    merged = list(ipaddress.collapse_addresses(parsed))

    # Build canonical unique list
    supernets = []
    seen = set()
    for net in merged:
        key = f"{net.network_address}/{net.prefixlen}"
        if key in seen:
            continue
        seen.add(key)
        supernets.append({
            "network": str(net.network_address),
            "prefix": net.prefixlen,
            "mask": str(net.netmask)
        })

    return {"count": len(supernets), "supernets": supernets}


# app/utils/subnet_tools.py (add)

def minimal_cover_supernet(networks: List[str]) -> Dict[str, Any]:
    """
    Return the minimal single CIDR that covers all provided networks.
    Example: ["192.168.1.0/27","192.168.2.0/27"] -> {"supernet":"192.168.0.0/22", "prefix":22, "mask":"255.255.252.0"}
    """
    if not networks:
        raise ValueError("No networks provided")

    parsed = []
    for s in networks:
        s = s.strip()
        if not s:
            continue
        if "/" not in s:
            raise ValueError(f"Each network must include a prefix (CIDR): {s}")
        try:
            net = ipaddress.IPv4Network(s, strict=False)
            parsed.append(net)
        except Exception:
            raise ValueError(f"Invalid network: {s}")

    if not parsed:
        raise ValueError("No valid networks provided")

    min_ip = min(int(net.network_address) for net in parsed)
    max_ip = max(int(net.broadcast_address) for net in parsed)

    xor = min_ip ^ max_ip
    if xor == 0:
        prefix = 32
    else:
        # number of common leading bits
        prefix = 32 - xor.bit_length()

    # compute network address masked to that prefix
    mask = (~0 << (32 - prefix)) & 0xFFFFFFFF
    network_addr_int = min_ip & mask
    network_addr = ipaddress.IPv4Address(network_addr_int)
    result_net = ipaddress.IPv4Network(f"{network_addr}/{prefix}", strict=False)

    return {
        "supernet": f"{result_net.network_address}/{result_net.prefixlen}",
        "prefix": result_net.prefixlen,
        "mask": str(result_net.netmask)
    }




# ---------------- NEXT SUBNET ----------------
def next_subnet(network: str) -> Dict[str, Any]:
    """
    Find the next subnet of a given CIDR.
    """
    try:
        net = ipaddress.IPv4Network(network, strict=False)
    except Exception:
        raise ValueError("Invalid network")

    size = net.num_addresses
    next_net_addr = int(net.network_address) + size

    if next_net_addr > int(ipaddress.IPv4Address("255.255.255.255")):
        raise ValueError("No next subnet available")

    next_net = ipaddress.IPv4Network((ipaddress.IPv4Address(next_net_addr), net.prefixlen), strict=False)

    return {
        "next_subnet": {
            "network": str(next_net.network_address),
            "prefix": net.prefixlen,
            "broadcast": str(next_net.broadcast_address)
        }
    }


# ---------------- REVERSE LOOKUP ----------------
def reverse_lookup(ip: str) -> Dict[str, Any]:
    """
    Reverse DNS lookup of an IP address.
    """
    import socket
    if not validate_ipv4(ip):
        raise ValueError("Invalid IP address")

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except Exception:
        hostname = "No PTR record found"

    return {
        "ip": ip,
        "hostname": hostname
    }
