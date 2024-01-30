---
layout: post
title: "Raspberry Pi UniFi Controller Mastery"
date: 2024-01-30 17:30:00 -0300
tags: [Computers, Networking]
description: Things I wish I had known before installing the Unifi Controller in a Raspberry PI
---

The [UniFi Controller software](https://help.ui.com/hc/en-us/articles/220066768-Updating-and-Installing-Self-Hosted-UniFi-Network-Servers-Linux) offers seamless network management for users with multiple UniFi products. While setting it up on a Raspberry Pi seems like a pragmatic choice, several considerations can significantly impact your experience. The UniFi Controller software is great for managing a network if you have multiple UniFi products, such as a router/switch and a hand of UniFi UAPs.

You could either:

- Run the UniFi controller on your computer.
- Run the UniFi controller on a server.
- Run the UniFi controller in the “cloud”.

Running the Controller in the "cloud” is a no-go for me, it's not a privacy-minded decision and most of us wouldn't rest assured of the security of a cloud environment where we can barely control things.

![UniFi controller](/assets/images/raspberry-pi-unifi-1/unifi-controller.png)
> UniFi controller UI is slick


Running the Controller on my laptop sacrifices the versatility that multiple admins can manage the network, and if I go on vacation no one (nor me) could control the network.

So running a local server sounds like the best trade-off for us, since we haven't bought a server yet, I decided to run the controller on a Raspberry PI 3, *sighs in bad decisions*.

- [An old MongoDB version](#an-old-mongodb-version)
- [MongoDB version limitations](#mongodb-version-limitations)
- [MongoDB is fragile](#mongodb-is-fragile)
- [Don't try to start the mongod.service](#dont-try-to-start-the-mongodservice)
- [Disk writes are heavy](#disk-writes-are-heavy)
	- [logrotate to the rescue](#logrotate-to-the-rescue)
- [Memory pressure is heavy](#memory-pressure-is-heavy)
- [Conclusion](#conclusion)


# An old MongoDB version

The UniFi controller software uses MongoDB as the main database, sigh. It's not only unreliable, but it also requires you to run [MongoDB 4.4, from 2020.](https://www.mongodb.com/evolved#mdbfourfour) While it may not sound *that* old, it is old. And the latest Linux distributions don't include that version in their repos.

```bash
curl https://pgp.mongodb.com/server-4.4.asc | sudo gpg --dearmor | sudo tee /usr/share/keyrings/mongodb-org-server-4.4-archive-keyring.gpg >/dev/null
echo 'deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-org-server-4.4-archive-keyring.gpg] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse' | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list > /dev/null
sudo apt update
sudo apt install -y mongodb-org-server
```

# MongoDB version limitations

There's an additional limitation: MongoDB 4.4 > 4.4.23 wouldn't work on a Raspberry PI. It just crashes with an illegal instruction, and probably with a core dump.

```bash
apt install \
	mongodb-org=4.4.18 \
	mongodb-org-server=4.4.18 \
	mongodb-org-shell=4.4.18 \
	mongodb-org-mongos=4.4.18 \
	mongodb-org-tools=4.4.18
```

# MongoDB is fragile

This isn't news, but since the UniFi controller uses MongoDB as the main database, you need to take care of backups. A power outage may leave the SD Card partition broken, or at least with some errors, that can make the MongoDB data folder unrecoverable, and I bet [the UniFi recovery guide wouldn't help you.](https://help.ui.com/hc/en-us/articles/360006634094-UniFi-Repairing-Database-Issues-on-the-UniFi-Network-Application)

```bash
file:WiredTiger.wt, connection: WiredTiger.wt read error: failed to read 4096 bytes at offset 73728: WT_ERROR: non-specific WiredTiger error
```

# Don't try to start the mongod.service

The UniFi Controller has a built-in mechanism to start and stop MongoDB. If you start `mongod.service` manually, the UniFi service wouldn't start. This also applies if you enabled the unit through Systemd.

# Disk writes are heavy

The UniFi Controller writes each UniFi device status in a JSON file inside `/var/log/unifi/remote`, in a matter of minutes, and with 10 UniFi devices you could get around 100MB worth of data written to the SD.

```bash
root@controller:/var/log/unifi/remote# ls
10.115.254.227_ac8baREDACTED.log  10.115.254.231_ac8baREDACTED.log  10.115.254.237_ac8baREDACTED.log
10.115.254.228_ac8baREDACTED.log  10.115.254.232_ac8baREDACTED.log  10.115.254.254_ac8baREDACTED.log
10.115.254.229_e4388REDACTED.log  10.115.254.234_ac8baREDACTED.log  10.115.254.238_ac8baREDACTED.log
10.115.254.230_ac8baREDACTED.log  10.115.254.235_ac8baREDACTED.log  10.115.254.239_ac8baREDACTED.log
root@controller:/var/log/unifi/remote# du -sh .
240M	.
```

Naturally, each time I configure a new Raspberry PI I install [log2ram](https://github.com/azlux/log2ram) on it. log2ram creates a RAM mount point for `/var/log` so your SD Card doesn't suffer from heavy writing. The problem arises from how much memory you borrow from the RAM itself into the mount point. For devices with low RAM like these (1GB), I wouldn't pick more than 100MB for the `/var/log/` partition.

## logrotate to the rescue

I use logrotate to limit the amount of data stored by the UniFi Controller with the following configuration stored in `/etc/logrotate.d/unifi-remote`

```bash
/var/log/unifi/remote/*.log {
        rotate 0
        size 5M
        compress
        missingok
	      notifempty
      	copytruncate
      	create 0644 unifi unifi
}
```

This way each file wouldn't weigh more than 5MB and with `rotate 0` I prevent logrotate from generating `.gz` and `.0` files from rotated logs.

# Memory pressure is heavy

The UniFi controller software is a Java application and indeed uses too much memory. The Raspberry PI would hang after a few minutes of operating the UniFi console. To avoid that I tend to lower the `XmX` Java parameter on the `/lib/systemd/system/unifi.service` file. `512M` would suffice.

```bash
-    "UNIFI_JVM_OPTS=-Xmx1024M -XX:+UseParallelGC"
+    "UNIFI_JVM_OPTS=-Xmx512M -XX:+UseParallelGC" 
```


# Conclusion

Deploying the UniFi Controller on a Raspberry Pi offers cost-effective network management, but it comes with its share of challenges. The outdated MongoDB version, fragility of the database, and disk write issues demand careful consideration. Armed with these insights, you can navigate the UniFi on Raspberry Pi journey more effectively, ensuring a robust and reliable network management solution tailored to your needs.

Last but not least, a picture I took in 2012 configuring one of the first Ubiquiti products I bought for a company Internet setup. An original 1st gen UniFi UAP, with its classic green light, next to my beloved [Dell Latitude E6400](https://www.notebookcheck.net/Review-Dell-Latitude-E6400-Notebook.12875.0.html) and [Motorola Atrix](https://www.gsmarena.com/motorola_atrix-3709.php).

![UniFi Controller 2012](/assets/images/raspberry-pi-unifi-1/unifi-uap-old.jpg)
