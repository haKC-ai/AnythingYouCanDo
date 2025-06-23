import json

input_path = 'LIS/lnkedin_cookies.json'  # Your EditThisCookie export
output_path = 'LIS/lnkedin_cookies.txt'  # Output for Selenium

with open(input_path, 'r') as f:
    cookies = json.load(f)

with open(output_path, 'w') as out:
    out.write('# Netscape HTTP Cookie File\n')
    for c in cookies:
        domain = c['domain']
        flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = c['path']
        secure = 'TRUE' if c.get('secure') else 'FALSE'
        expiration = str(int(c['expirationDate'])) if 'expirationDate' in c else '0'
        name = c['name']
        value = c['value']
        out.write('\t'.join([domain, flag, path, secure, expiration, name, value]) + '\n')
