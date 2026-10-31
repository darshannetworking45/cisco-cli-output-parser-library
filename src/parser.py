"""Regular-expression parsers for selected Cisco CLI output."""

from __future__ import annotations

import re
from typing import Dict, List, Optional

class CiscoCliParser:
    """Parses selected Cisco IOS and IOS-XE command output."""

    @staticmethod
    def parse_show_ip_int_brief(text: str) -> List[Dict[str, Optional[str]]]:
        """Parses 'show ip interface brief' into a list of interface records."""
        results: List[Dict[str, Optional[str]]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("Interface"):
                continue

            m = re.match(
                r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(administratively down|up|down)\s+(up|down)",
                line,
                re.IGNORECASE
            )
            if m:
                raw_ip = m.group(2)
                ip_val = None if raw_ip.lower() == "unassigned" else raw_ip
                results.append({
                    "interface": m.group(1),
                    "ip_address": ip_val,
                    "ip": ip_val,
                    "ok": m.group(3),
                    "method": m.group(4),
                    "status": m.group(5).lower(),
                    "proto": m.group(6).lower()
                })
        return results

    @staticmethod
    def parse_show_cdp_neighbors(text: str) -> List[Dict[str, str]]:
        """Parses 'show cdp neighbors' tabular output."""
        results: List[Dict[str, str]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("Device ID") or line.startswith("Capability"):
                continue

            m = re.match(
                r"^(\S+)\s+([A-Za-z0-9/]+(?:\s+[0-9/]+)?)\s+(\d+)\s+([A-Za-z\s]+?)\s{2,}([A-Za-z0-9\-]+)\s+(.+)$",
                line
            )
            if m:
                results.append({
                    "neighbor": m.group(1),
                    "local_interface": m.group(2).strip(),
                    "holdtime": m.group(3),
                    "capability": m.group(4).strip(),
                    "platform": m.group(5),
                    "remote_port": m.group(6).strip()
                })
        return results

    @staticmethod
    def parse_show_ip_ospf_neighbor(text: str) -> List[Dict[str, str]]:
        """Parses 'show ip ospf neighbor' output."""
        results: List[Dict[str, str]] = []
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("Neighbor ID"):
                continue

            m = re.match(
                r"^(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+([A-Za-z0-9/_]+)\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)",
                line
            )
            if m:
                results.append({
                    "neighbor_id": m.group(1),
                    "priority": m.group(2),
                    "state": m.group(3),
                    "dead_time": m.group(4),
                    "address": m.group(5),
                    "interface": m.group(6)
                })
        return results
