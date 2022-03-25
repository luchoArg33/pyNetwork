# Logs
The scripts on this page are used to treate logs from different devices or platforms.
I normally use pandas to process large chunks of data. 
Honestly I'm pretty impressed by the processing speed and the simplicity of the scripts needed once you've organized the data the way it's needed.

## fortiAnalyzer.py
That's a script to treat Fortianalyser traffic logs exported as CSV. I've treated 4Gb of logs. 
It uses about the doble of RAM memory and processing time will depend on your device but with a new laptop is a couple of minutes not more (even less some times).
It returns the # of hits for a particular destination IP:
'''
srcintf="XXXXX"  dstintf="XXXXXXXXXXX"          dstport=135    dstip="X.XX.XX.XX"         190
                                                dstport=1688   dstip="X.XX.XX.XX"          13
                                                dstport=18445  dstip="X.XX.XX.XX"      118626
                                                dstport=22     dstip="X.XX.XX.XX"         28
                                                dstport=25     dstip="X.XX.XX.XX"        32906
                                                dstport=3389   dstip="X.XX.XX.XX"          25
                                                               dstip="X.XX.XX.XX"           6
'''
