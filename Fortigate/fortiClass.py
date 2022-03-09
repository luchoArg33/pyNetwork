import paramiko
import re
import time

class Forti:
    """
    A class used to represent a Fortigate Firewall

    Attributes
    ----------
    ip : str
        IP of the device to ssh a connection
    user : str
        The username to connect to the device
    password : str
        username password to get access to device
    interfaces_zones : arr
        multidimensional array that contains zones and interfaces

    Methods
    --------
    getZonesInterfaces
        Gets the zones and the interfaces of the FW
        returns a multidimensional array
    getNextHop
        using a next hop prefix it returns the zone and interface
        used to forward the packet
    getInterfaceZone
        Returns the zone of a specific interface (string)
    """
    def __init__(self, ip, user, password):
        """
        Parameters
        ----------
        ip : str
            IP of the device to ssh a connection
        user : str
            The username to connect to the device
        password : str
            username password to get access to device
        """
        self.ip = ip
        self.user = user
        self.password = password
        
    def getZonesInterfaces(self):
        """Gets the zones and the interfaces of the FW.

        NOTE: It catches the zone names with regular expresions.
        They have to be in the following formats:
        ZONE \"[a-zA-Z]+\"
        Zone \"[a-zA-Z]+\"
        ZONE_Internet_1
        DMZ_Outgoing_EXT \"[a-zA-Z]+\_[a-zA-Z]+\_\d*[A-Z]*\"
        
        Interfaces names with the following formats:
        AGG_TEST.100 \"[A-Z]+\_[A-Z]+\.\d+\"
        
        If your firewall zones/interfaces are named differently you should change
        the regular expression used to match the names.
        
        Returns
        -----------
        Multidimensional array
        [['"TEST"', '"AGG_TEST.10"'],
        ['"Test"', '"AGG_TEST.20"'],
        ['"Test_Incoming_EXT"', '"AGG_TEST.30"', '"AGG_TEST.40"', '"AGG_TEST.50"', '"AGG_TEST.60"']]
        
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username = self.user, password = self.password) 
        connection = ssh.invoke_shell()
        connection.send("config vdom\n")           # Only if there are vdoms configurated, otherwise remove lines
        time.sleep(1)                              # Used otherwise script does not capture anything, too fast
        connection.send("edit XXX\n")
        time.sleep(1)
        connection.send("show system zone\n")
        time.sleep(1)
        device_output = connection.recv(10000).decode(encoding='utf-8') # Output we will parse afterwards
        connection.close()
        ssh.close()
        result = []
        new_zone = []
        # Below pattern matches everything, zone and interfaces names
        total_pattern = re.compile(r'(\"[a-zA-Z]+\_[a-zA-Z]+\_\d*[A-Z]*\"|\"[a-zA-Z]+\"|\"[A-Z]+\_[A-Z]+\.\d+\")')
        # Below pattern matches only zones, used as a control variable during iteration
        zone_pattern = re.compile(r'(\"[a-zA-Z]+\_[a-zA-Z]+\_\d*[A-Z]*\"|\"[a-zA-Z]+\")')
        matches = total_pattern.finditer(device_output)
        for match in matches:
            condition = zone_pattern.match(match.group())
            try:                                        # Verification can throw a None object or a string
                if type(condition.group()) is str:      # New zone
                    result.append(new_zone)
                    new_zone = [match.group().replace("\"","")]
            except:                                     # Interface of a zone
                new_zone.append(match.group().replace("\"",""))
        result.append(new_zone)                         # Last element
        result.pop(0)                                   # Pop the first (empty) array element
        return result
    
    def getNextHop(self, zones ,prefix):
        """Returns the output zone and interface for a specified prefix
        
        Parameters
        ----------
        zones: Array
            Generated by class method getZonesInterfaces
        prefix: str
            Any ip prefix you want to know next hop
        
        NOTE: It catches the information with regular expresions.
        IP next-hop (\*\s[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|\s[a-z]+\s[a-z]+\,|[A-Z]+\_[A-Z]+\.\d+)
        
        Interfaces names with the following formats:
        AGG_TEST.222 \"[A-Z]+\_[A-Z]+\.\d+\"
        
        If your firewall zones/interfaces are named differently you should change
        the regular expression used to match the names.
        
        It works with this command output:
        
        XXXX (XX) # get router info routing-table details 1.1.1.1

        Routing table for VRF=0
        Routing entry for 1.1.1.1/32
        Known via "static", distance 10, metric 0, best
        * 2.2.2.2, via AGG_TEST.200
        
        EUAMSFWI101 (DC) # get router info routing-table details 1.1.1.1

        Routing table for VRF=0
        Routing entry for 2.2.2.2/25
        Known via "connected", distance 0, metric 0, best
         * is directly connected, AGG_TEST.69
        Returns
        -----------
        An array = [1.1.1.1, 2.2.2.2, AGG_TEST.200]
        [prefix, next hop, interface (aggregate)]
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip, username = self.user, password = self.password) 
        connection = ssh.invoke_shell()
        connection.send("config vdom\n")           # Only if there are vdoms configurated, otherwise remove lines
        time.sleep(1)                              # Used otherwise script does not capture anything, too fast
        connection.send("edit XXXX\n")
        time.sleep(1)
        connection.send("get router info routing-table details "+prefix+"\n")
        time.sleep(1)
        device_output = connection.recv(10000).decode(encoding='utf-8')
        connection.close()
        ssh.close()
        pattern = re.compile(r'(\*\s[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+|\s[a-z]+\s[a-z]+\,|[A-Z]+\_[A-Z]+\.\d+)')
        matches = pattern.finditer(device_output)
        result =[]
        for match in matches:
            result.append(match.group())
        result[0] = result[0][2:]
        result.insert(0,prefix)
        return result
    
    def getInterfaceZone(self, zones ,interface):
        """Returns the zone of a specified interface
        
        Parameters
        ----------
        zones: Array
            Generated by class method getZonesInterfaces
        interface: str
            Interface name like AGG_TEST.23
        
        Returns
        -----------
        A zone name (string) or None
        """
        for zone in zones:
            if interface in zone:
                return zone[0]
        return None

