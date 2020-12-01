# Change Log

<!--
## DATE, vx.x.x

### Notable changes

### Breaking changes

### Contributors

---
-->

## 2020-11-30, v2.0.2

### Notable changes

  - Updated issue template and information collection tasks.

---

## 2020-11-30, v2.0.1

### Notable changes

  - Fixed a number of typos in the README.md
  - Updated the meta/main.yml to put quotes around minimum Ansible version.

---

## 2020-11-29, v2.0.0

### Notable changes

  - #64 - Initial release of v2.0.0 of
    [ansible-role-k3s](https://github.com/PyratLabs/ansible-role-k3s).
  - Minimum supported k3s version now: v1.19.1+k3s1
  - Minimum supported Ansible version now: v2.10.0
  - #62 - Remove all references to the word "master".
  - #53 - Move to file-based configuration.
  - Refactored to avoid duplication in code and make contribution easier.
  - Validation checks moved to using variables defined in `vars/`

### Breaking changes

#### File based configuration

Issue #53

With the release of v1.19.1+k3s1, this role has moved to file-based
configuration of k3s. This requires manuall translation of v1 configuration
variables into configuration file format.

Please see: https://rancher.com/docs/k3s/latest/en/installation/install-options/#configuration-file

#### Minimum supported k3s version

As this role now relies on file-based configuration, the v2.x release of this
role will only support v1.19+ of k3s. If you are not in a position to update
k3s you will need to continue using the v1.x release of this role, which will
be supported until March 2021<!-- 1 year after k8s v1.18 release -->.

#### Minimum supported ansible version

This role now only supports Ansible v2.10+, this is because it has moved on to
using FQDNs, with the exception of `set_fact` tasks which have
[been broken](https://github.com/ansible/ansible/issues/72319) and the fixes
have [not yet been backported to v2.10](https://github.com/ansible/ansible/pull/71824).

The use of FQDNs allows for custom modules to be introduced to override task
behavior. If this role requires a custom ansible module to be introduced then
this can be added as a dependency and targeted specifically by using the
correct FQDN.
