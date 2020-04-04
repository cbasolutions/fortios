#! /usr/bin/env python3

from datetime import date
from datetime import datetime

# Log file path - edit these to your liking
logfile_path = "/var/log/fortigate_cert_updates/"
logfile_name = "certupdate{}.log".format(date.today())

# Certificate related variables
cert_name = ""
cert_fullchain_file = ""
cert_privkey_file = ""

# Fortigates to be updated - this is a python list, to add a new element just add a comma
# to the end of the } and start with a new dictionary
#
# example my_gates = [
# {
#     "hostname": "gate1.domain.local",
#     "key":"your_key_here",
#     "port": "8443",
#     "VerifyCert": False
# },{
#       "hostname": "gate2.domain.local",
#       "key":"your_key_here",
#       "port": "8443",
#       "VerifyCert": False
# }
# ]

my_gates = [
{
    #Friendly Name of Fortigate
    "hostname": "",
    #"host_ip":"10.0.0.1",
    "key":"", #API user key
    "port": "", #Admin port number
    "VerifyCert": False
},{
    #Friendly Name of Fortigate
    "hostname": "",
    #"host_ip":"10.0.0.1",
    "key":"", #API user key
    "port": "", #Admin port number
    "VerifyCert": False
}
]

# Creating the JSON for the cert creation
cert_post_body = {
    "type": "regular",
    "certname": cert_name,
    "key_file_content": "",
    "scope": "global",
    "file_content": "",
    "password": ""
}

# Creating the JSON for for assigning the cert as the system/admin cert
cert_system_assignment = {
    "admin-server-cert": cert_name
}
