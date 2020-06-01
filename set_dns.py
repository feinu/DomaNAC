#!/usr/bin/env python3
import logging
import requests
import socket
import yaml

from domains_client import DomainsClient


def get_current_ip():
    """
    Find the current public IP by making a request to httpbin.org/ip
    """
    response = requests.get("https://httpbin.org/ip")
    return response.json()["origin"]


def get_current_dns(hostname):
    return socket.gethostbyname(hostname)


with open("config.yml") as f:
    config = yaml.safe_load(f)


hostname = config["hostname"]


current_ip = get_current_ip()
dns_ip = get_current_dns(hostname)

dns_entries = {
    config["dns_entry"]: current_ip,
}

if current_ip != dns_ip:
    logging.info(
        "Updating DNS entry for %s from %s to %s"
        % (hostname, dns_ip, current_ip)
    )
    client = DomainsClient(config["username"], config["password"])
    client.set_dns_from_scratch(dns_entries)
