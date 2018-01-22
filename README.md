# ans4zab
Upload ansible reporting to zabbix management

# Requirement 

You need to install py-zabbix (pip install py-zabbix)

# Installation

   1. Authorize ansible to use callback ans4zab
      In /etc/ansible/ansible.cfg, ensure this line is uncomment and contains ans4zab
      
      ```callback_whitelist = ans4zab```
   
   2. Copy ans4zab into plugins directory callback (ie : ```~/.ansible/plugins/callback```)
   
# Use 

   1. 2 env variables :
   
      This one indicates zabbix server address
      
      ```export ZABBIX_SERVER=myzabbixserver.com``` mandatory !
      
      This one incidates zabbix server port (default is 10051)
      
      ```export ZABBIX_PORT=10051``` optionnal !
      
      This on indicates if you want return of zabbix, (ie if you set /tmp, a file /tmp/zab_trace_<hostname> will be generated)
  
      ```export ZABBIX_DBGPATH=/tmp``` optionnal !
      
  # Zabbix side    
  
  You need to configure template, items and triggers into zabbix interface.
   
  Items:
  
  ![zabbix_items](https://github.com/coxifred/ans4zab/blob/master/zabbix_ansible/zabbix_item.jpg "zabbix_items")
      
  Triggers:
  
  ![zabbix_triggers](https://github.com/coxifred/ans4zab/blob/master/zabbix_ansible/zabbix_trigger.jpg "zabbix_triggers")
  
  Main page:
  
  ![zabbix_mp](https://github.com/coxifred/ans4zab/blob/master/zabbix_ansible/zabbix_playbook.jpg "zabbix_mp")

  or you can import template zbx_export_templates_ansible.xml (present in root of this repo)
  
