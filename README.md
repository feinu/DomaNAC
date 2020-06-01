# Domains.co.za Non-API Client
domains.co.za only offers API access to domain resellers, not end users.
End users are left with only the web interface to update DNS records, which can be
a problem for those of us with dynamically allocated IPs.

This tool logs in to the web interface using Selenium and edits a DNS record.
It is very flaky, as it relies entirely on the layout of the web page.

## Prerequisites
* Mozilla Firefox
* https://github.com/mozilla/geckodriver/releases
* `pip install -r requirements.txt`

## Usage
Set up a `config.yml` file similarly to `sample_config.yml`.

```
./set_dns.py
```

It will check your current IP, and update the DNS record to match (if necessary).
