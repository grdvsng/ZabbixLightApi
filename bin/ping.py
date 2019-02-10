from os  import system, name as osname
from subprocess import Popen as popen, PIPE
import locale


''' Module EasyPing.
    Version: 0.8
    Author:  Trishkin Sergey.
    Mail:    grdvsng@gmail.com
        
    used modules:
        os;
        subprocess;
        locale.
        
    Module can help your made fast ping and receive response in special diction or just boolean.
    It's 100% work in Windows and %50% Linux because i test it only in windows and vertual machine.
    
    You can use next query keys:
        count    - This option sets the number of ICMP Echo Requests to send, from 1 to 4294967295. 
                   The ping command will send 4 by default if -n isn't used.;
        size     - Use this option to set the size, in bytes, of the echo request packet from 32 to 65,527. 
                   The ping command will send a 32-byte echo request if you don't use the -l option.;
        TTL      - This option sets the Time to Live (TTL) value, the maximum of which is 255.;
        interval - Specifying a timeout value when executing the ping command adjusts the amount of time, in milliseconds, that ping waits for each reply. If you don't use the -w option, the default timeout value of 4000 is used, which is 4 seconds..
            
        **I'm use this site: https://www.lifewire.com/ping-command-2618099
                for give fine make a description.
    
    Main Class EasyPing.
        
    Converter Class for formate stdin:
    ------------------------------------    
              Base_converter
             /              \
     NT_converter       Posix_converter   
    ------------------------------------    
    
    And finally:
        Sorry my English and you found error in script let me know.

'''


class Base_converter:
    ''' Class Base_converter.
        Same method for NT_converter and Posix_converter.
        Can normal work only in this module, but if you try to use in other can be mistake.
        
        Attributer:
            user_platform - key of user platform for specific platform formated.
            
        Methods(+ lambda):
           _parse(values) - 
                parse clean list(values) from platform converter to special diction where:
                    key   - key from response_val;
                    value - response ping 'clean' value.
           
           _parse_list(L) - 
                parse dirt values from platform converter to clean values and str with other dirt values. 
       
    '''
    
    return_int    = lambda self, x: x if isinstance(x, (int, float)) else x[0]
    user_platform = None
    
    def _parse_list(self, L):
        ''' Method _parse_list class Base_converter.
            Parse dirt values from platform converter to clean values and str with other dirt values. 
            
            parameters:
                L - with string from platform converter.
            
        '''
        
        cur  = []
        temp = ''
        
        for i in L:
            try:
                node = self.return_int(eval(i))
                cur.append(node)
            except: 
                if '%' in i and self.user_platform == 'posix'\
                and len(i) <= 3 \
                and isinstance(int(i[0:1]), int): cur.append(i)
                else:                             temp += ' ' + i
        return cur, temp

    def _parse(self, values):
        ''' Method _parse_list class Base_converter.
            parse clean list(values) from platform converter to special diction.
            
            parameters:
                values - values clean list from platform converter and method _parse_list.
            
        '''
        
        result = dict(zip(self.response_val, values))
        result['availability'] = True
        
        return result   
        
    def short_url(self, url):
        ''' Method short_url class Base_converter.
            parse clean list(values) from platform converter to special diction.
            
            parameters:
                url - str with full url.
            
        '''
        
        L = url.replace('http:', '').replace('/', ' ').split(" ")
        
        for i in L:
            if len(i):
                return i

                
class NT_converter(Base_converter):
    ''' Class NT_converter self Base_converter.
        Attributes:
            None.
            
        Methods:
            __init__  - set master response_val and user_platform;
            __call__  - just return method converter;
            converter - convent and format dirt stdin value to special diction (with use master method).
            
    '''
    
    def __init__(self, D):
        ''' Method __init__ class NT_converter.
            Set master response_val and user_platform.
            
            Arguments:
                D - dict response_val from class EasyPing.
                
        '''
        
        self.response_val  = D
        self.user_platform = 'nt'
        
    def __call__(self, _str, quick=None):
        ''' Method __call__ class NT_converter.
            Just return method converter, please read converter DOC;
                
        '''
        
        return self.converter(_str, quick)
    
    def converter(self, _str, quick):
        ''' Method converter class NT_converter.
            Convent and format dirt stdin value to special diction (with use master method).
             
            Attribute:
                _str  - dirt stdin str from EasyPing;
                quick - if quick method make light formating.
                
        '''
        
        
        L       = _str.split("\n")
        _string = ''
        start   = False 
        
        for i in L:
            if start:       _string += i
            if 'Ping' in i: start    = True
        
        nodes, temp = self._parse_list(_string.split(" "))
        
        if len(nodes) < 5:
            if quick: return False
            else:     return {'availability': False}
        
        if quick: return True   
        return self._parse(nodes)
    
    
class Posix_converter(Base_converter):
    ''' Class NT_converter self Base_converter.
        Attributes:
            None.
            
        Methods:
            __init__  - set master response_val and user_platform;
            __call__  - just return method converter;
            converter - convent and format dirt stdin value to special diction (with use master method).
            
    '''
    
    def __init__(self, D):
        ''' Method __init__ class NT_converter.
                Set master response_val and user_platform.
                
                Arguments:
                    D - dict response_val from class EasyPing.
                    
        '''
    
        self.response_val = D
        self.platform     = 'posix'
        
    def __call__(self, _str, quick=False):
        ''' Method __call__ class NT_converter.
            Just return method converter, please read converter DOC;
                
        '''
        
        return self.converter(_str, quick)
            
    def converter(self, _str, quick):
        ''' Method converter class NT_converter.
            Convent and format dirt stdin value to special diction (with use master method).
             
            Attribute:
                _str  - dirt stdin str from EasyPing;
                quick - if quick method make light formating.
                
        '''
        
        _string = ''
        _start  = False
        
        for i in _str.split("---"): 
            if _start:                 _string += i
            if 'ping statistics' in i: _start   = True
        
        L1, temp = self._parse_list(_string.replace('=', ' ').split(' '))
        L2, temp = self._parse_list(temp.replace(' ', '/').split("/"))
        nodes = L1 + L2
        
        if len(nodes) < 6:
            if quick: return False
            else:     return {'availability': False}
        
        if quick: return True 
        return self._parse(nodes)
    
    
class EasyPing:
    ''' Class EasyPing.
        This is cross platform realization of ping for check node(s) availability.
        Only for Linux and Windows.
        
        Attributes:
        
        |-----Name----|----Type----|----Description----|
        |basis        |    dict    | Same for platforms command ping start keys.                    
        |platform     |    dict    | Special command ping start keys unique for platform.              
        |last_resul   |    str     | String with formated values with last ping session.                
        |resp_all     |    list    | Same for two  platform ping return values like send, lose and etc.            
        |response_val |    dict    | Sequence and unique ping return values for platform.      
        |errors       |    dict    | Special diction where key error type and val is list with str to errors format.             
        |converter    |    dict    | Diction where keys is OS names and values is class of converter(parser) for format return values.             
        |enc          |    str     | Prefer platform decoder.                   
        |-------------|------------|-------------------|                                    
        
        Public methods:
            ping(nodes, count, size, ttl, interval, quick):
                nodes    - with URL or List with URLS.
                count    - int with count of send;
                size     - int with packetsize;
                ttl      - int with TLL value;
                interval - int with time send interval;
                quick    - boolian if you need return true if node 
        
        Other method are privates, please don't touch them if you need just ping.
                
    '''
    
    # I ignore flood ping keys, because them haven't mean in script.
    basis = { # Independent on platforms ping Key for.
        'count':    None,
        'size':     None,
        'tll':      '-i',
        'interval': '-w'
    } 
    
    # Dependent on platform ping Key. 
    platform = {
        'nt':    ('-n', '-l'),
        'posix': ('-c', '-s')
    }
    
    last_resul     = None # if user want print result.

    # Response value for parse.
    resp_all = [
        'bytes',
        'send',
        'received',
        'lose',
        'low_ping',
        'max_ping',
        'average_ping',
        ]
    
    response_val = {
        'nt': [
            resp_all[1],
            resp_all[2],
            resp_all[3],
            resp_all[4],
            resp_all[5],
            resp_all[6] 
        ],
        'posix': [
            resp_all[1],
            resp_all[2],
            resp_all[3],
            resp_all[4],
            resp_all[6] ,
            resp_all[5],
            'mdev'
        ]
        
    }
    
    # Script internal errors.
    errors = {
        ValueError: [
            "Argument '{}' must be <int> or <float> not: {}.",
            "Node must be <str>, but your's: {}.\nCheck URL: '{}'",
        ]
    }
    
    # Special convener stdin result. 
    converter = {
        'nt':    NT_converter(response_val['nt']),
        'posix': Posix_converter(response_val['posix'])
    }
    # prefer encoding for decode msg.
    enc = locale.getpreferredencoding()
    
    def __init__(self):
        ''' Method __init__ class EasyPing
            Set parameters val to platform:
                1 format OS name to default;
                2 create exemplar of converter class by platform.
                3 set special values for platform ping (count and size);
                
        '''
        
        name           = osname.lower()
        self.converter = self.converter[name]
        
        self.basis['count'], self.basis['size']  = self.platform[name]
        
    def _parse(self, *args):
        ''' Method _parse class EasyPing
            parameters:
                args - method ping args.
                parse values and append to special str with full system command.
                
        '''
        
        temp = [i for i in self.basis.keys()] # List with all system ping keys.
        ping = 'ping'

        for i in args:
            form = temp[args.index(i)]
            if i:
                if not (isinstance(i, int) or isinstance(i, float)): 
                    self._errors(ValueError, 0, *(form, type(i)))
                else: ping += ' {} {}'.format(self.basis[form], round(i))
        return ping

    def  _errors(self, key, n, *args):
        ''' Method _errors class EasyPing
            parameters:
                key   - class of error-type;
                n     - number of error;
                *args - str or many str for format error value in error string.
                
        '''

        txt = self.errors[key][n].format(*args)
        raise key('\a\n\n' + txt + '>nul \n if %error% echo Hello World!')

    def ping(self, nodes, count=4, size=32, ttl=None, interval=4000, quick=False):
        ''' Method _errors class EasyPing.
            Main module method.
            
            ping(nodes, count, size, ttl, interval, quick):
                nodes    - with URL or List with URLS.
                count    - int with count of send;
                size     - int with packetsize;
                ttl      - int with TLL value;
                interval - int with time send interval;
                quick    - boolian if you need return true if node 
            
            If you need quick boolean response use parameter quick=True.
            Program return you True if nod is availability and false if not or list with values.
                
        '''
        
        # Formated command for system request.
        _ping  = self._parse(count, size, ttl, interval)
        result = {}
        
        # For program script work.
        if not isinstance(nodes, (list, tuple)): nodes = [nodes]

        for i in nodes:
            # Check URL standard value.
            if not isinstance(i, str): self._errors(ValueError, 1, type(i), i)
            # Create process and read stein.
            url  = self.converter.short_url(i)
            pip  = popen(_ping + ' ' + url, stdout=PIPE)
            while pip.poll(): pass
            
            # Decode bytes and ignore error, for Slavic and Latin symbols its working, other don't know.
            _str      = pip.stdout.read().decode(self.enc, "ignore")
            # Convert 'dirt' stdin string to script format (read Converter class DOC).
            result[i] = self.converter(_str, quick)
 
        if quick:
            if len(result) == 1: return result[i]
        
        self.last_result = self._printer(result) # Only printer     
        return result

    def _printer(self, D):
        ''' Method _printer class EasyPing.
            Format and print ping format values.
            
            parameters:
                D - diction with ping formated values + formated keys;
                
        '''

        line   = '\n{}\n'.format('--' * 15)
        result = ''
        
        for k in D.keys():
            result += ('\n{}'.format(k) + line)
            for k,v in D[k].items(): 
                result += ('\n\t{}: {}'.format(k, v))
            result += ('\n')
            print(result)
        return result

    def __str__(self):
        ''' Method __str__ class EasyPing.
            Print class attribute last_result.

        '''
        
        print('\nLast ping result\n')
        return self.last_result
        
    def __call__(self, **args):
        ''' Method __call__ class EasyPing.
            Return method ping.

        '''
        
        return self.ping(**args)