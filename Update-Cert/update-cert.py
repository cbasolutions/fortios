#! /usr/bin/env python3

import requests
import json
import urllib3
import sys
import base64
from datetime import date
from datetime import datetime
import time
import os
from config import *

# disable security warning for SSL certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setting up some basic logging - nothing fancy, just need to keep track of what happens
def writelog(logmessage):
    # If the folder where the log file should be doesn't exist, create it
    if not os.path.exists(logfile_path):
        os.mkdir(logfile_path)

    with open("{}{}-{}".format(logfile_path, date.today(), logfile_name), "a+") as logfile:
        logfile.write("\n\r{}".format(logmessage))


def PrepareCert(cert_file):
    # Declaring some variables we'll be using to prepare our certs
    cert_list = []
    prepared_cert = ""

    file = open(cert_file, "r")
    file_content = file.read()
    file.close()
    file_content = file_content.replace('\n\n','\n',1)
    file_content = file_content[:file_content.rfind('\n')]
    prepared_cert = base64.b64encode(file_content.encode()).decode('ascii')
    return prepared_cert

writelog(" ")
writelog("Starting Script {}".format(datetime.now()))

# Reading the cert files
writelog("Reading Certificate Files")

# Setting up our cert vairables
cert_fullchain = PrepareCert(cert_fullchain_file)

# Prepare the private key to be one long string
cert_privkey = PrepareCert(cert_privkey_file)

cert_post_body["file_content"]=cert_fullchain
cert_post_body["key_file_content"]=cert_privkey

writelog(" ")
writelog(json.dumps(cert_post_body))

# Now we get down to business - for each gate in the config file do the following
for gate in my_gates:
    # Setting up variables for ease of reading
    hostname = gate["hostname"]
    api_key = gate["key"]
    VerifyTrustedCert = gate["VerifyCert"]
    gate_port = gate["port"]

    writelog("Attempting to update the cert on {}".format(gate["hostname"]))
    access_url = "https://{}:{}/api/v2/cmdb/certificate/local/{}?access_token={}".format(hostname, gate_port, cert_name, api_key)
    writelog(access_url)
    # Check and see if the certificate exists
    response = requests.get(access_url, verify=VerifyTrustedCert)
    writelog("reponse code is: {}".format(response.status_code))
    # If the cert isn't present, then create it
    if response.status_code != 200:
        writelog("Could not find the cert - creating")
    else:
        writelog("Assigning Fortinet_Factory as SSL VPN server cert")
        access_url = "https://{}:{}/api/v2/cmdb/vpn.ssl/settings?access_token={}".format(hostname, gate_port, api_key)
        writelog(access_url)
        response = requests.put(access_url, json={'servercert': 'Fortinet_Factory'}, verify=VerifyTrustedCert)
        writelog("response code is: {}".format(response.status_code))

        writelog("Assigning Fortinet_Factory as admin cert")
        access_url = "https://{}:{}/api/v2/cmdb/system/global?access_token={}".format(hostname, gate_port, api_key)
        writelog(access_url)

        try:
            cert_assignment = requests.put(access_url, json={'admin-server-cert': 'Fortinet_Factory'}, verify=VerifyTrustedCert)
            if cert_assignment.status_code == 200:
                writelog("Cert successfully assigned as management cert")
            else:
                writelog("An error occurred, the details are:\n {}".format(cert_system_assignment.text))
        except urllib3.exceptions.ProtocolError:
            current_settings = requests.get(access_url, verify=False)
            print(current_settings.json()["results"]["admin-server-cert"])
        except requests.exceptions.ConnectionError:
            current_settings = requests.get(access_url, verify=False)
            print(current_settings.json()["results"]["admin-server-cert"])
        except Exception as e:
            writelog("An error occurred, the details are:\n {}".format(e))

        writelog("Attempting to delete exisitng cert on {}".format(gate["hostname"]))

        access_url = "https://{}:{}/api/v2/cmdb/vpn.certificate/local/{}?access_token={}".format(hostname, gate_port, cert_name, api_key)
        writelog(access_url)
        # Check and see if the certificate exists
        response = requests.delete(access_url, verify=VerifyTrustedCert)
        writelog("reponse code is: {}".format(response.status_code))

    # request and create the cert
    access_url = "https://{}:{}/api/v2/monitor/vpn-certificate/local/import?access_token={}".format(hostname, gate_port, api_key)
    writelog(access_url)
    writelog("cert_post_body equals: \n {}".format(cert_post_body))
    cert_update = requests.post(access_url, json=cert_post_body, verify=VerifyTrustedCert)
    writelog(cert_update.json())
    if cert_update.status_code == 200:
        writelog("Cert successfully installed, making default system cert")
        # assign the cert as the default for management gui
        access_url = "https://{}:{}/api/v2/cmdb/system/global?access_token={}".format(hostname, gate_port, api_key)
        writelog(access_url)
        writelog("cert assignment equals: \n {}".format(cert_system_assignment))
        try:
            cert_assignment = requests.put(access_url, json=cert_system_assignment, verify=VerifyTrustedCert)
            if cert_assignment.status_code == 200:
                writelog("Cert successfully assigned as management cert")
            else:
                writelog("An error occurred, the details are:\n {}".format(cert_system_assignment.text))
        except urllib3.exceptions.ProtocolError:
            current_settings = requests.get(access_url, verify=False)
            print(current_settings.json()["results"]["admin-server-cert"])
        except requests.exceptions.ConnectionError:
            current_settings = requests.get(access_url, verify=False)
            print(current_settings.json()["results"]["admin-server-cert"])
        except Exception as e:
            writelog("An error occurred, the details are:\n {}".format(e))
        # set cert to VPN cert
        writelog("Assigning {} as SSL VPN server cert".format(cert_system_assignment))
        access_url = "https://{}:{}/api/v2/cmdb/vpn.ssl/settings?access_token={}".format(hostname, gate_port, api_key)
        writelog(access_url)
        response = requests.put(access_url, json={'servercert': cert_name}, verify=VerifyTrustedCert)
        writelog("response code is: {}".format(response.status_code))
    else:
        writelog("An error occurred, the details are:\n {}".format(cert_update.text))
