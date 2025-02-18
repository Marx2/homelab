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
- url for passwords in password manager
- recreate sealed secrets
- cafe upload address (?)
- each cluster node:
  - /etc/hosts
  - /etc/postfix/main.cf
- NAS: NOTHING
- GitHub - Dex authentication
  - change Homepage URL:: https://k.marx.katowice.pl
  - change Authorization callback URL: https://dex.k.marx.katowice.pl/callback

Apps:
- Uptime Kuma
- Google Sheets functions
- AntennaPod