---
layout: post
title: "Netgear ReadyNAS remote decryption"
date: 2024-12-22 12:30:00 -0300
tags: [Computers, Security]
description: Decrypting the ReadyNAS from anywhere
---

My [home server](https://blog.nico.ninja/my-home-server/) has a[ Netgear ReadyNAS](https://blog.nico.ninja/monitoring-netgear-readynas/) NAS where I store sensitive data. The volumes are encrypted, so if someone steals the NAS, they won't determine the disk's contents.[ ReadyOS 6.x](https://kb.netgear.com/24916/ReadyNAS-OS-Version-6-1-8) (the NAS software, based on Debian) can encrypt the volumes with an encryption key. While this is a great feature, it's a bit unflexible: You need to insert a USB device in your NAS whenever you need to decrypt your volumes. But what happens when you are not at home?

![Netgear ReadyNAS and the Raspberry PI Zero](/assets/images/netgear-remote-decryption-1/netgear-readynas-raspberry.jpg)


This happened to me at least thrice a year, and, of course, I was not at home. The situation is far from a delightful experience: The NAS is locked, you cannot access your files, and the NAS doesn't expose the NFS and Samba shares, so the Proxmox server and the containers and virtual machines with attached shares behave very weirdly.

The simplest solution? Leave the USB device with the decryption key always plugged in in the NAS. Of course, you see the flaw: one whose stoles your NAS would also have the decryption key. Encrypting your volumes now renders it useless.

A more sophisticated solution would be a virtual USB mass storage device that I could trigger whenever possible. A few days ago, I was playing with my [Pwnagotchi](https://blog.nico.ninja/pwnagotchi-improvements/), and I remembered that it uses the [Raspberry PI Zero's OTG capabilities](https://gpiozero.readthedocs.io/en/stable/pi_zero_otg.html) to spin up a network interface in the OTG USB port. I thought for a moment if I could use those same OTG features to create a software-defined USB Mass Storage device.

So the scenario could be:

* I am at the beach when an alarm comes in, informing me that a power outage rebooted my NAS. 
* Now, the shares are inaccessible, and my files are encrypted.
* I connect to the VPN, SSH into the Raspberry PI Zero, and spin up a virtual USB Mass Storage device.
* When ready, I enter the decryption key manually, and the NAS decrypts the contents.

That sounds more than doable, so I put my hands on it. During the setup, I also wondered if it would be a good idea to have a fallback for the Raspberry PI network connection, so I also wired a USB-TTL device between the Raspberry PI Zero and my server. I can access the robust serial console if the Wi-Fi network goes down or the Raspberry PI becomes flaky.

![Raspberry PI UART](/assets/images/netgear-remote-decryption-1/raspberry-uart-pinout.jpg)

With a cheap USB-TTL device you can then connect the UART pins (crossed) and share the ground connection between. GPIO14 (UART TXD) goes to the USB-TTL RX pin and the GPIO15 (UART RXD) pin goes to the USB-TTL TX. From Linux you can access the serial console with `screen`. The connection speed is 115.200 bps.

```
screen /dev/ttyUSB0 115200
```


**But how does it work?**

When you enable volume encryption in your ReadyNAS, it asks you to save the encryption key named `{your_volume_name}.key` in a USB storage device, like a flash memory or a USB stick.
If your NAS reboots, it will wait up to 10 minutes for the USB stick. From a software perspective, it is waiting for a key file in `/media/*/{your_volume_name}.key.` If no key is found during those 10 minutes, the NAS continues to boot and starts its services without any shares or access to your files. From there, you can plug in your USB stick and reboot the NAS gracefully; then, it will pick up the key in the next boot.

The Raspberry PI scripts would mimic that behavior: it creates and mounts a tiny (5MB) ramdisk image and exposes it as a gadget through the `overlay=dwc2` option. Then the [set-key.sh](https://github.com/reynico/readynas-remote-decrypt/blob/main/set-key.sh) script will write a file with your name volume and the key contents you input via STDIN.

The complete setup is available [here](https://github.com/reynico/readynas-remote-decrypt).
