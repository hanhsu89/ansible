#!/usr/bin/python
import requests
import json
import sys
import getpass
import keyring

class Kcloudflare:
    def __init__(self, cfg=None):
        self.apiKey     = keyring.get_password('quydo', 'kdata_cf_key')
        self.email      = 'webmaster@kdatacdn.net'

        self.zone_api   = 'https://api.cloudflare.com/client/v4/zones'
        self.headers    = {'X-Auth-Email' : self.email, 'X-Auth-Key' : self.apiKey, 'Content-Type': 'application/json'}
        self.zone       = None
        self.zone_id    = None
	self.zone_type	= None
	self.ip         = None
        self.domain     = None
        self.proxy      = False

        if cfg:
            for key, val in cfg.items():
                setattr(self, key, val)

    def _valid(self):
        if self.domain is None:
            sys.exit('domain is required')

        if self.ip is None:
            sys.exit('ip is required')

        if self.zone_type is None:
            sys.exit('Zone type is required')

        self.set_zone('.'.join(self.domain.split('.')[-2:]))
        self.get_zone_id_from_zone()

    def add_config(self, cfg=None):
        if cfg:
            for key, val in cfg.items():
                setattr(self, key, val)


    def set_zone(self, zone):
        self.zone = zone


    def set_zone_id(self, zone_id):
        self.zone_id = zone_id


    def get_zone_id(self):
        return self.zone_id


    def get_zone_id_from_zone(self):
        '''
        get zone id
        '''
        zoneUrl = "%s?name=%s" % (self.zone_api, self.zone)
        r = requests.get(zoneUrl, headers=self.headers)
        data = json.loads(r.text)
        try:
            self.zone_id = data.get("result")[0].get("id")
        except:
            self.zone_id = None

    def set_zone_type(self, zone_type):
        self.zone_type = zone_type


    def get_zone_type(self):
        return self.zone_type


    def get_record(self):
        '''
        get record
        '''
        recordUrl = "%s/%s/dns_records" % (self.zone_api, self.get_zone_id())
        payload = {"name": self.domain, "type": self.get_zone_type()}
        r = requests.get(recordUrl, headers=self.headers, params=payload)
        data = json.loads(r.text)
        return [{"content": ip.get("content"), "id": ip.get("id"), "proxied": ip.get("proxied")} for ip in data.get("result")]


    def remove_record(self, record_id):
        self._valid()
        remove_url = "%s/%s/dns_records/%s" % (self.zone_api, self.get_zone_id(), record_id)
        res = requests.delete(remove_url, headers=self.headers)
        print res.text

    def add_record(self):
        '''
        add record
        '''
        self._valid()

        existIp = self.get_record()
        createUrl = "%s/%s/dns_records" % (self.zone_api, self.get_zone_id())
        if len(existIp) > 0:
            return {'status': False, 'msg': 'domain existed', 'data': existIp}

            for ipInfo in existIp:
                print(ipInfo)
            nextStep = raw_input("Update or Add or Cancel? (U/A/C): ")
            if nextStep.upper() == "A":
                data = '{"type": "%s","name": "%s","content": "%s", "proxied": %s}' % (zType, name, content, proxied)
                r = requests.post(createUrl, headers=self.headers, data=data)
                print("Added another record!")
            if nextStep.upper() == "U":
                recordId = raw_input("Paste above record id: ")
                updateUrl = "%s/%s" % (createUrl, recordId)
                data = '{"type": "%s","name": "%s","content": "%s", "proxied": %s}' % (zType, name, content, proxied)
                r = requests.put(updateUrl, headers=self.headers, data=data)
                print(r.text)
                print("Updated")
            else:
                print("Done")
        else:
            for i in self.ip:
                data = '{"type": "%s","name": "%s","content": "%s", "proxied": %s}' % (self.get_zone_type(), self.domain, i, self.proxy)
                r = requests.post(createUrl, headers=self.headers, data=data)

            return {'status': True, 'msg': 'domain added'}

    def get_zone(self, domain):
        if self.zone:
            return self.zone
        self.zone = '.'.join(domain.split('.')[-2:])
        return self.zone


if  __name__ == '__main__':
    cfg = {
        'domain': 'test111.kdatacdn.net'
        ,'zone_type': 'A'
        ,'ip': ['123.30.171.236', '123.30.171.254']
        ,'proxy': False
    }
    kcf = Kcloudflare(cfg)
    record_id = 'fccf3338a12ef0573becd9afa48652d6'
    kcf.remove_record(record_id)
    sys.exit()

    cfg = {
        'domain': 'test111.kdatacdn.net'
        ,'zone_type': 'A'
        ,'ip': ['123.30.171.236', '123.30.171.254']
        ,'proxy': False
    }
    print kcf.add_record()
