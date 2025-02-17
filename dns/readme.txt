https://dev.to/stjohnjohnson/internal-domains-with-dnsmasq-and-pi-hole-4cof

dns forwarding in Pihole:
/etc/dnsmasq.d/kmarx.conf:
server=/k.marx.katowice.pl/192.168.1.214

updating Pi-hole:
pihole -up


DNS switching:
- cloudflare entries
- Pihole:
  - dns records in UI
  - kmarx.conf
- router: NOTHNIG
- new domain in password manager (BOOTSTRAP_DOMAIN)
- recreate sealed secrets
- cafe upload address (?)
- each cluster node:
  - /etc/hosts
  - /etc/postfix/main.cf
- NAS: NOTHING
- Google Sheets functions
- AntennaPod