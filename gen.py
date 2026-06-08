"""This script produces configuration files for octodns."""

import json

A = "A"
AAAA = "AAAA"
CNAME = "CNAME"
MX = "MX"
TXT = "TXT"

### subtlecoolness.com.yaml

root = {}

### coruscant
# this machine is hosted in linode

CORUSCANT_IPV4 = "45.79.10.128"
CORUSCANT_IPV6 = "2600:3c00::f03c:91ff:fe24:29ee"

root.update(
    {
        "coruscant": [
            {"type": A, "value": CORUSCANT_IPV4},
            {"type": AAAA, "value": CORUSCANT_IPV6},
            {
                "type": MX,
                "values": [{"exchange": "mail.subtlecoolness.com.", "preference": 10}],
            },
        ],
        "mail": [
            {"type": A, "value": CORUSCANT_IPV4},
            {"type": AAAA, "value": CORUSCANT_IPV6},
        ],
    }
)

### scarif
# this machine is hosted in oracle cloud

SCARIF_IPV4 = "163.192.112.100"

root.update({"scarif": [{"type": A, "value": SCARIF_IPV4}]})

### cname to scarif

cname_scarif = {"type": CNAME, "value": "scarif.subtlecoolness.com."}

for name in [
    "birthdayfeed",
    "kuma",
]:
    root.update({name: [cname_scarif]})

### domain root

root_mx = {
    "aspmx.l.google.com.": 10,
    "alt1.aspmx.l.google.com.": 20,
    "alt2.aspmx.l.google.com.": 30,
    "aspmx2.googlemail.com.": 40,
    "aspmx3.googlemail.com.": 50,
}

root.update(
    {
        "": [
            {"type": A, "value": CORUSCANT_IPV4},
            {
                "type": TXT,
                "ttl": 3600,
                "values": [
                    "MS=ms39318768",
                    "google-site-verification=RxUAQK2lPrb8l0bltRH-OcplAFQYr-2sL3_xq-CqJxw",
                    "v=spf1 include:outbound.mailhop.org ~all",  # mailhop.org is for outboundsmtp.com
                ],
            },
            {
                "type": MX,
                "values": [
                    {"exchange": exchange, "preference": preference}
                    for exchange, preference in root_mx.items()
                ],
            },
        ]
    }
)

### domain verification for discord

root.update(
    {
        "_discord": [
            {"type": TXT, "value": "dh=3704a9cd0c5ea23c3cb60cf61aec9159c912746b"}
        ]
    }
)

### cname to coruscant

cname_coruscant = {"type": CNAME, "value": "coruscant.subtlecoolness.com."}

for name in [
    "acciojacksons",
    "cal",
    "echoip",
    "groupmemail",
    "groupmemail-test",
    "jour",
    "junk",
    "lpb",
    "nocodb",
    "rss",
    "wiki",
    "www",
    "yavin",
]:
    root.update({name: [cname_coruscant]})

### tailscale

tailscale_hosts = {
    "coruscant": "100.67.215.117",  # linode server
    "dagobah": "100.95.127.66",  # thinkcentre
    "felucia": "100.66.139.64",  # ipad
    "kessel": "100.112.154.57",  # iphone
    "mandalore": "100.75.215.67",  # rebecca desktop
    "scarif": "100.101.205.124",
    "tatooine": "100.116.13.60",  # raspberry pi
}

for hostname, ip in tailscale_hosts.items():
    root.update({f"{hostname}.ts": [{"type": A, "value": ip}]})

### cnames for tailscale hosts

tailscale_cnames = {
    "music": "dagobah",
    "papers": "dagobah",
    "photos": "dagobah",
    "videos": "dagobah",
}

for hostname, target in tailscale_cnames.items():
    root.update(
        {hostname: [{"type": CNAME, "value": f"{target}.ts.subtlecoolness.com."}]}
    )

### github pages

pages_sites = {
    "accio": "jackson-family",
    "andromeda": "williamjacksn",
    "blog": "williamjacksn",
    "ellie": "jackson-family",
    "he-gave-me-my-ears": "jackson-family",
    "htmx": "williamjacksn",
    "menu": "williamjacksn",
    "mhs-chamber-singers-spring-2000": "williamjacksn",
    "molly": "jackson-family",
    "obs": "williamjacksn",
    "python-rainwave-client": "williamjacksn",
    "recipes": "jackson-family",
    "silly-sentences": "williamjacksn",
}

for hostname, target_org in pages_sites.items():
    root.update({hostname: [{"type": CNAME, "value": f"{target_org}.github.io."}]})

### home network

local_hostnames = {
    "adblock": "192.168.4.4",
    "dagobah.sambuca": "192.168.4.94",
    "tatooine.sambuca": "192.168.4.4",
}

for hostname, ip in local_hostnames.items():
    root.update({hostname: [{"type": A, "value": ip}]})

local_cnames = {
    "music": "dagobah",
    "papers": "dagobah",
    "photos": "dagobah",
    "videos": "dagobah",
}

for hostname, target in local_cnames.items():
    root.update(
        {
            f"{hostname}.sambuca": [
                {"type": CNAME, "value": f"{target}.sambuca.subtlecoolness.com."}
            ]
        }
    )

### syncthing is always localhost

root.update({"syncthing": [{"type": A, "value": "127.0.0.1"}]})

### outboundsmtp (https://www.outboundsmtp.com/)
# outboundsmtp is a simple smtp service that I set up because I wanted to add smtp settings to my home hp officejet
# scanner. I would have used sendgrid, but the scanner had a length limit for the smtp password and sendgrid's api key
# was too long. The password for outboundsmtp is shorter and fits within the length limit on the scanner.

root.update(
    {
        "duo-1651460024648-8e3e5c59._domainkey": [
            {
                "type": TXT,
                "value": "v=DKIM1\\; k=rsa\\; s=email\\; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLWiBESFejMDydnDE7ERkklPgnUsmXgpOQohtvBaEaNc+KVkXJ+1zxTuQmRzKIdraep9CQ9sz/l2+cymh2wszV/bWBC7AfaRUcSUNd/R0DRUJuomIgL2kHfI2sXI2dVANCnYek3oYfPbm5LcJRY3v6oHUbGJ+Y8iyds6DcyVBQKwIDAQAB",
            }
        ]
    }
)

### bluesky social

root.update(
    {
        "_atproto": [
            {
                "type": TXT,
                "value": "did=did:plc:yypsrghmekhc7wz6lwpkxsqd",
            },
        ],
        "bluesky": [
            {
                # https://bsky.app/profile/jacob.gold/post/3kh6re46yd42k
                #
                # Experimental feature for those comfortable with DNS,
                # you can set your domain to be a CNAME of `redirect.bsky.app`
                # and we'll redirect your domain to your bsky profile URL.
                #
                # https://bsky.app/profile/jacob.gold/post/3kh6rnpdzmp2v
                #
                # You can also use "bsky.example.com" -> "redirect.bsky.app"
                # or "bluesky.example.com" -> "redirect.bsky.app" and we'll
                # strip off the "bsky" or "bluesky" prefix when redirecting
                # to your profile.
                "type": CNAME,
                "value": "redirect.bsky.app.",
            },
        ],
    }
)

with open("config/subtlecoolness.com.yaml", "w") as f:
    json.dump(root, f, indent=2, sort_keys=True)

# end subtlecoolness.com.yaml

### valerocomingsoon.com.yaml

root = {
    "": [
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": "ALIAS",
            "value": "valerocomingsoon.github.io.",
        },
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": MX,
            "values": [
                {"exchange": "route1.mx.cloudflare.net.", "preference": 10},
                {"exchange": "route3.mx.cloudflare.net.", "preference": 60},
                {"exchange": "route2.mx.cloudflare.net.", "preference": 80},
            ],
        },
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": TXT,
            "value": "v=spf1 include:_spf.mx.cloudflare.net ~all",
        },
    ],
    "_dmarc": [
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": TXT,
            "value": "v=DMARC1\\; p=none\\; rua=mailto:1837ecd149ce40a48e55097ae29d6dc3@dmarc-reports.cloudflare.net",
        }
    ],
    "cf2024-1._domainkey": [
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": TXT,
            "value": "v=DKIM1\\; h=sha256\\; k=rsa\\; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78km4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB",
        }
    ],
    "www": [
        {
            "octodns": {"cloudflare": {"auto-ttl": True}},
            "type": CNAME,
            "value": "valerocomingsoon.github.io.",
        }
    ],
}

with open("config/valerocomingsoon.com.yaml", "w") as f:
    json.dump(root, f, indent=2, sort_keys=True)

# end valerocomingsoon.com.yaml

### production.yaml

root = {
    "#": "generated with gen.py",
    "manager": {
        "max_workers": 2,
    },
    "providers": {
        "config": {
            "class": "octodns.provider.yaml.YamlProvider",
            "directory": "./config",
            "default_ttl": 300,
            "enforce_order": False,
        },
        "cloudflare": {
            "class": "octodns_cloudflare.CloudflareProvider",
            "token": "env/CLOUDFLARE_TOKEN",
        },
    },
}

zone_names = ["subtlecoolness.com.", "valerocomingsoon.com."]

zones = {
    zone_name: {
        "sources": ["config"],
        "targets": ["cloudflare"],
    }
    for zone_name in zone_names
}
root.update({"zones": zones})

with open("config/production.yaml", "w") as f:
    json.dump(root, f, indent=2, sort_keys=True)

### end production.yaml
