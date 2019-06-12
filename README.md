# pyZabbix
## Light module for use Get Method Zabbix API.
> If you need create simple script for your *__Zabbix__* server,it's can help you.
### example:

```python

import pyZabbix

user     = "admin"
password = "bob1992"
base_url = "https://192.168.1.244:8080"

app = Zabbix(self, user, password, base_url)

method = "host.get"
params = {
    "output": [
        "hostid",
        "host"
    ],
    "selectInterfaces": [
        "interfaceid",
        "ip"
    ]
}
app.get(method, params)

```
