import requests
from time     import sleep
from datetime import datetime
from random   import randint
from sys      import path
from json     import dumps

path.append('..\\')
from bin.ping   import *
from bin.errors import *

''' Module ZabbixLightApi.
    author:  Sergey Trishkin
    version: 1.1
    use modules:
        requests;
        time;
        datetime;
        random;
        json;
        ping (my own module).
        error (for special scrip errors).
        
    Description: Module help you create fast request to your zabbix api in your server.
    
    
   
    Classes:
        ---Tree---
        |Protocol|
        |   ||   |   
        |   ||   |
        |   \/   |
        |Protocol|   
        ----------        
        Protocol:
            convert script values to server standard;
            decode and parse response to light easy performance;
            write your session data result;
        Zabbix:
            connect to server;
            send request;
            get response.
     
        Algoritm:
        
        Create exemplar of class Zabbix.
       --USE---------------------------------
       | server login;                      |
       | pass;                              |    
       | server (URL like 127.0.1.1).       |
       --------------------------------------
                        ||
                        ||
                        \/
                With initializations:
        \-----------------------------------------------\
         \* Script check your values;                    \      
          \* Script try connect on server with your data; \
           \* Script save special api key for use api.     \
            \-----------------------------------------------\     
               ||                   ||
               ||                   ||
               \/                   \/
          Without Error           Error -----> Return Error
               ||
               ||
               \/
        Get method can use.
         
        get(meth, params)
            Method is zabbix API method can find in https://www.zabbix.com/documentation/3.4/manual/api
            params dict with API method format.
            Exampl:
               (meth = "host.get", 
                params = {
                    "output": [
                        "hostid",
                        "host"
                    ],
                    "selectInterfaces": [
                       "interfaceid",
                       "ip"
                   ]}
                ) 
                
            script ping server and if all right:
                method return data (and if response was incorrect too).
            else: return error.
            
'''

class Protocol:
    ''' Class Protocol.
        Base class for script:
            save specific method to convent request;
            parse and format data content;
            save main variables.
        
        Attributes:
           user         - str    - client name;
           password     - str    - password;
           base_url     - str    - server address;
           _pinger      - obj    - special class for _isintanse server connection;
           _isintanse   - lambda - check value type and return val or error;
           _path        - str    - path of log file;
           num          - list   - list with nums 0-9;
           session_data - list   - list with class all returned results;
           private      - bool   - printe or not response result;
           json_rpc     - dict   - special dict request format to zabbix api;
           EType        - obj    - script errors exemplar;
           errors       - dict   - Dict with ETypes and str with error msg.
           active_resp  - str    - last main resp params.
        methods:
            _header - header for zabbix api.
            _error(ET, code, *args) - special script error;
                ET   - key of EType dict.
                code - index of errors node list.
                args - some str args to format.
            _warning(**params): dara argumets from api error response;
            _print_data - format and print format public response data.
            short_url   - convert full path to main URL;
                text - str with last Zabbix method.
                data - dict with response value.
                
    '''
    
    # Main parameters.
    user        = None
    password    = None
    _path       = False
    active_resp = None
    
    base_url = 'http://{}/zabbix/api_jsonrpc.php' # Only server address without full path.
    _pinger  = EasyPing() 
    
    # Specific instance for error catch.
    _isintanse   = lambda m, a, n: a if isinstance(a, str) else m._error(0, 0, *(n, type(a)))
    num          = [i for i in range(0, 10)]
    session_data = [] # Variable with all response.
    private      = False
    
    json_rpc = {
        "jsonrpc": "2.0",
        "method": None,
        "params": {
            "user": None,
            "password": None,
        },
        "id": None,
        "auth": None
    }
    _list_data = [
        '{',
        ')',
        '(',
        ',',
        '[',
        ']',
        '}',
    ]
    
    EType  = [
        BadValueError,
        ArgumentError,
        ServerError,
    ]
    
    errors = {
        BadValueError: [
            "Argument: '{}' must be string, but your's: {}.",
            "Please _isintanse base_url value: {}.",
            "Incorrect user name or password, please change parameters.",
            "Base_url can't be < 0, try again.",
            "Argument: parameters must be {}, but your's: {}.",
        ],
        ArgumentError: [
            "Incorrect response({}), please, _isintanse base_url '{}'.",
            "Argument's output and selectInterfaces must be list type object, but your's: '{}', full URL({})."
        ],
        ServerError: [
            "Timeout interval exceeded from server: {}."
        ],
    }
    
    @property
    def _header(self):
        ''' Method _header class Protocol.
            Special head for platform requests.
            
        '''
        
        head = {} 
        head['Content-Type'] = 'application/json-rpc'
        
    def _error(self, ET, code, *args):
        ''' Method _error class Protocol.
            ET   - key of EType dict.
            code - index of errors node list.
            args - some str args to format.
            
        '''
        
        iType   = self.EType[ET]
        message = self.errors[iType][code]
        if args: message = message.format(*args)
        raise iType(message)
    
    def _warning(self, **params):
        ''' Method _warnings class Protocol.
            Format platform error data to simplified.
            
        '''
        
        if params['code']== -32602: self._error(0, 2) #Login name or password is incorrect.
        
        line = '\n{}\n'.format('--' * 30) 
        msg  = '\t\t!WARNING Error in server response!' + line  
        msg += '\ncode: {code} \ninformation:{data}'.format(**params)
        
        print(msg)
        return ''
    
    def _parse(self, content):
        ''' Method _parse class Protocol.
            Format decode responded content and simplified format.
            
        '''
        
        diction = content.decode()
        diction = eval(diction)
        
        time = diction['time'] = str(datetime.now()) # For virtual log.
        
        if 'error' in diction: diction = self._warning(**diction['error']) # Server Error.
        if not self.private:   self._print_data(diction)                   # Private only login.user method.
        
        self.session_data.append(diction)
        return diction
    
    def _print_data(self, data):
        ''' Method _print_data class Protocol.
            Format and print format public response data.            
            
            attributes:
                data - dict with content.
                
        '''
        
        line = '{}'.format('--' * 12)
        msg  = '\n' + line[0:-2] + 'DATA' + line[0:-2]
        txt  = ''
        
        for i in dumps(data, indent=4, sort_keys=True):
            if  not i in self._list_data: txt += i
                
        msg += txt + line*2
        
        if self._path: self._write_data(self.active_resp, txt)
        print(msg)
      
    def short_url(self, url):
        ''' Method _print_data class Protocol.
            Convert full path to main URL.     
            
            attributes:
                url - str with 'long url'.
                
        '''

        L = url.replace('http:', '').replace('/', ' ').split(" ")
        
        for i in L:
            if len(i) > 0: return i
    
    def _write_data(self, text, data=False):
        ''' Method _print_data class Protocol.
            Format and write log.    
            
            attributes:
                text - str with last Zabbix method.
                data - dict with response value.
                
        '''
        
        line = '\n{0}\n'.format('-' * 10) 
        text = line + text
        
        if data: text += data       
        text += line
        
        with open(r'%s' % self._path, 'a') as file:
            file.write(text)
        
        
class Zabbix(Protocol):
    ''' Class Zabbix self Protocol.
        Basic class to connect on zabbix server and use api.
        
        Atributes:
            _json = self.json_rpc with user data;
            _url  = server URL.
       
        Methods:
            Main:
                __init__(user, password, base_url) - class constructor;
                    user     - str  - username on server;
                    password - str  - password on server
                    base_url - str  - server url.
                    path     - file - path of txt file for save response data.
                _request(method, Json) - convert Json and request on server;
                    method - reguests.request method;
                    Json   - special zabbix json reques (self.json_rpc).
                _user_login: try connect on zabbix server;
                
                
            For User:
                get(meth, params) - send request to server;
                    meth   - str  - zabbix api meth;
                    params - dict - with meth request params.

    '''
    
    _json = {}
    _url  = None
    
    def __init__(self, user, password, base_url, _path=False):
        ''' Method __init__ class Zabbix.
            Class constructor;.
            
            Attributes: 
                    obligatory:
                        user     - str  - username on server;
                        password - str  - password on server
                        base_url - str  - server url.
                    optional:
                        path     - file - path of txt file for save response data.
                    
        '''
        
        self.user     = self._isintanse(user, 'user')
        self.password = self._isintanse(password, 'password')
        base_url      = self._isintanse(self.short_url(base_url), 'base_url')
        self._url     = self.base_url.format(base_url) if len(base_url) > 0 else self._error(0, 3)
        self.server   = base_url
        self._path    = _path
        
        self._json.update(self.json_rpc)
        self._user_login
        
    def _request(self, method, Json):
        ''' Method __init__ class Zabbix.
            Convert Json and request on server;
            
            Attributes: 
                method - reguests.request method;
                Json   - special zabbix json reques (self.json_rpc).     params - dict - with meth request params.
                    
        '''
        
        ping = self._pinger(nodes=self.server, quick=True)
        if not ping: return self._error(2, 0, self.server)
        
        response = requests.request(method, self._url, headers=self._header, json=Json)
        self.active_resp = '\nmethod:{}\nparametrs:{}'.format(Json["method"], Json["params"])

        content  = self._parse(response._content)
        
        sleep(3); Json["method"] = Json["params"] = None
        return content
    
    @property
    def _user_login(self):
        ''' Method _user_login class Zabbix.
            Connect to zabbix server use user data.
                    
        '''
        
        self.private = True
        method       = 'POST'
         
        self._json["id"]                 = randint(1, 9)
        self._json["params"]["user"]     = self.user
        self._json["params"]["password"] = self.password
        self._json["method"]             = "user.login"

        result = self._json["auth"] = self._request(method, self._json)['result']
        self.password = self.user = None
        
        msg = '\nAuthorization was successful!'
        if self._path: self._write_data(msg, '\ntime: ' + str(datetime.now()))
        
        print(msg)
        return result
    
    def get(self, meth, params):
        ''' Method get class Zabbix.
            Send request to zabbix server;
            
            Attributes: 
                meth   - str  - zabbix api meth;
                params - dict - with meth request params.
                    
        '''
        
        self.private         = False
        method               = 'GET'
        self._json["method"] = meth

        if isinstance(params, dict): self._json["params"] = params
        else:                        self._error(0, 4, type(params))         
        
        result = self._request(method, self._json)['result']     
        return result