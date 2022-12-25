https://dev.to/stjohnjohnson/internal-domains-with-dnsmasq-and-pi-hole-4cof

dns forwarding in Pihole:
/etc/dnsmasq.d/kmarx.conf:
server=/k.marx.katowice.pl/192.168.1.214

updating Pi-hole:
pihole -up