# fortiClass.py
It's a class with a couple of methods for Fortigate.
It uses paramiko to connect to CLI and send commands. It collects logs and then parses then with regular expressions.
Do not use it as is. Check the outputs of your device, modify regular expressions if you need to, verify the commands that are sent in the class (vdom commands for example).

In order to obtain detailed information you can do:
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

next_hop => ['X.X.X.X', '* X.X.X.X', 'AGG_TEST.100']
```
