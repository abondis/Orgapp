#!/usr/bin/env python
# from bottle-cork examples
# https://github.com/FedericoCeratto/bottle-cork/tree/master/examples
# needs pycrypto
from datetime import datetime
from cork import Cork


def create_test_users():
    """Run from the 'src' folder"""
    cork = Cork('config', initialize=True)

    cork._store.roles['admin'] = 100
    cork._store.roles['edit'] = 50
    cork._store.save_roles()

    tstamp = str(datetime.utcnow())
    username = 'admin'
    password = 'test'
    cork._store.users[username] = {
        'role': 'admin',
        'hash': cork._hash(username, password),
        'email_addr': username + '@localhost.local',
        'desc': username + ' test user',
        'creation_date': tstamp
    }
    cork._store.save_users()

if __name__ == '__main__':
    create_test_users()
