# fortiClass.py
It's a class with a couple of methods. 
In order to obtain information you can do:
```
from fortiClass import Forti
help(Forti)
```
Class dependencies
```
import paramiko
import re
import time
```
#### Sample code 
Obtain next hop:
```
from fortiClass import Forti

ip = 'X.X.X.X'
user = 'XXXXXXX'
password = 'XXXXX'
firewall = Forti(ip, user = user, password = password)
zones = firewall.getZonesInterfaces()
next_hop = firewall.getNextHop(zones,"X.X.X.X")
print(next_hop)
```
