forward DNS queries for subdomain to other DNS server

add via ssh in router: /jffs/configs/dnsmasq.conf.add
server=/k.marx.katowice.pl/192.168.1.214

Current solution: PiHole
/etc/dnsmasq.d/k.marx.conf


https://unfinishedbitness.info/2015/05/26/asuswrt-finalized-setup/
https://github.com/RMerl/asuswrt-merlin.ng/wiki/Custom-config-files#postconf-scripts
https://github.com/RMerl/asuswrt-merlin.ng/wiki/Custom-domains-with-dnsmasq
https://www.reddit.com/r/HomeNetworking/comments/46uk1z/is_it_possible_to_add_custom_dns_routes_to_rtac68u/
https://serverfault.com/questions/798419/how-to-conditionally-redirect-dns-queries-by-server-with-dnsmasq


Dynamic DNS
DNSomatic + CloudFlare
At DNS-O-MATIC you must set the following settings:

- Service:        Cloudflare

- E-Mail:         “E-Mail-address which is registered at Cloudflare”

- API Token:      “API Token from Cloudflare”

- Hostname:       dynamic

- Domain:         “yourdomain.xyz”

 

At Cloudflare you must set the following records:

- Type: A     |              Name: dynamic                                |              Value: “your WAN IP” ***

- Type: CNAME |              *                                            |              Value: dynamic.”yourdomain.xyz”

 
*** will later be actualized by DNS-O-MATIC

https://support.opendns.com/hc/en-us/community/posts/115000937008-How-to-set-up-DNS-O-MATIC-for-Cloudflare-and-the-other-way-around-and-a-FritzBox