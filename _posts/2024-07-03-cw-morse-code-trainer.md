---
layout: post
title: "CW Morse code trainer"
date: 2024-07-03 18:30:00 -0300
tags: [Electronics, DIY]
description: Learning Morse Code in a fun way
---

This year, I enrolled in a three-month ham radio course to get my ham radio license and be able to transmit and talk with the folks. The course is divided into five steps, one of which is Morse Code, or CW, in the amateur radio jargon. Practicing some Morse code with a standalone device would be cool!

![Morse Trainer powered on](/assets/images/cw-morse-trainer-1/powered-on.jpg)


At first, I thought of coding the entire thing by myself, but I gave up since I am running too many projects in parallel, so digging the Internet, I found Garry's blog with an excellent fit of a [Morse trainer project with Arduino](https://garrysblog.com/2020/03/22/morse-code-decoder-using-an-arduino-nano/). Even it takes care of the Prosigns! [I forked out the project into my own GitHub account](https://github.com/reynico/arduino-morse-code-decoder) and adjusted the code to match some of my specs, such as using an HD44780 20x4 LCD driven through i2c, setting auto/manual modes through the same speed potentiometer, adding a button to clear out the screen, etc.

![Wiring](/assets/images/cw-morse-trainer-1/wired.jpg)


During my practices, I found a button to clear the screen contents useful, so I didn't need to reset the microcontroller. I attached a button that puts down D3 into the ground to clear the screen.

![Front Panel](/assets/images/cw-morse-trainer-1/front-panel.jpg)


I also found the auditive feedback of a speaker helpful. I built a simple oscillator with three transistors. At first, I tried to use Arduino's `tone()` command, but `tone()` messes up with the microcontroller timings and is unsuitable for this project when using interrupts.

![Speaker](/assets/images/cw-morse-trainer-1/speaker.jpg)


The 3D-printed case was divided into two parts: the body containing the Arduino Nano (in a USB-C flavor) and the speaker. The front panel holds the 20x4 LCD screen, two potentiometers, the clear screen button, and the audio jack for the keyer.


## Bill of Materials
Here's the complete BOM and related files for building this project.

| QTY | Description             | Usage                      |
| --- | ----------------------- | -------------------------- |
| 1   | Arduino Nano            | Microcontroller            |
| 2   | BC548 or NPN-compatible | Audio Oscillator           |
| 1   | BC559 or PNP-compatible | Audio Oscillator           |
| 1   | 33k Ohm resistor        | Audio Oscillator           |
| 1   | 0.1uF x 16v capacitor   | Audio Oscillator           |
| 4   | 3.5mm jack              | Keyer connector            |
| 2   | 10k Ohm potentiometers  | Volume and Speed selectors |
| 1   | i2c HD44780 20x4 LCD    | LCD Screen                 |
| 1   | 8 Ohm 0.5 watt speaker  | Speaker                    |
| 1   | Square button           | Clear screen button        |

## Resources
* [Morse Code Decoder using an Arduino Nano, from Garry's Blog](https://garrysblog.com/2020/03/22/morse-code-decoder-using-an-arduino-nano/)
* [My fork from Garry's code](https://github.com/reynico/arduino-morse-code-decoder)
* [The schematic circuit](https://github.com/reynico/arduino-morse-code-decoder/blob/master/schematic.pdf)
* [The 3D Printer STL files](https://github.com/reynico/arduino-morse-code-decoder/tree/master/3d-printed-case)