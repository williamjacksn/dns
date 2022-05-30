"""This script produces configuration files for octodns."""

import json

A = 'A'
AAAA = 'AAAA'
CNAME = 'CNAME'
MX = 'MX'
TXT = 'TXT'

### subtlecoolness.com.yaml

root = {}

### coruscant
# this machine is hosted in linode

CORUSCANT_IPV4 = '45.79.10.128'
CORUSCANT_IPV6 = '2600:3c00::f03c:91ff:fe24:29ee'

root.update({
    'coruscant': [
        {'type': A, 'value': CORUSCANT_IPV4},
        {'type': AAAA, 'value': CORUSCANT_IPV6},
    ]
})

### domain root

root_mx = {
    'aspmx.l.google.com.': 10,
    'alt1.aspmx.l.google.com.': 20,
    'alt2.aspmx.l.google.com.': 30,
    'aspmx2.googlemail.com.': 40,
    'aspmx3.googlemail.com.': 50,
}

root.update({
    '': [
        {'type': A, 'value': CORUSCANT_IPV4},
        {'type': TXT, 'ttl': 3600, 'values': [
            'MS=ms39318768',
            'google-site-verification=RxUAQK2lPrb8l0bltRH-OcplAFQYr-2sL3_xq-CqJxw',
            'v=spf1 include:outbound.mailhop.org ~all',  # mailhop.org is for outboundsmtp.com
        ]},
        {'type': MX, 'values': [
            {'exchange': exchange, 'preference': preference}
            for exchange, preference in root_mx.items()
        ]}
    ]
})

### cname to coruscant

cname_coruscant = {
    'type': CNAME,
    'value': 'coruscant.subtlecoolness.com.'
}

for name in [
    '404',
    'acciojacksons',
    'birthdayfeed',
    'cal',
    'echoip',
    'groupmemail',
    'groupmemail-test',
    'junk',
    'rss',
    'wiki',
    'www',
    'yavin',
]:
    root.update({name: [cname_coruscant]})

### tailscale

tailscale_hosts = {
    'coruscant': '100.67.215.117',
    'raspberrypi': '100.81.7.64',
}

for hostname, ip in tailscale_hosts.items():
    root.update({
        f'{hostname}.ts': [{'type': A, 'value': ip}]
    })

### netlify

netlify_sites = {
    'accio': 'accio',
    'andromeda': 'demo-andromeda',
    'blog': 'blog-subtlecoolness-com',
    'molly': 'molly-subtlecoolness-com',
    'python-rainwave-client': 'python-rainwave-client',
    'recipes': 'jackson-family-recipes',
    'silly-sentences': 'silly-sentences',
}

for hostname, alias in netlify_sites.items():
    root.update({
        hostname: [{'type': CNAME, 'value': f'{alias}.netlify.app.'}]
    })

### blogger

root.update({
    'he-gave-me-my-ears': [{
        'type': CNAME,
        'value': 'ghs.google.com.',
    }]
})

### sendgrid

sendgrid_cnames = {
    'em8786': 'u25937580.wl081.sendgrid.net.',
    's1._domainkey': 's1.domainkey.u25937580.wl081.sendgrid.net.',
    's2._domainkey': 's2.domainkey.u25937580.wl081.sendgrid.net.',
}

for hostname, value in sendgrid_cnames.items():
    root.update({
        hostname: [{'type': CNAME, 'value': value}]
    })

### outboundsmtp (https://www.outboundsmtp.com/)
# outboundsmtp is a simple smtp service that I set up because I wanted to add smtp settings to my home hp officejet
# scanner. I would have used sendgrid, but the scanner had a length limit for the smtp password and sendgrid's api key
# was too long. The password for outboundsmtp is shorter and fits within the length limit on the scanner.

root.update({
    'duo-1651460024648-8e3e5c59._domainkey': [{
        'type': TXT,
        'value': 'v=DKIM1\; k=rsa\; s=email\; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLWiBESFejMDydnDE7ERkklPgnUsmXgpOQohtvBaEaNc+KVkXJ+1zxTuQmRzKIdraep9CQ9sz/l2+cymh2wszV/bWBC7AfaRUcSUNd/R0DRUJuomIgL2kHfI2sXI2dVANCnYek3oYfPbm5LcJRY3v6oHUbGJ+Y8iyds6DcyVBQKwIDAQAB',
    }]
})

### mailgun
# groupmemail uses mailgun to send and receive email for *@mg.subtlecoolness.com

root.update({
    'krs._domainkey.mg': [{
        'type': TXT,
        'value': 'k=rsa\; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDXdL1VkQmI026q2KW+mryp0xqaJsMZGxF96QrlaGO5kqFBPuH7SEJEBJWw305bHxsV30XSZwTLHDWVVm6R2PDMowf4ke3LFxPC7Sjbr8lnHWz/goVBZbNkVRkZCwh5LLcufwXI1hY3M/Q1Wkx9oGelJOfAxOEqj2mwL8ZQb+69mwIDAQAB',
    }]
})

root.update({
    'mail._domainkey': [{
        'type': TXT,
        'value': 'k=rsa\;p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDeMVIzrCa3T14JsNY0IRv5/2V1/v2itlviLQBwXsa7shBD6TrBkswsFUToPyMRWC9tbR/5ey0nRBH0ZVxp+lsmTxid2Y2z+FApQ6ra2VsXfbJP3HE6wAO0YTVEJt1TmeczhEd2Jiz/fcabIISgXEdSpTYJhb0ct0VJRxcg4c8c7wIDAQAB',
    }]
})

root.update({
    'email.mg': [{
        'type': CNAME,
        'value': 'mailgun.org.',
    }]
})

root.update({
    'mg': [
        {
            'type': TXT,
            'value': 'v=spf1 include:mailgun.org ~all',
        },
        {
            'type': MX,
            'values': [
                {'exchange': 'mxa.mailgun.org.', 'preference': 10},
                {'exchange': 'mxb.mailgun.org.', 'preference': 10},
            ]
        },
    ]
})

with open('config/subtlecoolness.com.yaml', 'w') as f:
    json.dump(root, f, indent=2, sort_keys=True)

# end subtlecoolness.com.yaml

### lugolandscapingservices.com.yaml

root = {}

root_mx = {
    'route1.mx.cloudflare.net.': 15,
    'route2.mx.cloudflare.net.': 64,
    'route3.mx.cloudflare.net.': 11,
}

root.update({
    '': [
        {
            'type': MX,
            'values': [
                {'exchange': exchange, 'preference': preference}
                for exchange, preference in root_mx.items()
            ]
        },
        {
            'type': TXT,
            'value': 'v=spf1 include:_spf.mx.cloudflare.net ~all',
        },
    ],
    '_dmarc': [
        {'type': TXT, 'value': 'v=DMARC1\; p=none\; rua=mailto:william@subtlecoolness.com'}
    ]
})

with open('config/lugolandscapingservices.com.yaml', 'w') as f:
    json.dump(root, f, indent=2, sort_keys=True)

### end lugolandscapingservices.com.yaml

### production.yaml

root = {
    'manager': {
        'max_workers': 2,
    },
    'providers': {
        'config': {
            'class': 'octodns.provider.yaml.YamlProvider',
            'directory': './config',
            'default_ttl': 300,
            'enforce_order': False,
        },
        'cloudflare': {
            'class': 'octodns_cloudflare.CloudflareProvider',
            'token': 'env/CLOUDFLARE_TOKEN',
        },
    },
}

zone_names = [
    'lugolandscapingservices.com.',
    'subtlecoolness.com.',
]

zones = {
    zone_name: {
        'sources': ['config'],
        'targets': ['cloudflare'],
    }
    for zone_name in zone_names
}
root.update({
    'zones': zones
})

with open('config/production.yaml', 'w') as f:
    json.dump(root, f, indent=2, sort_keys=True)

### end production.yaml
