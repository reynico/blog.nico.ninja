---
layout: post
title: "GOES satellite reception part 1"
date: 2024-01-17 18:10:00 -0300
tags: [Computers, Radio]
description: A journey on trying to receive satellite images from the GOES 16
---

This is the first of a series of posts about receiving and decoding images from the GOES 16 satellite, a geosynchronous, sophisticated satellite that operates in L-Band (1694.1 MHz) and sends images in [HRIT](https://www.noaasis.noaa.gov/GOES/HRIT/about_hrit.html) format. The satellite sends beautiful pictures of the whole earth, and in this episode, we'll talk about the required hardware and software to make that possible. Since the proper LNA for reception is not with me yet, I wouldn't be able to test the reception yet.

- [Bill of Materials](#bill-of-materials)
- [Antenna design](#antenna-design)
  - [The dish](#the-dish)
  - [The feed](#the-feed)
    - [Concerns with the feed](#concerns-with-the-feed)
- [Software](#software)
- [Downloads](#downloads)
- [Final words](#final-words)



# Bill of Materials
* A computer or Raspberry PI running Linux, preferably Ubuntu or Debian.
* An [RTL-SDR dongle](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) would suffice, but a more advanced hardware like a [HackRF](https://greatscottgadgets.com/hackrf/) may create a better experience.
* A Low-Noise Amplififer (LNA) with a SAW Filter, like the [Nooelec SAWbird+ GOES](https://www.nooelec.com/store/sawbird-plus-goes.html).
* A satellite dish or a Wi-Fi grid antenna.
* Access to a 3D printer.
* RF cables or pigtails.
* [A RF N-Connector, chassis mount](/assets/files/goes-part-1/connector.pdf).


# Antenna design
Since we are trying to receive very weak signals from a transmitter orbiting at ~36.000KM, we will need a quite special antenna. First, we need to source an old satellite dish antenna, I got a secondhand cheap 80cm dish from the Internet.

![Orbit](/assets/images/goes-part-1/orbit.jpg)


## The dish
Almost any dish antenna will do the work, there are some variants of these dishes like offset and prime-focus antennas. Offset antennas are commonly those used for Satellite TV like DirecTV, where the dish structure is asymmetric, more like an oval and the feed has an arm installed. Those are the more common types you may source for cheap.

![Prime Focus and Offset antennas](/assets/images/goes-part-1/dish-prime-antennas.png)


## The feed

There are several feed designs, but one I liked much is the LHCP (Left-hand circular polarized) helix antenna. Since we're trying to receive an RHCP (Right-hand circular polarized) signal from the satellite, the feed should be the opposite because the dish reflection inverts the signal phase. 

[Derek](https://twitter.com/dereksgc) designed a [helix antenna scaffold](https://www.thingiverse.com/thing:4980180) that is highly configurable with [OpenSCAD](https://openscad.org/), so you can adjust the size, number of turns and polarization before printing it. In my case, I opted to print the `1700L_7.5T_0.14S_4D_10-90M.stl` file. It stands for:

* 1700 MHz
* Left-hand polarization
* 7.5 Turns


I've used a 20x20cm PCB board and some standard hardware to build the feed. If you plan to follow my journey, [here is a printable A4 page](/assets/files/goes-part-1/pcb-antenna-drawing.pdf) and [the AutoCAD DWG editable file](/assets/files/goes-part-1/pcb-antenna-drawing.dwg) you can glue over the PCB to make the holes for the N-Connector, the helix scaffold and the support. Additionally, I printed an ["L" support (STL file here)](/assets/files/goes-part-1/lnb-mount.stl) to screw the PCB patch to the standard LNB support of the dish antenna. Don't be desperate, I will leave all the downloadable files at the end of the post.

![Feed construction 1](/assets/images/goes-part-1/antenna-build-1.jpg)


Once drilled and some of the parts installed, the feed starts to have a better look.

![Feed construction 2](/assets/images/goes-part-1/antenna-build-2.jpg)


Patience is key when it comes to winding the scaffold. I suggest you pre-winding the wire over a circular object like a small bottle or a soda can.

![Feed construction 3](/assets/images/goes-part-1/antenna-build-3.jpg)


The mounted feed looks great, but I am unsure about both the focal distance and focal position so I may need to redo the ["L" support](/assets/files/goes-part-1/lnb-mount.stl).

![Feed installed](/assets/images/goes-part-1/antenna-build-4.jpg)


### Concerns with the feed

There are some caveats with the current design of my feed, but they are only visual appreciations:
* I think the PCB is way too big, I'll try to make it smaller, like 12 x 12 cm or similar so it doesn't eclipse the dish that comes into the dish.
* I'm not happy at all with the feed position relative to the dish focal point. For me, it seems like it needs to go lower.

I'll give it a try soon and see how it behaves with real signals.


# Software

I've been investigating software for GOES decoding and I found [goestools](https://github.com/pietern/goestools) very promising, but unmaintained for a few years. I tried to build goestools on my [2011 Macbook Air](https://blog.nico.ninja/macbook-air-ubuntu/) (That runs Linux) and encountered some caveats here and there so I decided to [fork](https://github.com/reynico/goestools) the project and try fixing those errors. With the help of the community, I was able not just to fix the compilation errors but also to bring back the [GitHub Actions CI builds](https://github.com/reynico/goestools/actions).

![Running goesrecv](/assets/images/goes-part-1/goestools-working.jpg)


# Downloads
I'll leave here the complete list of artifacts mentioned in the post, for the sake of clarity.

* [Dereksgc's helix scaffold tuned for 1.7GHz, LHCP](/assets/files/goes-part-1/1700L_5.5T_0.14S_4D_10-90M.stl).
* [Printable A4 drill template for the helix mount](/assets/files/goes-part-1/pcb-antenna-drawing.pdf) and the [editable DWG file](/assets/files/goes-part-1/pcb-antenna-drawing.dwg).
* ["L Support" to mount the feed into the dish antenna](/assets/files/goes-part-1/lnb-mount.stl).


# Final words

Since I don't have a proper [LNA/Filter](https://www.nooelec.com/store/sawbird-plus-goes.html) for this application, I wouldn't be able to completely test the full chain, so stay tuned for the next part!