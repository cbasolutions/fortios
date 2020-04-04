# Update certs on multiple Fortigate devices via API

### Current Version Notes:
#### Release - 2020-04-04
#### Version .1
#### Source of original version - Unknown. If you are the original writer, please message me. 

This Python script will use the Fortigate API to create or delete and create an updated SSL cert. It can be used with any PEM compliant key and full chain cert. I am using it with Let's Encrypt and this is the extent of my testing. 

To use, you need to creat a REST API Admin user in either the web portal or via the CLI.

E.g.: 
![Admin - Create New - REST API Admin](https://raw.githubusercontent.com/cbasolutions/fortios/master/Update-Cert/images/api_create.png)
![Fill in the Profile Info](https://raw.githubusercontent.com/cbasolutions/fortios/master/Update-Cert/images/api_profile.png)
![Create an Administrator Profile](https://raw.githubusercontent.com/cbasolutions/fortios/master/Update-Cert/images/api_permissions.png)


* Add your settings to config.py
* Test your update and review the logs**
* Set it via cron or a hook from your certbot updater as needed


** This script will reset any active SSL sessions because it swaps out the SSL administrative cert. Any active session will have to be restarted.  

