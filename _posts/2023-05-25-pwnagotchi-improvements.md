---
layout: post
title: "Pwnagotchi fixes and improvements"
date: 2023-05-25 14:00:00 -0300
categories: [linux, raspberry]
description: Upgrading the Battery and GPS for Enhanced Performance
---

![Pwnagotchi](/assets/images/pwnagotchi-fixes-1/pwnagotchi-working.jpg)

It had been a while since I last [tinkered with my Pwnagotchi](https://blog.nico.ninja/linux/raspberry/gamifying-the-pwnagotchi/), but recently, when I pulled it out of the drawer of forgotten projects, I noticed that the [PiSugar2](https://www.pisugar.com/) battery had swollen. It seemed like the lithium-ion battery, despite being stored carefully and away from heat sources, was not of the best quality. Determined to get my Pwnagotchi up and running again, I decided to replace both the battery and the GPS board.

![903052 battery](/assets/images/pwnagotchi-fixes-1/903052-battery.jpg)

The [PiSugar2](https://www.pisugar.com/) battery, a 3.7V 1200mAh lithium-ion battery, needed a replacement. After a quick search through my local storage, I stumbled upon a generic, China-made [903052](https://www.amazon.com/OCTelect-Battery-903052-1800mah-KY601S/dp/B0989Z9VK8) battery that boasted the same size and specifications. It cost me around $8, making it a cost-effective alternative. Eager to test its performance, I ran a few battery life experiments, and to my surprise, the new battery delivered similar results to the original [PiSugar2](https://www.pisugar.com/) battery. With approximately 3 hours of AI mode capturing handshakes, along with the e-paper screen and GPS unit, I was satisfied with the replacement's performance.

![Battery replaced](/assets/images/pwnagotchi-fixes-1/battery-replaced.jpg)

One of the persistent challenges I faced with the Pwnagotchi's GPS module was the time it took to acquire a lock on satellite signals and determine a position. The u-blox Neo-6 GPS unit, while reliable, was frustratingly slow in this regard. However, I had previously used the newer u-blox Neo-M8n GPS unit for a friend's GPS-based speedometer project, and it had proven to be significantly faster in both cold and warm startup scenarios. To put things into perspective, while the Neo-6 took approximately 20 minutes to achieve a cold start lock, the Neo-M8n achieved the same in less than 4 minutes. Even for warm startups, the Neo-M8n managed to lock a position in just 1 minute or less.

![Everything installed](/assets/images/pwnagotchi-fixes-1/gps-installed.jpg)

With the knowledge of the Neo-M8n's improved performance, I decided to swap out the GPS board in my Pwnagotchi. Fortunately, the pinout and signals were identical for both GPS units, simplifying the process. I carefully replaced the GPS board, ensuring a secure connection. To validate the functionality, I performed a sanity check by querying the `/dev/ttyAMA0` port, confirming that the new GPS module was operating as expected.

```bash
pi@robertgotchi:~ $ sudo cat /dev/ttyAMA0
.99,,,,,,*56
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,1*33
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,3*31
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,5*37
$GPGSV,1,1,00,0*65
$GAGSV,1,1,00,0*74
$GQGSV,1,1,,,0,00,99.99,,,,,,*56
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,1*33
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,3*31
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,5*37
$GPGSV,1,1,00,0*65
$GAGSV,1,1,00,0*74
$G$GNRMC,,V,,,,,,,,,,N,V*37
$GNVTG,,,,,,,,,N*2E
$GNGGA,,,,,,0,00,99.99,,,,,,*56
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,1*33
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.99,99.99,3*31
$GNGSA,A,1,,,,,,,,,,,,,99.99,99.9^C
```

The cost-effective battery replacement delivered comparable performance, while the improved GPS module drastically reduced the time required to acquire a position lock. These upgrades enhance the overall usability and reliability of the Pwnagotchi, allowing for extended usage and quicker access to crucial GPS data. If you're looking to optimize your Pwnagotchi experience, I highly recommend considering these upgrades.

