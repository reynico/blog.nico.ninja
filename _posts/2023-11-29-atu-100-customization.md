---
layout: post
title: "ATU-100 antenna tuner configuration"
date: 2023-11-29 11:00:00 -0300
tags: [Radio, Electronics]
description: My journey during the configuration of the ATU-100 antenna tuner
---

![Kenwood TL-922 maxed out](/assets/images/atu-100-customization-1/kenwood-meter.jpg)

The [N7DDC's ATU-100 automatic antenna tuner](https://github.com/Dfinitski/N7DDC-ATU-100-mini-and-extended-boards/tree/master/ATU_100_EXT_board) is a great piece of hardware for any radio ham trying to adjust their SWR while transmitting. The ATU-100 is an inexpensive hardware unit and can be configured by writing the [PIC16F1938's](https://www.microchip.com/en-us/product/pic16f1938) EEPROM.

- [Why](#why)
- [How](#how)
  - [Bill of materials](#bill-of-materials)
  - [Replacing the bit](#replacing-the-bit)
- [Testing](#testing)


# Why

My father has been using the ATU-100 on his projects for a while, but he complained more than once about the automatic SWR adjustment activation threshold, he was looking for the automatic routine to run whenever the SWR reaches 1.1:1 or higher, while by default, the ATU-100 does that when the SWR passes the 1.3:1 barrier.

# How

At first, I thought that the SWR threshold could be configurable through the already-installed buttons. Turns out that that wasn't the way.

Instead, you need to rewrite the https://www.microchip.com/en-us/product/pic16f1938) EEPROM in a specific memory pointer to reconfigure the ATU-100. Interesting. Luckily the [ATU-100 user's manual](https://github.com/Dfinitski/N7DDC-ATU-100-mini-and-extended-boards/blob/master/ATU_100_EXT_board/ATU_100_EXT_board_User_Manual/ENG_ATU-100_Extended_Board_User_Manual.pdf) covers the configuration in extent.

> During programming of the microprocessor, in addition to writing directly to the
control code (program), it is also proposed to record a small number of cells of the
rewritable memory EEPROM. The information in these cells can be changed by the
user before programming. During each start of the processor, its program first reads
data from the cells of long-term memory in order to further use this information for
work. Thus, the user can easily change many parameters of the device without
understanding the much more complex software development processes.

The ATU-100 provides a programming header that in normal operation is intended to drive a 128x64 OLED screen.

![ATU-100 programming header](/assets/images/atu-100-customization-1/atu-100-header.jpg)


## Bill of materials

We need just two things: A Microchip's PIC programmer and a computer with the programmer's software.

By checking on my drawers I found a VERY VERY VERY old PicKit2 clone called “[THOR Programmer](https://www.facebook.com/programadorusb.picthor)”, which is fully compatible with the [PicKit2 software](https://www.microchip.com/en-us/development-tool/pg164120) for Windows. I just had to connect the ATU-100 header to the programmer's header and the software recognized it in a blaze.

![PicKit2 clone](/assets/images/atu-100-customization-1/pickit2-clone.jpg)


## Replacing the bit

The user manual states:

> 04 — cell to set the threshold settings in automatic mode.
It is recorded in the format: the first number is the SWR integer part, the second
number is the tenths. The default value is 13. That is, when the automatic mode is
activated, the tuning process will be triggered when the SWR is above 1.3 and when
it changes to (1.3 — 1).

So we just need to change the default `13` value for `11`, to make the automatic routine trigger when SWR > 1.1

![PicKit2 programmer](/assets/images/atu-100-customization-1/pickit2-programmer.png)

First, we need to read the compiled code from the microcontroller, then modify the value, and last, upload the code again. And that's it!

# Testing

The tests were done with the Kenwood TL-922, and the ATU-100 hooked at its RF input. Tests were completed with success!

![ATU-100 hooked](/assets/images/atu-100-customization-1/kenwood-atu-100.jpg)
