---
layout: post
title: "The OpenIPC Project"
date: 2024-07-30 18:30:00 -0300
tags: [Computers, DIY]
description: Opensourcing knockoff security cameras
---

Last week, my father asked if I could look at a cheap knockoff security camera, the PCBOX CIP720IPTZ. A friend of his bought it five years ago, but they never succeeded in using it, most likely due to the poor management software those cameras came with. At first glance, it is one of those white-label consumer electronics products; while it connected to the network and exposed a web server, I noticed the lack of an RTSP endpoint. *Chuckles*.

![The camera and its box](/assets/images/the-openipc-project-1/camera_box.jpg)

The camera forced me to install a browser web extension (no way); otherwise, it didn't give any video signal other than a simple JPEG preview. Then I started googling about this camera and reading this useful Github repository: https://github.com/btsimonh/826-x-ip-camera/tree/master. Here, I learned that:

- The SoC is a [GrainMedia 8135s, or 8136s](https://www.cnx-software.com/2015/06/30/grain-media-8136s-8138s-are-low-cost-hd-ip-camera-socs/), commonly used in security cameras.
- These cameras are known widely as “826-x”.
- They have a UART connection, `115200 8n1`.

![GrainMedia CPU, board, and UART connection](/assets/images/the-openipc-project-1/board_uart.jpg)

Turns out that you need to follow time-sensitive steps to get into the camera's bootloader:

1. Unplug the UART serial adapter from the camera. If RX or TX pins are pulled in some way (up/down), the camera refuses to boot.
2. Power up the camera.
3. Immediately connect the UART serial adapter.
4. Within one second or less, press ^C in the serial terminal.

![UART connections](/assets/images/the-openipc-project-1/boardfrombottom-uart.jpg)

You may need to repeat these steps a few times once you get the correct timing. An extra pair of hands can also be helpful.

During my investigation of firmware, I stopped the OpenIPC project. The project aims to build open-source firmware and software for IP Cameras. Given that my SoC was supported, I downloaded the latest firmware release (nightly build): [openipc.gm8136-nor-lite.tgz](https://github.com/OpenIPC/firmware/releases/download/latest/openipc.gm8136-nor-lite.tgz)

and started a TFTP server on my Mac, using the built-in TFTP server

```zsh
% sudo launchctl load -F /System/Library/LaunchDaemons/tftp.plist
```

The TFTP files are served by default from `/private/tftpboot`. 

From the camera's serial console and with the networking up and running, I pulled the files from my Mac with the following commands:

```zsh
setenv ipaddr 192.168.0.128; setenv serverip 192.168.0.185; saveenv
setenv bootargs 'mem=128M gmmem=90M console=ttyS0,115200 user_debug=31 root=/dev/mtdblock3 init=/init rootfstype=squashfs mtdparts=nor-flash:256k(boot),256k(env),2048k(kernel),5120k(rootfs),-(rootfs_data)'; saveenv
setenv bootcmd 'sf probe 0; sf read 0x02000000 0x80000 0x200000; bootm 0x02000000'; saveenv
mw.b 0x02000000 ff 1000000; tftp 0x02000000 uImage.gm8136; sf probe 0; sf erase 0x80000 0x200000; sf write 0x02000000 0x80000 ${filesize};
mw.b 0x02000000 ff 1000000; tftp 0x02000000 rootfs.squashfs.gm8136; sf probe 0; sf erase 0x280000 0x500000; sf write 0x02000000 0x280000 ${filesize}; reset
```

![SSH Login](/assets/images/the-openipc-project-1/ssh-login.png)

Once you're done with the server, unload the daemon with

```zsh
% sudo launchctl unload /System/Library/LaunchDaemons/tftp.plist
```

While my SoC is not fully and officially supported by the project, as seen on https://openipc.org/supported-hardware/featured, it, at least, booted correctly but I haven't had any image from the sensor. The Majestic (the streamer software) gave me the following errors:

```zsh
23:49:50  <       majestic> [     sdk] encode_thread@209             Timeout get any data from venc channel 0
23:49:50  <       majestic> [     sdk] encode_thread@209             Timeout get any data from venc channel 0
23:49:51  <       majestic> [     sdk] encode_thread@209             Timeout get any data from venc channel 0
23:49:51  <       majestic> [     sdk] encode_thread@209             Timeout get any data from venc channel 0
```

![Camera open](/assets/images/the-openipc-project-1/inside_1.jpg)

Time passed, and I ended up joining the OpenIPC Telegram group: [#@openipc](https://web.telegram.org/k/#@openipc). There, I found a very active community, and the project's core maintainers were very willing to help. I exchanged messages with Willmerson, and he pointed me to testing different sensors, like the `sc1045` and `sc1145`. 

![Video sensor detail](/assets/images/the-openipc-project-1/sensor_detail.jpg)

After hitting the wall several times, Will shared with me a handful of modules, including the `soih61`. After reconfiguring the `load_grainmedia` script to add the new definition and setting the `SENSOR` environment variable, the camera started to show the video stream!

```zsh
"soih61")
    codec_max_width=1280
    codec_max_height=720
    if [ "$video_system" == "NTSC" ]; then
        insmod fisp328.ko cfg_path=/etc/sensors/isp328_soih61.cfg
        insmod fisp_algorithm.ko pwr_freq=0
        insmod fisp_soih61.ko sensor_w=1280 sensor_h=720 fps=30
    elif [ "$video_system" == "PAL" ]; then
        insmod fisp328.ko cfg_path=/etc/sensors/isp328_soih61.cfg
        insmod fisp_algorithm.ko pwr_freq=1
        insmod fisp_soih61.ko sensor_w=1280 sensor_h=720 fps=25
    fi
    ;;
```

I also had to copy the `fisp_soih61.ko` object linked file, which Will shared with me

```zsh
cp fisp_soih61.ko /lib/modules/3.3.0/grainmedia/fisp_soih61.ko
```

The `SENSOR` environment variable was set as:

```bash
fw_setenv sensor soih61
```

![Video stream working](/assets/images/the-openipc-project-1/video_live.png)

These changes, as well as the required `.ko` module are now part of the nightly builds [since my changes are now merged successfully](https://github.com/OpenIPC/firmware/commit/525c6aa5e43cd6be572f185e18161a1389425b20).


## What does not work yet

While getting a video was an amazing milestone, I still needed to figure out how to drive the pan and tilt motors and enable the WiFi module, microphone, and speaker. Right now, the camera does not have a PTZ. Speaking of WiFi, the camera has a RTL8188u, or RTL8188eu and I'm currently messing around with the `wext` driver. While I got the driver working for scanning I cannot connect to access points yet.


## Conclusion

The OpenIPC project is a great opportunity to de-bloat any knockoff security camera and give it a new life with open-source software. Tied with a great community, this is a great project to get involved in and contribute.