---
layout: post
title: "The perfect fit for my 2011 Macbook Air"
date: 2024-01-09 19:30:00 -0300
tags: [Computers, Internet]
description: Experience the revival of an old favorite but with Xubuntu 23.10
---

There is it, lying in a drawer. My first Macbook. This is one of those things I felt in love at first sight. In my opinion, this was Apple's peak design for portable computers, thin, small, lightweight, with outstanding hardware capabilities and performance, and, one of the things I like most, a beautiful screen resolution.

![MacBook Air sitting next to a plant](/assets/images/macbook-air-ubuntu-1/header.jpg)

---

- [The Macbook Air](#the-macbook-air)
- [The Operating System](#the-operating-system)
- [Why would I install Linux on it?](#why-would-i-install-linux-on-it)
- [Installing Xubuntu 23.10](#installing-xubuntu-2310)
- [Configuring Xubuntu 23.10](#configuring-xubuntu-2310)
- [Battery health and performance](#battery-health-and-performance)
- [Thoughts](#thoughts)


# The Macbook Air

This is a [Mid-2011, 13-inch Macbook Air](https://support.apple.com/kb/sp683?locale=en_US), has a 1440x900 pixels display with maxed out the internals, it shows a dual-core 1.8GHz [i7-2677M](https://www.intel.com/content/www/us/en/products/sku/54617/intel-core-i72677m-processor-4m-cache-up-to-2-90-ghz/specifications.html), a 256GB solid-state drive and 4GB of RAM. The Wi-Fi supports the 5GHz band and the battery *should* last like 7 hours of web browsing. I never got such uptime on the battery, to be honest.

![Travelling](/assets/images/macbook-air-ubuntu-1/travelling.jpg)
> 8 years ago, traveling by train to Bruges.


# The Operating System

At the time of formatting the drive, this Macbook was running macOS High Sierra, in its 10.13.6 version. The latest supported by this hardware. I used this laptop up to 2018 when I bought the last Macbook Pro by that time and felt the Macbook Air was so laggy for most of the tasks, including simple coding and web browsing.

# Why would I install Linux on it?

As part of my geeky side, I wanted to revive this computer. I'm completely in love with this MacBook Air design so I thought I could give it a chance to see how a modern Operating System would work. I choose [Xubuntu 23.10](https://xubuntu.org/news/xubuntu-23-10-released/). I like the xfce4 design, portability, and performance, and I prefer it over Gnome or KDE, despite I've used KDE for around 5 or 6 years. As this machine is not precisely an extent of performance, I preferred to save some bits and CPU cycles here and there with a lightweight window manager. Surely I could choose something even lighter, but I'm comfortable with the trade-offs of using Xfce and an Ubuntu-based distro. If you asked me a few years ago, I would install Arch Linux.

# Installing Xubuntu 23.10

This was one of the easiest installs I ever did before.
1. Download the [Xubuntu 23.10 ISO](https://xubuntu.org/download/)
2. Use `dd` or any other tool like [balenaEtcher](https://etcher.balena.io/) to burn the ISO in an USB stick.
3. Reboot or power on your Mac while holding the alt/option key until you see the Apple logo.
4. A boot menu will appear on the screen, just pick your USB drive. Some warnings about a boot problem will be displayed.
5. I choose to encrypt the whole drive and use LVM.
6. The installation process took less than 30 minutes, and everything including the Wi-Fi worked out of the box.

![Boot menu](/assets/images/macbook-air-ubuntu-1/installer.jpg)

# Configuring Xubuntu 23.10

Despite the hardware working on the first try, I couldn't get the keyboard layout to match the MacBook's: The Command (Or Meta) key wasn't working. Diving on the Internet I found different tools and configurations but none worked. I ended up configuring the layout by hand, starting from the Macbook layout but configuring the shortcuts in the xfce4 keyboard configuration menu.

![Keyboard shortcut](/assets/images/macbook-air-ubuntu-1/keyboard_shortcuts.png)


# Battery health and performance

I choose to install [TLP](https://github.com/linrunner/TLP). TLP works out of the box heading to a battery-saver profile. Since I am not looking for strepitous performance here, I left most of the TLP settings as they come from the factory. The installation is very straightforward:

```bash
sudo add-apt-repository ppa:linrunner/tlp
sudo apt update
sudo apt install tlp tlp-rdw
```

Then you need to enable and start the systemd unit

```bash
sudo systemctl enable tlp.service
sudo systemctl start tlp.service
```

As I said earlier, I have never been able to reach the declared 7-hour of web browsing/video playing, but the battery is good enough to keep the computer working for at least 4 to 5 hours, which is a reasonable deal for me. The power statistics panel shows that while browsing, editing images with GIMP, and writing this post, the battery will last a good amount of hours. Even suspended, the laptop has low power consumption.

![Power Statistics panel](/assets/images/macbook-air-ubuntu-1/battery.png)



# Thoughts

It started just as another nerdy project with forgotten hardware. I have no specific plans for this machine, it may become my traveling computer due to its lightweightness and small form factor.

![MacBook closed lid](/assets/images/macbook-air-ubuntu-1/closed-table.jpg)


I will also do some blogging from it, as the keyboard feels great and I think I also love the screen bezels, maybe I'm just going bananas.

I always feel great when restoring or recycling old hardware, despite this Macbook having almost 15 years of life, it works great and has way better construction quality than my latter Macbook Pro 2019 and 2022.

![Blogging night](/assets/images/macbook-air-ubuntu-1/blogging_night.jpg)
