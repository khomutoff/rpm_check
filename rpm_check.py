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

import rpm

EXAMPLES = '''
- name: Check if Apache installed
  rpm_check:
    name: httpd
    state: installed

- name: Check multiple rpm packages installed on your system
  rpm_check:
    name: nginx,httpd
'''

def is_installed(packages):
    rpmdb_ts = rpm.TransactionSet()
    missing_packages = []
    for p in packages:
        installed_pkgs = rpmdb_ts.dbMatch('name', p)
        if not installed_pkgs:
            missing_packages.append(p)
    return missing_packages

def check_rpms(module, packages, state):
    result = {}
    result['results'] = []
    result['msg'] = ''
    result['changed'] = False
    result['rc'] = 0
    if state == 'installed':
        missing_pkg_names_str = ", ".join(is_installed(packages))
        if missing_pkg_names_str:
            module.fail_json(msg="No RPMs matching '%s' found on system" % missing_pkg_names_str)
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