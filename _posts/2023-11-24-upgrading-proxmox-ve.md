---
layout: post
title: "Upgrading Proxmox VE 7.x"
date: 2023-11-24 11:00:00 -0300
tags: [Computers, Internet]
description: My notes during the upgrade of my Proxmox VE server
---

![Debian upgrade procedure](/assets/images/upgrading-proxmox-7-8/header.jpg)

For quite some time, [my Proxmox VE server](https://blog.nico.ninja/my-home-server/) has been running on version 7.1-10. Due to a busy year, I hadn't found the time to perform the necessary upgrades until now. In this post, I'll walk you through the steps I took to upgrade it to the latest 7.x release and then to version 8.x.

# Upgrading to the Latest Proxmox VE 7.x Release

## Configuring the repositories
Initially, I was advised to add a new line to `/etc/apt/sources.list`, but I found that this repository was already included at `/etc/apt/sources.list.d/pve-no-subscription.list`.

```
deb http://download.proxmox.com/debian/pve bullseye pve-no-subscription
```

## Update and Dist-Upgrade
Executing the following commands updated the Debian local repository and performed a dist-upgrade:

```
apt update && apt dist-upgrade
```

## Stopping Virtual Machines and Containers
Before proceeding, I bulk-stopped both virtual machines and containers. I noticed that Proxmox rebooted faster if stopped prior to the upgrade. This was achieved through the Proxmox web UI. You just need to Right-click over your server in the Proxmox web UI and click on Bulk Stop.

![Bulk stop](/assets/images/upgrading-proxmox-7-8/bulk-stop.jpg)

## Rebooting the Proxmox Server
A simple `reboot` brought the server back online.

## Checking Everything Is Working
Post-reboot, logging into the Proxmox UI confirmed the successful update to version 7.4-17.


# Actual Upgrade to Proxmox VE 8.x
The upgrade process to version 8.x is straightforward. Proxmox provides an automated checker tool, `pve7to8`, which checks hardware and software configurations before initiating the upgrade.
```
= CHECKING VERSION INFORMATION FOR PVE PACKAGES =

Checking for package updates..
PASS: all packages up-to-date

Checking proxmox-ve package version..
PASS: proxmox-ve package has version >= 7.4-1

Checking running kernel version..
PASS: running kernel '5.15.131-1-pve' is considered suitable for upgrade.

= CHECKING CLUSTER HEALTH/SETTINGS =

SKIP: standalone node.

= CHECKING HYPER-CONVERGED CEPH STATUS =

SKIP: no hyper-converged ceph setup detected!

= CHECKING CONFIGURED STORAGES =

PASS: storage 'local' enabled and active.
PASS: storage 'local-lvm' enabled and active.
PASS: storage 'nas-backup' enabled and active.
PASS: storage 'nas-media' enabled and active.
PASS: storage 'nas-time-machine' enabled and active.
INFO: Checking storage content type configuration..
PASS: no storage content problems found
PASS: no storage re-uses a directory for multiple content types.

= MISCELLANEOUS CHECKS =

INFO: Checking common daemon services..
PASS: systemd unit 'pveproxy.service' is in state 'active'
PASS: systemd unit 'pvedaemon.service' is in state 'active'
PASS: systemd unit 'pvescheduler.service' is in state 'active'
PASS: systemd unit 'pvestatd.service' is in state 'active'
INFO: Checking for supported & active NTP service..
PASS: Detected active time synchronisation unit 'chrony.service'
INFO: Checking for running guests..
WARN: 15 running guest(s) detected - consider migrating or stopping them.
INFO: Checking if the local node's hostname 'nuc01' is resolvable..
INFO: Checking if resolved IP is configured on local node..
PASS: Resolved node IP '192.168.1.2' configured and active on single interface.
INFO: Check node certificate's RSA key size
PASS: Certificate 'pve-root-ca.pem' passed Debian Busters (and newer) security level for TLS connections (4096 >= 2048)
PASS: Certificate 'pve-ssl.pem' passed Debian Busters (and newer) security level for TLS connections (2048 >= 2048)
PASS: Certificate 'pveproxy-ssl.pem' passed Debian Busters (and newer) security level for TLS connections (4096 >= 2048)
INFO: Checking backup retention settings..
PASS: no backup retention problems found.
INFO: checking CIFS credential location..
PASS: no CIFS credentials at outdated location found.
INFO: Checking permission system changes..
INFO: Checking custom role IDs for clashes with new 'PVE' namespace..
PASS: no custom roles defined, so no clash with 'PVE' role ID namespace enforced in Proxmox VE 8
INFO: Checking if LXCFS is running with FUSE3 library, if already upgraded..
SKIP: not yet upgraded, no need to check the FUSE library version LXCFS uses
INFO: Checking node and guest description/note length..
PASS: All node config descriptions fit in the new limit of 64 KiB
PASS: All guest config descriptions fit in the new limit of 8 KiB
INFO: Checking container configs for deprecated lxc.cgroup entries
PASS: No legacy 'lxc.cgroup' keys found.
INFO: Checking if the suite for the Debian security repository is correct..
PASS: found no suite mismatch
INFO: Checking for existence of NVIDIA vGPU Manager..
PASS: No NVIDIA vGPU Service found.
INFO: Checking bootloader configuration...
SKIP: not yet upgraded, no need to check the presence of systemd-boot
INFO: Check for dkms modules...
SKIP: could not get dkms status
SKIP: NOTE: Expensive checks, like CT cgroupv2 compat, not performed without '--full' parameter

= SUMMARY =

TOTAL:    34
PASSED:   27
SKIPPED:  6
WARNINGS: 1
FAILURES: 0

ATTENTION: Please check the output for detailed information!
root@nuc01:~#
```

## Update Base Repositories
To transition from Debian Bullseye to Bookworm, a simple sed replace in the APT sources list files followed by a repository update:
```
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list
sed -i 's/bullseye/bookworm/g' /etc/apt/sources.list.d/pve-no-subscription.list
apt update
```

## Stopping Virtual Machines and Containers (Again)
Similar to the earlier step, a bulk stop of all machines was performed.

## Upgrading the software

The software upgrade process is quite similar to the minor Proxmox VE 7.x upgrades:
```
apt dist-upgrade
```

## Changes in configuration files
Certain system-wide files may change during upgrades. Here's a list of files and my corresponding actions:

* `/etc/issue`
Keep your current version installed (answer No).

* `/etc/lvm/lvm.conf`
Install the package maintainer's version (answer Yes).

* `/etc/ssh/sshd_config`
Depending on modifications, answer No (Keep the current version installed).


## Checking the Upgrade Results Before Rebooting
Using pve7to8 again revealed three warnings. One of note was related to UEFI mode, prompting the installation of grub-efi-amd64:
```
WARN: unexpected running and installed kernel '5.15.131-1-pve'.
WARN: systems seems to be upgraded but LXCFS is still running with FUSE 2 library, not yet rebooted?
WARN: System booted in uefi mode but grub-efi-amd64 meta-package not installed, new grub versions will not be installed to /boot/efi! Install grub-efi-amd64.
```

I don't care much about the first and second warnings, as I haven't rebooted the server yet, but I'm curious about the third one. As I actually run EFI on my hardware I'll install the missing package. You can check if you're running EFI by doing a simple
```
ls /sys/firmware/efi
```

If the folder exists and it's not empty, you better install `grub-efi-amd64`
```
apt install grub-efi-amd64
```

## Rebooting the Server
A simple reboot brought the server back to life. For those anxious moments, I monitored the return with a `ping <server_ip>`.
```
% ping 192.168.1.2
PING 192.168.1.2 (192.168.1.2): 56 data bytes
64 bytes from 192.168.1.2: icmp_seq=0 ttl=64 time=22.053 ms
64 bytes from 192.168.1.2: icmp_seq=1 ttl=64 time=6.918 ms
64 bytes from 192.168.1.2: icmp_seq=2 ttl=64 time=6.679 ms
64 bytes from 192.168.1.2: icmp_seq=3 ttl=64 time=8.053 ms
64 bytes from 192.168.1.2: icmp_seq=4 ttl=64 time=7.346 ms
64 bytes from 192.168.1.2: icmp_seq=5 ttl=64 time=4.956 ms
64 bytes from 192.168.1.2: icmp_seq=6 ttl=64 time=5.176 ms
64 bytes from 192.168.1.2: icmp_seq=7 ttl=64 time=5.025 ms
64 bytes from 192.168.1.2: icmp_seq=8 ttl=64 time=5.262 ms
Request timeout for icmp_seq 9
Request timeout for icmp_seq 10
Request timeout for icmp_seq 11
Request timeout for icmp_seq 12
...
Request timeout for icmp_seq 31
Request timeout for icmp_seq 32
Request timeout for icmp_seq 33
Request timeout for icmp_seq 34
64 bytes from 192.168.1.2: icmp_seq=35 ttl=64 time=16.307 ms
64 bytes from 192.168.1.2: icmp_seq=36 ttl=64 time=4.172 ms
64 bytes from 192.168.1.2: icmp_seq=37 ttl=64 time=5.124 ms
64 bytes from 192.168.1.2: icmp_seq=38 ttl=64 time=3.630 ms
```

## Checking That Everything Is Working
Post-reboot, logging into the Proxmox VE web GUI confirmed the successful upgrade to version 8.x.

![Bulk stop](/assets/images/upgrading-proxmox-7-8/proxmox-ve-8-gui.jpg)


Plex, which runs on my Proxmox server, operated as expected, signaling a complete and successful upgrade. (AKA if Plex works, everything works)

![Bulk stop](/assets/images/upgrading-proxmox-7-8/hackers-1995.jpg)


### Monitoring
Post-upgrade, my Proxmox VE server was monitored using [prometheus-pve-exporter](https://github.com/prometheus-pve/prometheus-pve-exporter). However, it refused to function, warranting further investigation.
```
Nov 24 22:23:16 nuc01 systemd[1]: Started prometheus-pve-exporter.service - Prometheus exporter for Proxmox VE.
Nov 24 22:23:16 nuc01 pve_exporter[1096]: Traceback (most recent call last):
Nov 24 22:23:16 nuc01 pve_exporter[1096]:   File "/usr/local/bin/pve_exporter", line 5, in <module>
Nov 24 22:23:16 nuc01 pve_exporter[1096]:     from pve_exporter.cli import main
Nov 24 22:23:16 nuc01 pve_exporter[1096]: ModuleNotFoundError: No module named 'pve_exporter'
Nov 24 22:23:16 nuc01 systemd[1]: prometheus-pve-exporter.service: Main process exited, code=exited, status=1/FAILURE
Nov 24 22:23:16 nuc01 systemd[1]: prometheus-pve-exporter.service: Failed with result 'exit-code'.
Nov 24 22:23:16 nuc01 systemd[1]: prometheus-pve-exporter.service: Scheduled restart job, restart counter is at 5.
Nov 24 22:23:16 nuc01 systemd[1]: Stopped prometheus-pve-exporter.service - Prometheus exporter for Proxmox VE.
Nov 24 22:23:16 nuc01 systemd[1]: prometheus-pve-exporter.service: Start request repeated too quickly.
Nov 24 22:23:16 nuc01 systemd[1]: prometheus-pve-exporter.service: Failed with result 'exit-code'.
Nov 24 22:23:16 nuc01 systemd[1]: Failed to start prometheus-pve-exporter.service - Prometheus exporter for Proxmox VE.
```

Reinstalling the exporter did the trick:
```
python3 -m pip install prometheus-pve-exporter
pve_exporter --help
```

![Grafana dashboard](/assets/images/upgrading-proxmox-7-8/monitoring.jpg)
