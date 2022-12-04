# The C64 250407 replica

A replica of the Commodore 64 250407 1983 mother board, and the schematics.

The replica project was started by Michael K. (Der Alte Bastler) in 2019 to learn SprintLayout and the process of reverse engineering PCB. I finished it, importet it in KiCad, imported the KU motherboard schematics and modified it to match the 250407 Reb.B schematics.

The board has been prototyped, and tested by me and Langwell Cowan.

We are not the first to reverse engineer this board, but we are the first to share the design files online I think.

![screenshot top](250407_3D_top.png)
![screenshot bottom](250407_3D_bottom.png)

# BOM

Please see the [BOM file](250407_bom.csv).

Note that some values were left blank because they depend on the clock circuit (PAL/NTSC), and PLA model. They never made it into the schematics. You can find them in a table to the right of the schematics for 250407.
http://www.zimmers.net/anonftp/pub/cbm/schematics/computers/c64/index.html

# Interactive-BOM

[The interactive bom html page](https://htmlpreview.github.io/?https://raw.githubusercontent.com/bwack/C64-250407-Replica-KiCad/main/interactive-bom/ibom.html) is useful for assembling the board and finding signal traces by using a web browser. Try it here. For a BOM for ordering parts see the BOM above.

![alt text](ibom-preview.png)

# Schematics

Download the PDF file [250407_.pdf](250407_.pdf) for a high quality schematics.
Checkout [this tweet](https://twitter.com/paulrickards/status/1371988589974847492) by Paul Rickards where he plots the KU motherboard schematics KU-14194HB :-)

# Change log
- 2022-08-18: Schematics V1.2: symbol and ERC fixes (Pull request from Gabriele Gorla/GGLABS)
- 2020-06-19: PCB and schematics V1.1: First release
- 2020-04-22: PCB and schematics V1.0: Prototype

# YouTube

Part 1-4:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/ox3BLlNSVFU/0.jpg)](https://www.youtube.com/watch?v=ox3BLlNSVFU)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/tBIvXRH-Mj0/0.jpg)](https://www.youtube.com/watch?v=tBIvXRH-Mj0)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/Mg0gVhXbaxc/0.jpg)](https://www.youtube.com/watch?v=Mg0gVhXbaxc)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/UPUVA1PZOOk/0.jpg)](https://www.youtube.com/watch?v=UPUVA1PZOOk)

# License and Disclaimer

Copyright Bwack 2021

This documentation describes Open Hardware and is licensed under the CERN OHL v. 1.2.

You may redistribute and modify this documentation under the terms of theCERN OHL v.1.2. (http://ohwr.org/cernohl). This documentation is distributed WITHOUT ANY EXPRESS OR IMPLIED WARRANTY, INCLUDING OF MERCHANTABILITY, SATISFACTORY QUALITY AND FITNESS FOR APARTICULAR PURPOSE. Please see the CERN OHL v.1.2 for applicable conditions.
