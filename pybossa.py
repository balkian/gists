# coding: utf-8

import requests
import sys

HOST = 'http://localhost'


def get_count_all(user_name, host=HOST):
    user = get_user(user_name, host)
    user_id = user['id']

    page = 0
    total = 0

    while True:
        r = requests.get(host+'/api/taskrun',
                        params={'user_id': 2,
                                'limit': 100,
                                'offset': total},
                        headers={'content-type': 'application/json'})
        if r.status_code != 200:
            raise Exception('Error in call')
        delta = len(r.json())
        if not delta:
            break
        total += delta
    return total


def get_user_name(user_id, host=HOST):
    r = requests.get('{}/api/user/{}'.format(host, user_id),
                    headers={'content-type': 'application/json'})
    if r.status_code != 200:
        raise Exception(r)
    return r.json()['name']


def get_user(user_name, host=HOST):
    r = requests.get('{}/account/{}/'.format(host, user_name),
                    headers={'content-type': 'application/json'})
    if r.status_code != 200:
        raise Exception(r)
    return r.json()['user']

def get_all_users(host=HOST):
    r = requests.get('{}/account/'.format(host),
                    headers={'content-type': 'application/json'})
    if r.status_code != 200:
        raise Exception(r)
    return [u['name'] for u in r.json()['accounts']]

def get_count(user_name, host=HOST):
    user = get_user(user_name)
    return user['n_answers']


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Get the number of responses.')
    parser.add_argument('--host', type=str,
                        default=HOST, help='Pybossa hostname')
    parser.add_argument('user_name', type=str, nargs='?',
                        help='User name')

    args = parser.parse_args()
    if args.user_name:
        print(get_count(args.user_name, host=args.host))
    else:
        for user in get_all_users(args.host):
            print(user, get_count(user, args.host))