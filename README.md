# rpm_check
Module for Ansible to check if `rpm` package installed on your system.

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
