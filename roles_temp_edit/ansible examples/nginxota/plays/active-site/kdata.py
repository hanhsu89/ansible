#!/usr/bin/python2.7

import requests
import hashlib
import json
import re
from datetime import datetime
import optparse
import subprocess
#import MySQLdb
from datetime import datetime
import sys
import os

from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from kcloudflare import Kcloudflare as Kcf


'''
Kdata push notify
'''
class Knotify:
    def __init__(self):
        self.url = 'http://bot.1ly.co:7000/push'
        self.messenger = 'Telegram'
        self.receiver = 'kdatacdn'

    def push(self, msg):
        try:
            data = {
                'content': '{} | {}'.format(datetime.now(), msg),
                'messenger': self.messenger,
                'receiver': self.receiver,
            }
            requests.post(self.url, data=data)
        except:
            pass

'''Kdata Ansible class'''
class Kansible:
    def __init__(self, cfg=None):
        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.host_list = '/usr/local/sbin/ansible-role-diepdj/roles/ansible-role-nginx/production'
        self.playbook_path = '/home/d4jk4/kdata/test.yml'

        if cfg:
            if 'host_list' in cfg.keys():
                self.host_list = cfg['host_list']
            if 'playbook_path' in cfg.keys():
                self.playbook_path = cfg['playbook_path']


    def set_host_list(self, path):
        if not os.path.exists(path):
            sys.exit('path {} does not exists'.format(path))

        self.host_list = path


    def set_playbook_path(self, pb_path):
        if not os.path.exists(pb_path):
            sys.exit('path {} does not exists'.format(pb_path))

        self.playbook_path = pb_path


    def test(self):
	inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager,  host_list=self.host_list)
	if not os.path.exists(self.playbook_path):
	    print '[INFO] The playbook does not exist'
	    sys.exit()

	Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection','module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
	options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh', module_path=None, forks=100, remote_user='root', private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True, become_method=None, become_user='root', verbosity=None, check=False)

	#self.variable_manager.extra_vars = {'hosts': 'mywebserver'} # This can accomodate various other command line arguments.`

	passwords = {}

	pbex = PlaybookExecutor(playbooks=[self.playbook_path], inventory=inventory, variable_manager=self.variable_manager, loader=self.loader, options=options, passwords=passwords)

        print self.playbook_path

	results = pbex.run()
        print results


'''Kdata class'''
class Kdata:

    vhost_template_file = 'yaml_tpl'
    log_file = 'kdata_cdn_log'
    nginx_cache_dir = '/var/cache/nginx/'

    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_pass = 'manutd'
    mysql_db = 'kdata'
    domain_table = 'domain'

    uri_caches_url = 'https://kdatacdn.com/api/domains/removeCache'
    uri_caches_update_url = 'https://kdatacdn.com/api/domains/removeCache/done'
    domains_pending_url = 'https://kdatacdn.com/api/domains/pending'
    domains_update_url = 'https://kdatacdn.com/api/domains/update'

    must_check_valid_domain = False
    must_check_valid_origin = False

    def __init__(self):
        #self.db = MySQLdb.connect(
                    #self.mysql_host,
                    #self.mysql_user,
                    #self.mysql_pass,
                    #self.mysql_db
                #)
        #self.db_cursor = self.db.cursor()

        #elf.kcf = Kcf()
        pass

    def push_noti(self, data):
        knotify = Knotify()
        knotify.push(data)


    def close_db(self):
        self.db.close()


    def _db_escape_string(self, val):
        if type(val) is str:
            return MySQLdb.escape_string(val)
        else:
            return val


    def _db_domain_fetch_all(self):
        q = 'select * from {}'.format(self.domain_table)
        self.db_cursor.execute(q)

        columns = self.db_cursor.description
        data = self.db_cursor.fetchall()
        if data is None:
            return data

        rows = []
        for row in data:
            res = {}
            for i in range(0, len(row)):
                res[columns[i][0]] = row[i]
            rows.append(res)

        return rows


    def _db_domain_fetch_one_by_kdata_id(self, kid):
        if type(kid) is not int:
            return False

        q = 'select * from {} where domain_id={}'.format(self.domain_table, self._db_escape_string(kid))
        self.db_cursor.execute(q)

        columns = self.db_cursor.description
        data = self.db_cursor.fetchone()
        if data is None:
            return data

        res = {}
        for i in range(0, len(data)):
            res[columns[i][0]] = data[i]

        return res

    def _db_domain_fetch_one(self, id):
        if type(id) is not int:
            return False

        q = 'select * from {} where id={}'.format(self.domain_table, self._db_escape_string(id))
        self.db_cursor.execute(q)

        columns = self.db_cursor.description
        data = self.db_cursor.fetchone()
        res = {}
        for i in range(0, len(data)):
            res[columns[i][0]] = data[i]

        return res


    def _db_domain_update(self, id, data):
        if not isinstance(id, int):
            return False

        if not data:
            return False

        sets = []
        for k, v in data.items():
            sets.append('{}="{}"'.format(k, self._db_escape_string(v)))

        query = 'update {} set {} where id={}'.format(self.domain_table, ','.join(sets), id)
        try:
            self.db_cursor.execute(query)
            self.db.commit()
        except:
            self.db.rollback()

        return self.db_cursor.rowcount


    def _db_domain_add(self, data):
        '''
        add new row in script db
        '''
        fields = []
        values = []

        for k, v in data.items():
            fields.append(k)
            values.append(self._db_escape_string(v))

        query = 'insert into {}({}) values({})'.format(self.domain_table, ', '.join(fields), '"{}"'.format('", "'.join(values)))

        try:
            self.db_cursor.execute(query)
            self.db.commit()
        except:
            self.db.rollback()
            self._log('can not insert new script db row - {}'.format(data))
            return False

        return self.db_cursor.lastrowid


    def _res_bool(self, boolean_):
        '''
        return boolean and close db
        '''
        self.close_db()
        self._log('-----------------------------------------------\n\n')
        return boolean_

    def _debug(self, val):
        print val
        sys.exit()


    def _log(self, msg):
        '''
        log function
        '''
        with open(self.log_file, 'a') as f:
            f.write('{}|{}\n'.format(str(datetime.now()), msg))


    def get_domains_from_api(self, has_vhost='0'):
        '''
        get domains
        '''
        try:
            res = requests.get(self.domains_pending_url)
        except:
            return {}

        if res.status_code != 200:
            return {}

        js = json.loads(res.text)
        if js['status'] != 'true':
            return {}

        return js['data']


    def remove_cache_uri(self):
        '''
        process remove cache uris
        cache uris from kdata cdn api
        '''
        try:
            res = requests.get(self.uri_caches_url)
        except:
            self._log('remove_cache_uri can not connect API')
            return False

        if res.status_code != 200:
            self._log('remove_cache_uri api response != 200 - {}'.format(res.status_code))
            return False

        js = json.loads(res.text)
        if js['status'] != 'true':
            self._log('can not load remove_cache_uri api response')
            return False

        for uri in js['data']:
            domain = uri['user_domain']['domain']
            url_files = uri['url_files']
            cache_id = uri['id']

            with open('{}.uris'.format(domain), 'a') as f:
                if url_files == 'all':
                    f.write('- {}\n'.format(url_files))
                else:
                    f.write('- {}\n'.format(self.get_nginx_cache_path(url_files)))

            'write to template'
            self.update_uri_cache(cache_id)


    def get_nginx_cache_path(self, uri):
        '''
        generate nginx cache path from uri
        '''
        m = hashlib.md5()
        m.update(uri)
        md5 = m.hexdigest()
        last_char = md5[-1:]
        near_char = md5[-3:-1]

        return '{}{}/{}/{}'.format(self.nginx_cache_dir, last_char, near_char, md5)


    def update_uri_cache(self, cid):
        '''
        update status for line cache
        '''
        try:
            posts = {'id': cid}
            requests.post(self.uri_caches_update_url, data=posts)
        except:
            return False

        return True


    def update_domain_kdata_cdn(self, domain_id, status, msg):
        '''
        update domain status for KdataCDN backend
        + id: id domain
        + status: in_array(1,2,3)  1: pending, 2 done, 3 deactivate
        + messages: required when status = 1,
          - messages : domain.err_domain, domain.err_origin_server
        '''
        try:
            posts = {'id': domain_id, 'status': status, 'messages': msg}
            res = requests.post(self.domains_update_url, data=posts, verify=False)
        except:
            return False

        try:
            js = json.loads(res.text.decode('utf-8'))
            if js['status'] != 'true':
                return False
        except:
            self._log('can not decode update_domain api response')
            return False

        print res.text
        return True


    def get_cdn_origin(self, full_origin, domain):
        '''
        get origin server:port
        '''
        s = re.search(r'(.*)://([^/]*)', full_origin)

        try:
            self._log('got origin {} for domain {} - {}'.format(s.group(1), full_origin, domain))

            protocol = s.group(1)
            domain = s.group(2)

            ports = {'http': '80', 'https': '443'}

            if domain.find(':') != -1:
                return domain
            else:
                return '{}:{}'.format(domain, ports[protocol])

            return s.group(1)
        except:
            self._log('can not get origin for domain {}'.format(full_origin))
            return None

    def process_pending_domains(self):
        '''
        process pending domain
        - get list domains from kdata cdn
        - check is exist in script_data -> next
        - insert into script_data in wait_call_cdn_node mode
        '''

        # read cdn node vhost template
	with open(self.vhost_template_file) as f:
	    template_data = f.read()

        # get all kdata cdn domains
        domains = self.get_domains_from_api('0')
        for item in domains:
            '''
            {u'status': 1, u'domain': u'cdn.1ly.co', u'user_id': 10, u'origin_server': u'http://kdata.1ly.co', u'created_at': u'2016-10-26 11:45:25', u'messages': u'domain.err_domain', u'updated_at': u'2016-10-27 11:09:01', u'kdata_domain': u'cdn-1ly-co-06601832710.kdatacdn.net', u'id': 7}
            '''
            domain = item['domain']
            kdata_domain = item['kdata_domain']
            origin_server = item['origin_server']
            kdata_id = item['id']

            # domain existed in script db?
            check_domain = self._db_domain_fetch_one_by_kdata_id(kdata_id)
            if check_domain:
                self._log('domain {} existed with data {}'.format(domain, check_domain))
                continue

            # force check is valid domain
            if self.must_check_valid_domain and self.is_valid_domain(domain) == False:
                self._log('domain {} is invalid'.format(item['domain']))
                self.update_domain(item['id'], 1, 'domain.err_domain')
                continue

            # force check is valid origin
            if self.must_check_valid_origin and self.is_valid_origin(origin_server) == False:
                self._log('origin {} is invalid'.format(origin_server))
                self.update_domain(item['id'], 1, 'domain.err_origin_server')
                continue

            origin_server = self.get_cdn_origin(origin_server, domain)
            if origin_server is None:
                self._log('origin {} is invalid'.format(origin_server))
                self.update_domain(item['id'], 1, 'domain.err_origin_server')
                continue

            replaces = {
                '$domain': kdata_domain,
                '$origin_ip:port': origin_server,
            }

            # cdn node vhost data
            per_domain_vhost_file = '{}.yml'.format(kdata_domain)
            per_domain_template_data = template_data
            for find, repl in replaces.items():
                per_domain_template_data = per_domain_template_data.replace(find, repl)

            ''' create yml file'''
            with open(per_domain_vhost_file, 'w') as f:
                f.write(per_domain_template_data)

            ''' update db'''
            script_data = {
                'user_domain': domain
                ,'kdata_domain': kdata_domain
                ,'domain_id': str(kdata_id)
                ,'status': 'wait_call_cdn_node'
                ,'origin': item['origin_server']
                ,'comment': 'inserted from script at {}'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
            }
            self._db_domain_add(script_data)

            cfg = {
                'domain': kdata_domain
                ,'zone_type': 'A'
                ,'ip': ['123.30.171.238', '127.0.0.1']
                ,'proxy': False
            }

            self.kcf.add_config(cfg)
            res = self.kcf.add_record()
            if not res['status']:
                self.push_noti('[ERROR] Domain {} is existed --- {}'.format(kdata_domain, res))
            else:
                self.push_noti('[OK] Domain {} added'.format(kdata_domain))

            #push_ansible here
            kansible = Kansible({'playbook_path': '/path/to/playbook.yml'})
            kansible.test()


    def check_cdn_vhost(self):
        '''
        check domain in script db is valid vhost?
        '''

        # fetch all script domains
        rows = self._db_domain_fetch_all()
        if rows is None:
            return self._res_bool(False)

        for row in rows:
            if row['status'] == 'all_active':
                #self._log('domain {} is activated'.format(row['kdata_domain']))
                continue

            elif row['status'] == 'active':
                cname_valid = self.is_valid_cname(row['user_domain'], row['kdata_domain'])
                if cname_valid:
                    'update to script db'
                    self._db_domain_update(int(row['id']), {'status': 'all_active'})
                    self._log('domain {} is cname to {}'.format(row['user_domain'], row['kdata_domain']))
                    self.push_noti('domain {} is cname to {}, domain is fully activated'
                                    .format(row['user_domain'], row['kdata_domain']))
            else:
                # is valid cdn node?
                if self.is_valid_origin(row['origin']):
                    self._log('valid {}'.format(row['kdata_domain']))

                    ' update script db '
                    self._db_domain_update(int(row['id']), {'status': 'active'})

                    ' update kdata cdn db '
                    self.update_domain_kdata_cdn(row['domain_id'], 2, 'cdn node created')

                    self.push_noti('domain {} is activated'.format(row['kdata_domain']))
                else:
                    self._log('invalid origin for domain {}'.format(row['kdata_domain']))


    def is_valid_domain(self, domain):
        '''
        check domain is valid
        '''
        ping = subprocess.Popen('ping {} -c 3'.format(domain), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True);
        ping_err = ping.communicate()[1]
        if len(ping_err) > 0 and ping_err.index('unknown host') != -1:
            return False;
        return True;


    def is_valid_origin(self, origin):
        try:
            test = requests.get(origin, timeout=5, verify=False)
            if test is not None and int(test.status_code) in [200, 403, 404, 301, 302]:
                return True
            return False
        except:
            return False


    def is_valid_cname(self, domain, cname_to):
        pcall = subprocess.Popen(['dig', 'cname', domain]
                                ,stdout=subprocess.PIPE
                                ,stdin=subprocess.PIPE
                                ,stderr=subprocess.STDOUT
                                )
        success, failed = pcall.communicate()

        if success.find(cname_to) != -1:
            return True
        else:
            return False


if __name__ == '__main__':
    kdata = Kdata()

    parser = optparse.OptionParser()
    parser.add_option('-a', '--action', action='store', dest='action',
            help="-a --action running type\
            \t\tpending_domain: process pending domains from Kdata CDN\
            pending_cache: process remove cache uri from Kdata CDN\
            check_cdn_vhost: check vhost in CDN node\n")

    options, args = parser.parse_args()

    if options.action == 'pending_domain':
        kdata.process_pending_domains()
    elif options.action == 'pending_cache':
        kdata.remove_cache_uri()
    elif options.action == 'check_cdn_vhost':
        kdata.check_cdn_vhost()
    else:
        kansible = Kansible({'playbook_path': '/usr/local/sbin/ansible-role-diepdj/roles/ansible-role-nginx/plays/active-site/khanh-dantri-com-69690751484.kdatacdn.net.yml'})
        kansible.test()
