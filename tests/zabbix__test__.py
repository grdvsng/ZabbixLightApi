from sys import path

path.append('..\\')
from zabbix.zabbix import *

try:    from configparser import ConfigParser
except: raise MemoryError("Can't test without ConfigParser, please, 'pip install ConfigParser'.")


class Polygon:
    n      = 1
    config = ConfigParser()
    
    def __init__(self, ini):
        self.config.read(ini)
        
        self.setting = {
            'user':     self.config.get('seting', 'name').rstrip(),
            'password': self.config.get('seting', 'password').rstrip(),
            'base_url': self.config.get('seting', 'url').rstrip(),
        }
        
    def _generate(self, D):
        l = [i for i in D.values()]
        return l
        
    def login(self, exception, **args):  
        temp = self.setting.copy()
        
        for k,v in args.items():
            if k in temp: temp[k] = v
        
        args = self._generate(temp)
        print('step: {}'.format(self.n))
        
        try:   self.zabbix = Zabbix(*args, _path='session.txt')
        except exception: pass
        
        print('\n\nFine!')
        self.n += 1

    def get(self, meth, params, *args):   
        self.login(Warning, *args)
        self.zabbix.get(meth, params)
        
        
if '__main__' == __name__:
    test = Polygon('config.ini')

    test.login(BadValueError, user=1, password=2, base_url=str)
    test.login(ArgumentError, base_url=test.setting['base_url'] + '/zabbix')
    test.login(Warning)
    test.login(ServerError, base_url='123')
    test.get(
        "host.get", 
        {
            "output": [
                "hostid",
                "host"
            ],
            "selectInterfaces": [
                "interfaceid",
                "ip"
            ],
            "limit": 5
        }
        )