The PuttyDepthLogger is a compact underwater depth and temperature recorder built around the Adafruit Feather RP2040 Adalogger and the LPS28 pressure sensor.
It demonstrates a new approach to underwater electronics packaging using a non-Newtonian, putty-based, reworkable potting method. Over long timescales the putty flows to fill voids and displace compressible air, while during fast removal it behaves like a solid, allowing the entire electronics assembly to be opened, serviced, and reassembled without destructive potting.

This encapsulation method also enables 3D-printed housings to be used as waterproof enclosures, eliminating the need for machined pressure housings or epoxy-filled assemblies.
The goal of this methodology is to lower the barriers to building underwater instruments, making marine exploration and sensing more accessible to students, researchers, makers, and small organizations.

**This project includes:**

- Custom CircuitPython firmware (firmware.uf2) enabling the Adalogger’s SD card to appear as a USB-readable drive — not supported in the stock CircuitPython build.

- A dual-mode boot system controlled by an SPDT magnetic reed switch.

- code.py for timestamped pressure/temperature logging at 1 Hz.

- boot.py for safe filesystem handling based on the reed switch position.

**Dual-Mode Magnetic Reed Switch System**

A single-pole, dual-throw (SPDT) magnetic reed switch provides reliable hardware-level control of the boot mode without opening the enclosure.

Switch wiring:

- NC → BAT+

- NO → GND

- Common wiper → D9

Magnet away → wiper on NC → D9 = HIGH
Magnet present → wiper on NO → D9 = LOW

                  Li-Ion 3.7V (BAT+)
                      +
                      |
                     NC
                      o--------+
                               |
                               |
                            ( wiper ) ----→ D9
                               |
                               |
                     NO        o--------→ GND

**Mode Behavior**

HIGH (magnet away → NC → BAT+)
Normal Logging Mode

- SD card writable by CircuitPython

- CIRCUITPY locked read-only (protects running code during logging)

LOW (magnet present → NO → GND)
Maintenance / USB Mode

- CIRCUITPY writable over USB

- SD card read-only and protected from corruption

- Safe for firmware updates or extracting log files

**Firmware and Code Included**

firmware.uf2
- Custom CircuitPython build enabling USB access to the Adalogger’s SD card.

boot.py
- Mounts/remounts CIRCUITPY and the SD card according to D9’s hardware state.

code.py
- Logs:

  - epoch timestamp

  - pressure in hPa

  - temperature in °C once per second to incrementing CSV files.

**Hardware Overview**

Minimum required components:

- Adafruit Feather RP2040 Adalogger

- LPS28 / LPS28DFW pressure sensor (I²C)

- MicroSD card (FAT32)

- SPDT magnetic reed switch

- 3.7 V Li-ion battery

- 3D-printed enclosure

- Non-Newtonian reworkable potting putty

Because this putty effectively eliminates trapped air and tolerates small imperfections, 3D-printed housings become viable waterproof enclosures, even at meaningful depths.

**Grant Acknowledgment**

This work was funded by a grant from Experiment.com.
Project progress, experiments, and background can be followed here:

https://experiment.com/projects/non-newtonian-fluids-as-a-reworkable-potting-material-for-marine-electronics
