# rpm_check
[![Platform](http://img.shields.io/badge/platform-redhat-cc0000.svg?style=flat)](#)
[![Platform](http://img.shields.io/badge/platform-centos-932279.svg?style=flat)](#)

Module for [Ansible](http://www.ansible.com) to check if `rpm` package installed on your system.

### Installation
To use the `rpm_check` module just copy the file into `./library`, alongside your top level playbooks, or copy it into the path specified by `ANSIBLE_LIBRARY` or the `--module-path` command line option.

### Examples

```yml
# Check if Apache installed
- rpm_check:
    name: httpd
    state: installed
    
# Check multiple rpm packages installed on your system
- rpm_check:
    name: nginx,httpd
```
