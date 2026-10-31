# Cisco CLI Output Parser Library

Parses selected Cisco command output for interface status, CDP neighbors, and OSPF neighbors. The parsers use targeted Python regular expressions and return lists of dictionaries.

## Main entry points

- `src.parser.CiscoCliParser` (`parse_show_ip_int_brief, parse_show_cdp_neighbors, parse_show_ip_ospf_neighbor`)

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The project uses the Python standard library; no third-party package is required.

## Scope

These are command-specific regular-expression parsers, not TextFSM templates or a general-purpose CLI parsing engine. They handle the sample output formats covered by the tests; validate them against output from your own IOS / IOS-XE versions before using them in automation.
