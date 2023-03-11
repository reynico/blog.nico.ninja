---
layout: post
title: "My home server"
date: 2022-12-28 09:34:00 -0300
categories: [internet, linux]
description: Why do I have a home server and why you should as well
---

![server](/assets/images/home-server-1/server-header.jpg)

Since I was a kid and learned about computers I developed a sense of necessity for a home server. A home server is a great piece of hardware to learn about computers, services, and high availability, while as well enjoying the build journey on both hardware and software.

- [Storytime!](#storytime)
- [Current setup](#current-setup)
  - [Hardware](#hardware)
  - [Operating system](#operating-system)
  - [What do I run on top of Proxmox?](#what-do-i-run-on-top-of-proxmox)
  - [Future plans](#future-plans)
- [Conclusion](#conclusion)

---

# Storytime!

In 2007, I was able to build my first home server, at my parent's house. A tough Intel Celeron running at 400MHz, 256 Megabytes of RAM, and an 8GB hard drive, of course running Debian on its Etch release. Most of the hardware came from the trash.

![my first server](/assets/images/home-server-1/first-server.jpg)

Back in time, it was in charge of the print server for the family, feeding two printers: A Citizen GSX-190s and an Epson Stylus Color 400. Pain in the ass to configure. It also served as an [Echolink](https://www.echolink.org/) node for the city where my parents live, and some domotics projects I hosted there, controlling parallel port bits from a PHP web panel. Last but not least, it also served as a phpBB forum a friend and I maintained for some years.

# Current setup

Time passed since my first server (and I owed several!), I'll dive into the hardware and software configuration I used to setup it up and what does it every day.

## Hardware

Requirements were the following:

- Zero to minimal noise from fans and/or disks, power supplies, or whatever makes noise.
- Small form factor, mini ITX is a good example.
- Low energy consumption.
- Modern hardware, no rubbish stuff.
- Enough disk space for movies, tv shows, music, and my backups.

**The main server**

One of my friends told me that they use Asus PN50 mini PCs in their offices, the PN50 offers AMD Ryzen processors, up to 64GB DDR4 memory, and has an m2 and a SATA slot for storage. Since [the newest PN51 replaced the PN50](https://www.asus.com/displays-desktops/mini-pcs/pn-series/mini-pc-pn51/), I've ordered one, along with an Inland 2TB NVME disk, and a 32GB DDR4 memory stick, with 1-day shipping.

![Asus PN51](/assets/images/home-server-1/pn51-box.jpg)

The PN51 has the new 5000u series from the Ryzen processors, with as low as 9 watts of power consumption at idle and very low noise levels. This is perfect as my office is next to the bedroom and I didn't want to hear any high-pitched whining noise from the power supply coils, or the CPU fan.

![Asus PN51](/assets/images/home-server-1/pn51-open.jpg)

**The storage**

While these components covered most of the requirements, I was still missing the disk space stuff, 2TB may be sufficient but not enough if I wanted to bring virtual machines, containers, and clusters along with my files and media, so I got a bit old [Netgear ReadyNAS 312](https://www.netgear.com/support/product/RN312.aspx) network attached storage, and feed it with two [Western Digital Red NAS WD40EFAX](https://www.westerndigital.com/products/internal-drives/wd-red-sata-hdd#WD40EFAX) drives, in RAID 1.

I thought twice about it since the #1 requirement is zero noise. Later on, I realized that my apartment is fully CAT 6 wired, so I just left the NAS box in the living room behind the main TV. The first start-up of the NAS was OMG WHAT THE F. IS ALL THAT NOISE, then it just got very quiet and the chassis fan rarely spins, also disks are pretty silent by themselves.

**Networking**

Thought about this one several times, but I ended up getting it K.I.S.S.: as rare as it may sound, my cable modem router, a [Cisco DPC3848](https://www.cisco.com/c/en/us/obsolete/video/cisco-dpc3848-wireless-residential-gateway.html) works great. Great Wi-Fi speed (at least for my 300Mbps connection), and great software stability, even the ISP left it almost unmanaged so you can port-forward everything you want, so adding additional networking gear will just complicate things. In terms of wired connectivity, I'm using 3 out of the 4 ethernet ports, one for the Proxmox box, one for the NAS, and one for the Philips Hue Bridge.

## Operating system

Since I wanted to virtualize everything I could, I choose [Proxmox VE 7.x](https://www.proxmox.com/en/proxmox-ve). Proxmox is a complete server management platform, that integrates the KVM hypervisor and Linux containers (LXC), software-defined networking and storage, and a web interface to ease management.

It really helps to keep things tidy and connected: the software-defined storage permits local storage and remote storage in several different flavors, and connecting the NAS via NFS was really simple!

## What do I run on top of Proxmox?

[**Pi-Hole (LXC container)**](https://pi-hole.net/)

My main DNS server with local domain resolution. I'm using a `.home` TLD to map the internal devices on my network as well as containers and VMs on Proxmox. It's also great to blacklist specific domains you don't want to solve and has some good monitoring and tracing tools to check when something's going wrong.

![PI Hole](/assets/images/home-server-1/pihole.jpg)

[**Wireguard - Internet (LXC Container)**](https://www.wireguard.com/)

The main VPN server. Behind the scenes, it's a Pivpn installation. Pivpn eases the setup of a Wireguard or OpenVPN VPN server, with user management. Really great tool to manage a VPN server.

This is the VPN I use when I want to have a secured Internet gateway (my apartment), and what I provide to my closest friends when they need the same. It has an iptables rule to drop traffic to the internal subnet so it just works for solely the Internet.

```bash
-A FORWARD -d 192.168.1.0/24 -i wg0 -j DROP
```

Performance overall is so great that you wouldn't notice either if you're tunneled or not.

[**Wireguard - Local (LXC Container)**](https://www.wireguard.com/)

The internal VPN server. As well as the Internet Wireguard is a container running Pivpn, but runs with no restrictions on networking so this is the VPN I use to manage my cluster and files when I'm out of the home.

[**Transmission (LXC Container)**](https://transmissionbt.com/)

Transmission is by far my favorite torrent software. It's super lightweight, easy to configure, and also has a web interface to control it. I've been using it for at least 10 years and it's still my fav one.

Since my multimedia files belong to the NAS, I have a shared folder with specific permissions to read/write. Mounting the NAS NFS file share is a bit tricky and I had to use the Linux console from the Proxmox server, where `103` is the container ID for Transmission.

```c
pct set 103 -mp0 /mnt/nas/Media,mp=/mnt/nas/Media
```

[**Plex (LXC Container)**](https://www.plex.tv/)

The main media server for movies, TV Shows, and Music. Both of my TVs support Plex so watching my favorite movies is quite easy. Back in time, I had been using XBMC and then Kodi. Plex does the on-the-fly transcoding so I fed it with enough resources to run, one of the beauties things about Proxmox is that you can adjust each container's resources in real-time!

As well on Transmission, I had to mount the NAS NFS file share for multimedia, but this time in read-only mode (defined on the NAS).

[**Sonarr (LXC Container)**](https://sonarr.tv/)

Keeping track of TV shows, searching for Torrents, downloading, and then updating the Plex library is a lot of work. Sonarr is in charge of it, even for already running TV shows it constantly looks (with RSS) for new episodes to download. Sonarr has read-write access to the multimedia share of the NAS.

[**Radarr (LXC Container)**](https://radarr.video/)

Radarr is a fork of Sonarr, but for movies.

[**Bazarr (LXC Container)**](https://www.bazarr.media/)

Sometimes, I prefer to watch movies and TV shows with subtitles. Bazarr looks for subtitles by connecting to both Sonarr and Radarr and looking for them on different subtitle trackers. It also updates the Plex library to make it aware of them.

**Monitoring (LXC Container)**

This is the monitoring stack built with Grafana and Prometheus. I capture information from several devices and show them in a single place (Grafana). I'm also using Grafana alerts with Telegram so I notice when something goes wrong. I have three principal dashboards:

- **Proxmox:** Proxmox hardware and software health checks, how many containers, how many VMs, what's the disk usage (local and remote), what's the CPU and memory usage, what's going on with the network, and so on.
- **Internet:** I constantly monitor the cable modem stats (TX, RX, and MER power) so I could debug an Internet issue on the TAP before calling tech support (which sucks). I also monitor ping and round-trip time connections to different servers around the globe.
- **Home:** This is the IOT dashboard, I have some ESP32/ESP8266 devices spread around the house like temperature, humidity, and CO2 concentration.

![Monitoring dashboard](/assets/images/home-server-1/grafana.jpg)

**Time machine (LXC Container)**

This container holds the encrypted backups of my Apple devices, it's just a Linux box with avahi-daemon and [Netatalk](https://netatalk.sourceforge.io/) configured to act as a time machine for Apple. I had to mount an NFS share from the NAS to the container to hold my backups and configure [Netatalk](https://netatalk.sourceforge.io/) as follows:

```bash
[Time Machine]
path = /mnt/timemachine
time machine = yes
```

That's everything you need from the server side to set up a time machine. On a Mac you need to go to System Preferences > Time Machine > Select Backup Disk. and your network time machine would appear in the list.

**Backups (LXC Container)**

The backups container differs a bit from the time machine one. The time machine container stores solely snapshots of my Macbook, while backups (this one) collect photos, videos, documents, and other sensible stuff as well as a local copy of my Google Drive. I've found a great headless tool to manage it, called [Rclone](https://rclone.org/). With a little scripting, I run Rclone and [ClamAV](https://www.clamav.net/) on new synced files as well as a scheduled weekly [ClamAV](https://www.clamav.net/) run for all my files, just to keep sure nothing is infected. A Python script would notify me through Telegram if an infected file is found.

[**Nginx Proxy Manager (LXC Container)**](https://nginxproxymanager.com/)

Since I'm getting too old to remember weird port numbers and IP addresses, I've set up an Nginx frontend with Nginx Proxy Manager to centralize everything under a well-known domain name, with Let's Encrypt SSL termination, so I just need to assign a subdomain to each of my containers and VMs. Nginx Proxy Manager handles:

- Frontend to manage domains.
- SSL wildcard termination with Let's Encrypt.
- Subdomains for each service I need to redirect.
- Access lists.
- Access logs.
- Custom 404 pages.

**Windows 10 (VM)**

I'm not a Windows user but from time to time I need to run some Windows executables and I'm tired of dealing with Wine and that kind of emulation software, so I set up a Windows virtual machine that I start on demand. To ease the access to the VNC console from Proxmox I run a hook script on this virtual machine to enable it:

```bash
#!/usr/bin/expect

set vmid [lindex $argv 0]

spawn qm monitor $vmid
expect {"qm>"}
send "set_password vnc vncpass1 -d vnc2\r"
expect {"qm>"}
send "exit\r"
```

and then attach the hook script to the machine ID:

```c
qm set 113 --hookscript local:snippets/vnc.sh
```

**Ubuntu 12.04 (VM)**

I'm a big fan of open source and car racing. One of the projects I belove is [Megasquirt](https://megasquirt.info/): An open-source hardware/software solution for EFI management on fuel injection engines. Down here the most successful product from Megasquirt is the [Megasquirt 2](http://www.megamanual.com/MSFAQ.htm): cheap, full of options, and super customizable. During the past weeks, I've been working on a [wheel decoder to decode the Honda K20, K24, R18, R20, and some L15 engine trigger wheels with the Megasquirt 2](https://blog.nico.ninja/diy/electronics/cars/writing-a-wheel-decoder-megasquirt/). Sadly, most of the firmware development kit kept really old (As the MS2 brain is [a 1980's microprocessor](https://physics.mcmaster.ca/tech/HC908/HC908Intro.htm)) so I had to run an old Linux OS to compile the source code.

[**GNS3 server**](https://www.gns3.com/)

This is for my networking learning and tests, a small lab where I run the great GNS3 server, and then I could access it from my laptop or any virtual machine. GNS3 is quite power-consuming when setting up several routers to emulate so it's better to keep it on a separate machine/server.

## Future plans

While this is a completely functional home server, I still want to improve some little things.

**Networking**

I would like to set up separate VLANs for the different devices I have on my network, and then set up Proxmox to catch up with the trunk 802.11q and set up different VMs and containers to connect to each VLAN.

I would also like to set up some sort of firewall in front of my internet connection, which means adding some networking gear to keep the cable modem router as a simple modem and then manage NAT, firewall, and Wi-Fi from a different hardware device.

**Automation**

This setup has little to no automation, would be great to integrate automation tools like [Ansible](https://www.ansible.com/)!

In between the containers and VMs I haven't set up a home assistant server yet, that would be great to have to integrate with the Philips Hue system and the HomePod.

**Home Lab**

The unique piece of laboratory I'm running right now must be the [GNS3 server](https://www.gns3.com/). I'd love to set up some more goodies for the home lab such as a Kubernetes cluster.

# Conclusion

It's great what you can do with little hardware! Well managed, a home server converts into a swiss army knife for daily use. Bringing up a Linux virtual machine is just a matter of minutes, as well as destroying it. Proxmox handles great on networking and storage as well as resources management, I've never encountered a problem yet with the performance or management of the cluster.

I'm still missing using some Proxmox features such as the integrated firewall, or the replication system but it would be just a matter of time.
