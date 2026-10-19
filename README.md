# Ocean Pulse – Fisker Ocean custom integration for Home Assistant

[![BuyMeCoffee][buymecoffeebadge]][michaeloe-buymecoffee]

> Formerly **My Fisker**  
> Home Assistant integration for **Fisker Ocean** vehicles using the **Ocean Pulse** aftermarket device.

**Still beta - I have had a pulse installed since mid october '26 so expect changes/updates.**

## ⚠️ Breaking change (June 2026)
This integration has been renamed from **My Fisker** to **Ocean Pulse** and now uses the **Ocean Pulse device API**.

If you previously used **My Fisker** in HACS:

1. Uninstall **My Fisker**
2. Install **Ocean Pulse**
3. Reconfigure the integration

Entity names and sensor IDs have changed significantly.

## Target

The project provides sensor data from **Fisker Ocean** vehicles through the **Ocean Pulse** device for use in Home Assistant.

## Method
At regularly intervals poll the cloud service for updated values.

## Sensors
All values exposed by the cloud api are available as sensors in Home Assistant.
Location exposed also as device_tracker

<img width="409" height="2094" alt="Ocean Pulse Sensors" src="https://github.com/user-attachments/assets/09ab8104-4679-42dd-9955-48910ec34923" />

## Controls
Various controls (not implemented fully yet)

<img width="409" height="367" alt="image" src="https://github.com/user-attachments/assets/0fe557f0-0d68-4ec0-933b-c6b739f8c228" />


# Features
Currently only sensor values are present

# Installation and setup
This integration can be installed through HACS.

Alternatively, you can get the custom repository here: https://github.com/MichaelOE/homeassistant-ocean_pulse

## Setup
- QR code: Enter QR code digits to connect to cloud
- Alias: Prefix, which is used on all entity names created by the integration

# Known issues
- n/a
