---
layout: post
title: "HC-SR501 PIR Sensor and Home Assistant"
date: 2024-05-21 17:30:00 -0300
tags: [Electronics, DIY, Computers]
description: My journey through the PIR sensors
---

Living in a two-floor apartment has many good things and some bad things. And I assure you, trying to walk between the stairs semi-asleep in total darkness on an early winter morning is one of the worst. Follow me on my journey of automating as many things as I can at home.

![Motion sensor and bulb](/assets/images/pir-sensor-1/sensor-mounted.jpg)

- [Idea](#idea)
- [Bill of Materials](#bill-of-materials)
- [Hardware](#hardware)
  - [False triggers](#false-triggers)
  - [Coil whine](#coil-whine)
- [Software](#software)
  - [ESPHome](#esphome)
  - [Blueprint](#blueprint)
- [Conclusion](#conclusion)


# Idea

The stairs have a Philips Hue bulb, but turning it on requires me to ask Siri, use my phone, or touch something. After doing that, I would probably die due to the excess brightness. Since I now have a fully functional [Home Assistant](https://blog.nico.ninja/migrating-to-home-assistant/) setup and a bunch of ESP-01s to play with, I decided to build a motion sensor that will trigger the Philips Hue bulb at a low brightness value.

The triggering steps are easy:

1. A PIR sensor detects motion.
2. The nearby lamps are off already (hall, office).
3. There is no sun in sight.
4. Then, turn on the stairs lamp at a very low brightness value for a few seconds.

# Bill of Materials

- A working [Home Assistant instance](https://blog.nico.ninja/migrating-to-home-assistant/).
- An [HC-SR501](/assets/files/pir-sensor-1/hc-sr501.pdf) motion sensor.
- An ESP-01 microcontroller.
- A 5v or 3.3v power supply.
- A 220nF ceramic capacitor.

# Hardware

![Schematic circuit](/assets/images/pir-sensor-1/ha-motion-sensor_schem.png)

As it's not easy to get 220VAC to 3.3VDC converters, I used two 1n4148 diodes to step down the 5VDC voltage to ~3.4VDC. The SR-501 PIR sensor works excellently at this tension level despite the datasheet asking for a 5VDC input.

![Components glued](/assets/images/pir-sensor-1/components-glued.jpg)

## False triggers

After some tests, I found the [HC-SR501](/assets/files/pir-sensor-1/hc-sr501.pdf) prone to false triggers. I tried to set it in a controlled environment with no curtains, open windows, or air conditioner units, and I also tuned the “sensitivity” potentiometer. 

![Ceramic capacitor](/assets/images/pir-sensor-1/ceramic-cap.jpg)


I found [this Home Assistant Community thread](https://community.home-assistant.io/t/hc-sr501-no-good-for-esphome-change-the-docs/168483/5) very helpful, where a user recommends adding a 220nF capacitor between pins 12 and 13 of the [BISS0001](/assets/files/pir-sensor-1/BISS0001.pdf) PIR controller. 

![Added capacitors](/assets/images/pir-sensor-1/capacitors.jpg)

As I didn't have a 220nF capacitor, I soldered two 100nF capacitors in parallel, which did the trick. Check this comparison of sensor readings during the night:

Before the capacitor mod there were several triggers during the night:

![False triggers](/assets/images/pir-sensor-1/false-trigger.png)

After the capacitor mod the signal was clean all night. (I took the stairs at 7AM):
![False triggers](/assets/images/pir-sensor-1/false-trigger-solved.png)


## Coil whine

I've used these cheap power supplies, but they always ended up inside a cabinet and were far from the auditive spectrum. Since this motion sensor is mounted in the middle of the stairs and near my office, the coil whine drove me crazy, so I had to remove the motion sensor until getting this sorted out. 

![New power supply](/assets/images/pir-sensor-1/new-power-supply.jpg)
> The new power supply, a generic USB charger for cell phones.

Ultimately, I bought a generic USB cell phone charger that seemed more silent than the original power supply I purchased by some orders of magnitude, even though I decided to bathe the transformer in silicone with the glue gun to avoid any annoying hiss.

![Glued power supply](/assets/images/pir-sensor-1/power-supply-glued.jpg)

When testing a switching power supply like this, make sure you're putting some load into it. The coil will whine with load, so you will notice once you connect the electronics to it.

# Software

The software is easy to use. The ESPHome firmware only reads a [binary sensor](https://esphome.io/components/binary_sensor/index.html) (as the [HC-SR501](/assets/files/pir-sensor-1/hc-sr501.pdf) only outputs a TTL-level low or high signal). Then, the automation is done as a Blueprint.

## ESPHome

```yaml
binary_sensor:
  - platform: gpio
    id: stairs_pir_sensor
    pin: GPIO0
    name: "Stairs PIR Sensor"
    device_class: motion
```

## Blueprint

You will need to adjust the `device_id` and `entity_id`.

```yaml
alias: Turn on stairs light on darkness
description: "Turn on stairs light on darkness"
trigger:
  - type: motion
    platform: device
    device_id: 2b90174b320ec46ed58b25c4925d7503
    entity_id: fde5a1b9fcf2354cd25222be6101ecda
    domain: binary_sensor
    for:
      hours: 0
      minutes: 0
      seconds: 0
condition:
  - condition: device
    type: is_off
    device_id: a44691ab36d46631bef109c6c4f958df
    entity_id: 02973e5529e22bb9fc2ad5b315f9446d
    domain: light
  - condition: device
    type: is_off
    device_id: f46126447397c6c26df69dd20ef0a3d0
    entity_id: 4d09680e28d44ec8c7fcaeaa9fbbe2e4
    domain: light
  - condition: device
    type: is_off
    device_id: a7738268f974c22fae951da8336820c6
    entity_id: b42bc9d9d1b645e9a714a90bd1c6d734
    domain: light
  - condition: sun
    after: sunset
    before: sunrise
    enabled: true
action:
  - service: light.turn_on
    metadata: {}
    data:
      brightness_pct: 26
    target:
      entity_id:
        - light.entrepiso
  - delay:
      hours: 0
      minutes: 0
      seconds: 5
      milliseconds: 0
  - service: light.turn_off
    metadata: {}
    data:
      transition: 5
    target:
      entity_id: light.entrepiso
mode: single
```

# Conclusion

After having this setup working for a week or so, I can say that I'm more than satisfied with the result. I'm still amazed at what a great piece of software [Home Assistant](https://blog.nico.ninja/migrating-to-home-assistant/) is. It's not only easy to code and automate things but also cheap! You don't need anything fancy or special to start with.

![3D Printed case](/assets/images/pir-sensor-1/case-closed.jpg)
