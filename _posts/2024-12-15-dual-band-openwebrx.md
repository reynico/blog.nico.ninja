---
layout: post
title: "VHF/UHF OpenWebRX+ receiver"
date: 2024-12-15 12:30:00 -0300
tags: [Radio, DIY]
description: Building a dual band OpenWebRX+ receiver
---

Following my journey in the Ham Radio operation world, given that I now have a VHF/UHF antenna, I thought it would be awesome to spin up a VHF and UHF Internet-enabled SDR receiver.

![SDR Waterfall](/assets/images/openwebrx-1/waterfall.png)

- [Software](#software)
  - [Install](#install)
  - [Configuration](#configuration)
- [Hardware](#hardware)
  - [Insertion loss](#insertion-loss)
- [Conclusions](#conclusions)


I think it is a great tool for people testing their equipment and also a good ally for those who haven't bought their first radio yet but want to listen to what other colleagues are talking about.

![Flowerpot](/assets/images/openwebrx-1/balcony_flowerpot.jpg)


My journey with Software Defined Radio started 13 years ago, messing around with the blueish plastic case DVB-T SDR receivers, and I never stopped to play with them. I usually work with my father, LU3DJ, bringing up new WebSDR receivers around Argentina. We think it is a great way to bring people closer to the radio, covering different areas of the globe.

![LU8FCJ SDR](/assets/images/openwebrx-1/lu8fcj_sdr.jpg)
> LU8FCJ's WebSDR internals, [http://el22.dyndns-blog.com:8080/](http://el22.dyndns-blog.com:8080/)

# Software

Since 2011, we have built our very first Internet-enabled SDR receiver. Many things have changed, and I decided to run mine with [OpenWebRX Plus](https://github.com/0xAF/openwebrxplus) on a Ubuntu virtual machine in my [Home Server with Proxmox](https://blog.nico.ninja/my-home-server/).

## Install

Installation is easy. You can follow the official instructions [here](https://luarvique.github.io/ppa/#if-you-are-an-ubuntu-2204-user-). Once you run these commands, you will get your OpenWebRX+ available at [http://localhost:8073/](http://localhost:8073/)

```bash
curl -s https://luarvique.github.io/ppa/openwebrx-plus.gpg | sudo gpg --yes --dearmor -o /etc/apt/trusted.gpg.d/openwebrx-plus.gpg
sudo tee /etc/apt/sources.list.d/openwebrx-plus.list <<<"deb [signed-by=/etc/apt/trusted.gpg.d/openwebrx-plus.gpg] https://luarvique.github.io/ppa/noble ./"
sudo apt update
sudo apt install openwebrx
```

## Configuration

Configuration can be done manually via the web interface at [http://localhost:8073/settings](http://localhost:8073/settings), or through the JSON files stored in `/var/lib/openwebrx/`. I will only share the SDR settings section of the `settings.json` file:

```json
"sdrs": {
    "rtlsdr-a": {
        "name": "RTL-SDR a",
        "type": "rtl_sdr",
        "device": "1",
        "profiles": {
            "2m": {
                "name": "2m",
                "center_freq": 144500000,
                "rf_gain": 40.0,
                "samp_rate": 2048000,
                "start_freq": 143625000,
                "start_mod": "nfm",
                "tuning_step": 5000
            }
        }
    },
    "rtlsdr-b": {
        "name": "RTL-SDR b",
        "type": "rtl_sdr",
        "device": "0",
        "profiles": {
            "70cm": {
                "name": "70cm",
                "center_freq": 446000000,
                "rf_gain": 49.0,
                "samp_rate": 2400000,
                "start_freq": 446705000,
                "start_mod": "nfm",
                "tuning_step": 5000
            }
        }
    }
}
```

# Hardware

For this project, I decided to run two RTL-SDR v3 receivers coupled to the same antenna. The best way to share an antenna among multiple receivers is by using a splitter. Connecting the receivers directly to the antenna and between them (like if you were doing an electrical derivation) may lead to impedance mismatch, and the receiver performance would be very low. A standard CATV splitter is a simple way to split the signal. You will need some SMA to F-type connector adapters.

![Splitter](/assets/images/openwebrx-1/sdrs_splitter.jpg)


## Insertion loss

CATV splitters are marked as having between -4dB and -5dB of insertion loss due to the nature of the resistive-type splitters; nevertheless, I noticed a 2.5 to 3dB drop in the signal in VHF.

I set my HackRF to transmit a beacon at 145MHz with very low power for the loss test. A Python script with Numpy helped create the IQ file.

```python
import numpy as np

# Parameters
sample_rate = 48_000
frequency = 1_000
duration = 1000
output_file = "1khz_beacon.iq"

# Generate time array
t = np.arange(0, duration, 1 / sample_rate)

# Generate I and Q signals (1 kHz tone)
i_signal = np.sin(2 * np.pi * frequency * t)
q_signal = np.cos(2 * np.pi * frequency * t)

# Interleave I and Q
iq_data = np.empty((i_signal.size + q_signal.size,), dtype=np.float32)
iq_data[0::2] = i_signal
iq_data[1::2] = q_signal

# Save to file
iq_data.tofile(output_file)
print(f"1 kHz beacon saved to {output_file}")
```

The IQ file can be transmitted with

```bash
hackrf_transfer -t 1khz_beacon.iq -f 145000000 -s 2000000 -a 1 -x 20
```

![Signal loss](/assets/images/openwebrx-1/signal_comparison.png)

# Conclusions

It's been a few weeks since I started this SDR receiver, and I am more than happy with the results. While the antenna is not the best for the job, nor is its location favorable, I could listen to stations up to 13-15 km from my apartment, which is a great coverage range for a busy city such as Buenos Aires.

I plan to move the SDR receiver to the terrace during the summer since I can access one of my apartment's windows directly. I would probably set a Raspberry PI 4 up there to reduce the RF loss due to the long cable trajectory (around 20 meters).