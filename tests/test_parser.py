import unittest
from src.parser import CiscoCliParser

SAMPLE_IP_INT_BR = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.0.2.1       YES manual up                    up
GigabitEthernet0/1     unassigned      YES manual administratively down down
Loopback0              10.255.255.1    YES manual up                    up
"""

SAMPLE_CDP = """
Device ID        Local Intrfce     Holdtme    Capability  Platform  Port ID
sw-core-01.corp  Gig 0/1           154             R S I  C9500     Ten 1/0/1
ap-floor2        Gig 0/12          130               T    AIR-AP    Gig 0
"""

SAMPLE_OSPF = """
Neighbor ID     Pri   State           Dead Time   Address         Interface
10.255.255.2      1   FULL/BDR        00:00:34    192.168.1.2     GigabitEthernet0/0
10.255.255.3      1   2WAY/DROTHER    00:00:31    192.168.1.3     GigabitEthernet0/0
"""

class TestTextFSMParser(unittest.TestCase):
    def test_ip_int_brief(self):
        res = CiscoCliParser.parse_show_ip_int_brief(SAMPLE_IP_INT_BR)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]["interface"], "GigabitEthernet0/0")
        self.assertEqual(res[0]["ip_address"], "192.0.2.1")
        self.assertIsNone(res[1]["ip_address"])
        self.assertEqual(res[1]["status"], "administratively down")

    def test_cdp_neighbors(self):
        res = CiscoCliParser.parse_show_cdp_neighbors(SAMPLE_CDP)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["neighbor"], "sw-core-01.corp")
        self.assertEqual(res[0]["platform"], "C9500")

    def test_ospf_neighbor(self):
        res = CiscoCliParser.parse_show_ip_ospf_neighbor(SAMPLE_OSPF)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["neighbor_id"], "10.255.255.2")
        self.assertEqual(res[0]["state"], "FULL/BDR")

if __name__ == "__main__":
    unittest.main()
