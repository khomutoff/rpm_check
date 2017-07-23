#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Ansible module to check installed rpm packages
(c) 2016, Dmitriy Khomutov <khomutoff@gmail.com>

This file is part of Ansible

Ansible is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Ansible is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
"""

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: rpm_check
short_description: Check installed rpm packages
version_added: "1.9"
description:
  - Checks if rpm package is installed
options:
  name:
    description:
      - RPM package name. To operate on several packages this can accept a comma separated list of packages or (as of 2.0) a list of packages."
    required: true
    default: null
  state:
    description:
      - Currently supports only one state of a package (C(installed)).
    required: false
    choices: [ "installed" ]
    default: "installed"

# informational: requirements for nodes
requirements: [ rpm ]
author:
  - "Dmitriy Khomutov"
'''

EXAMPLES = '''
- name: Check if Apache installed
  rpm_check:
    name: httpd
    state: installed

- name: Check multiple rpm packages installed on your system
  rpm_check:
    name: nginx,httpd
'''

import rpm


def get_from_rpmdb(packages):
    rpmdb_ts = rpm.TransactionSet()
    existing_packages = []
    missing_packages = []
    for pkg_name in packages:
        installed_pkgs = rpmdb_ts.dbMatch('name', pkg_name)
        if not installed_pkgs:
            missing_packages.append(pkg_name)
        else:
            for pkg in installed_pkgs:
                existing_packages.append("%s-%s-%s-%s" % (pkg['name'], pkg['version'], pkg['release'], pkg['arch']))
    return existing_packages, missing_packages

def check_rpms(module, packages, state):
    result = {}
    result['results'] = []
    result['msg'] = ''
    result['changed'] = False
    result['rc'] = 0
    if state == 'installed':
        existing_pkgs, missing_pkgs = get_from_rpmdb(packages)
        if missing_pkgs:
            module.fail_json(msg="No RPMs matching '%s' found on system" % ", ".join(missing_pkgs))
        result['results'] = existing_pkgs
    return result

def main():

    module = AnsibleModule(
        argument_spec = dict(
            name=dict(type="list"),
            state=dict(default='installed', choices=['installed']),
        ),
        required_one_of = [['name','list']],
        mutually_exclusive = [['name','list']],
        supports_check_mode = True
    )

    params = module.params

    packages = [ p.strip() for p in params['name']]
    state = params['state']
    result = check_rpms(module, packages, state)

    module.exit_json(**result)

# import module snippets
from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()