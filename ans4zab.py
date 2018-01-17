# (c) 2018 Gorilla Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    callback: ans4zab
    callback_type: notification
    requirements:
      - whitelist in configuration
    short_description: sends events to a zabbix server
    version_added: ""
    description:
      - This plugin logs ansible-playbook and ansible runs to a zabbix server
    options:
      server:
        description: zabbix server that will receive the event
        env:
        - name: ZABBIX_SERVER
        default: localhost
      port:
        description: port on which zabbix server is listening
        env:
          - name: ZABBIX_PORT
        default: 10051
      debugPath:
        description: debug path to dump zabbix results (ie if you set /tmp, a file /tmp/zab_trace_<hostname> will be generated)
        env:
          - name: ZABBIX_DBGPATH
        default: none
'''



import os
import struct
import json
import codecs
import logging
import logging.handlers
import socket

from pyzabbix import ZabbixMetric, ZabbixSender
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    logs ansible-playbook and ansible runs to a zabbix server
    """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'ans4zab'
    CALLBACK_NEEDS_WHITELIST = True
    address = 'localhost'
    port = 10051
    debugPath = 'none'
    fileDebug = ''

    def __init__(self):

        super(CallbackModule, self).__init__()

        self.logger = logging.getLogger('ansible logger')
        self.logger.setLevel(logging.DEBUG)

        self.address=os.getenv('ZABBIX_SERVER', 'localhost')
        self.port=int(os.getenv('ZABBIX_PORT', 10051))
        self.debugPath=os.getenv('ZABBIX_DBGPATH', 'none')

        self.hostname = socket.gethostname()

    def debugInit(self,host):
        if self.debugPath != 'none':
         self.fileDebug = open(self.debugPath + "/zab_trace_" + host,"w")

    def traceLog(self,msg):
        if self.debugPath != 'none':
         self.fileDebug.write(msg + "\n")

    def debugClose(self):
        if self.debugPath != 'none':
         self.fileDebug.close


    def sendZabb(self,key,value,host,res):
        self.debugInit(host)
        self.traceLog("address zabbix=" + self.address)
        self.traceLog("   port zabbix=" + str(self.port))
        self.traceLog(" Sending " + key + "=" +  value)
        try:
          packet = [
                    ZabbixMetric(host, key, value),
                   ]
          result = ZabbixSender(self.address,self.port).send(packet)
          self.traceLog("Result is:" + str(result))
        except Exception as e:
          self.traceLog("   /!\ Error:" + str(e))
        finally:
          self.debugClose()

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.sendZabb("ansible_result","failed",host,self._dump_results(res))

    def runner_on_ok(self,host, res):
        self.sendZabb("ansible_result","ok",host,self._dump_results(res))

    def runner_on_skipped(self, host, item=None):
        self.sendZabb("ansible_result","skipped",host,"skipped")

    def runner_on_unreachable(self, host, res):
        self.sendZabb("ansible_result","unreachable",host,self._dump_results(res))

    def runner_on_async_failed(self, host, res, jid):
        self.sendZabb("ansible_result","async_failed",host,self._dump_results(res))

    def playbook_on_import_for_host(self, host, imported_file):
        self.sendZabb("ansible_result","import_for_host",host,imported_file)

    def playbook_on_not_import_for_host(self, host, missing_file):
        self.sendZabb("ansible_result","playbook not imported",host,missing_file)
