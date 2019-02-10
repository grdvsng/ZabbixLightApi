try:
    from setuptools import setup
except:
    from distutils.core import setup

config = {
    'description': 'Module for API client "www.zabbix.com".',
    'author': 'Sergey Trishkin',
    'url': 'https://github.com/grdvsng/zabbix',
    'download_url': 'https://github.com/grdvsng/zabbix',
    'author_email': 'grdvsng@gmail.com',
    'version': '1.0',
    'install_requires': ['zabbix'],
    'packages': ['zabbix'],
    'scripts': ['bin\\'],
    'name': 'ZabbixLightApi',
}

setup(**config)