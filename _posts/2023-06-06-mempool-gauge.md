---
layout: post
title: "A Bitcoin Mempool gauge indicator"
date: 2023-06-06 11:00:00 -0300
categories: [diy, electronics]
description: Measuring Bitcoin's next-block fee targets
---

![Mempool Gauge](/assets/images/mempool-gauge-1/mempool-gauge.jpg)

In the world of cryptocurrencies, the rising popularity of [BRC-20 tokens](https://brc-20.io/) on the Bitcoin blockchain has led to a surge in mempool fees. This has caused challenges for wallets using submarine swaps and users looking for fast and cost-effective transactions. To simplify this process, I came up with the idea of developing a "Mempool Load Indicator" that visually displays the next-block fee in sats/vByte using a gauge. The implementation was straightforward, utilizing a micro servo and an ESP8266.

![Schematic](/assets/images/mempool-gauge-1/schematic.png)

Initially, I encountered a minor setback with the servo I purchased. It failed to achieve the full 180-degree rotation as promised. However, I discovered a solution within the [Servo library](https://www.arduino.cc/reference/en/libraries/servo/attach/), using additional parameters to adjust the servo's performance. By experimenting with the values, I managed to achieve a satisfactory 180-degree sweep.

```c
s1.attach(5, 370, 2400);
```

To gather the necessary data, I utilized the [mempool's.space API](https://mempool.space/api/v1/fees/recommended), specifically the `fastestFee` value, which indicates the fee required for inclusion in the next block. The [ArduinoJSON](https://github.com/bblanchon/ArduinoJson) library proved invaluable in parsing JSON data from the internet, simplifying the processing steps, and handling any potential errors.

![3D model](/assets/images/mempool-gauge-1/3d-model.jpg)

I encountered a couple of challenges during the project. Firstly, I had to reverse the servo's motion to align it with the desired operation. Secondly, I wanted to limit the maximum fee displayed on the gauge. I successfully addressed both challenges using the `map()` function.

```c
int angle = map(fee, 1, 90, 180, 0);
```

In the future, I plan to introduce a revised version of the gauge that incorporates a logarithmic scale. This enhancement will allow the gauge to display higher values while maintaining the same size. By replacing the existing gauge numbers, a logarithmic scale can be easily implemented.

If you're interested in this project, you can find the [full code and 3D-printed model parts on GitHub](https://github.com/reynico/mempool-gauge)!