# Ocean Pulse – Fisker Ocean custom integration for Home Assistant

[![BuyMeCoffee][buymecoffeebadge]][michaeloe-buymecoffee]

> Formerly **My Fisker**  
> Home Assistant integration for **Fisker Ocean** vehicles using the **Ocean Pulse** aftermarket device.

## Target

The project provides sensor data and controls for **Fisker Ocean** vehicles through the **Ocean Pulse** device for use in Home Assistant.

## Method
The integration polls the cloud service at regular intervals for updated values.

## Features
- **Sensors** – all values exposed by the cloud API are available as sensors in Home Assistant
- **Device tracker** – the vehicle location is exposed as a `device_tracker`
- **Controls** – buttons for sending commands to the vehicle (see below)

### Sensors

<img width="407" height="2005" alt="billede" src="https://github.com/user-attachments/assets/8f5a139c-fca7-48b6-aed6-e25a328edf83" />

### Controls
The following buttons are available. More controls may be added in the future.

| Button | Action |
|---|---|
| Lock Doors | Locks the doors |
| Unlock Doors | Unlocks the doors |
| Trunk | Operates the trunk |
| Cabin climate (15 min) | Turns on cabin climate for 15 minutes |
| Cabin climate off | Turns off cabin climate |

## Installation

### Home Assistant Marketplace
The integration is **waiting for approval** to be listed in the Marketplace. Until it is approved, add it from a link:

1. Go to **Settings → Marketplace**
2. Select **Add from link** in the upper-right corner
3. Enter `MichaelOE/homeassistant-ocean_pulse` (or the full URL `https://github.com/MichaelOE/homeassistant-ocean_pulse`) as the GitHub link
4. Find **Ocean Pulse** in the Marketplace and click **Download**
5. Restart Home Assistant

Once approved, you will be able to find **Ocean Pulse** directly in the Marketplace without adding it from a link.

## Setup
After installing and restarting, go to **Settings → Devices & services → Add integration** and search for **Ocean Pulse**.

- **Pairing code** – in the Pulse dashboard on 'https://www.oceanlinkpulse.com', go to **Pair a phone** and click **Create pairing code**. Enter 6 digit code to connect to the cloud
- **Alias** – prefix used on all entity names created by the integration
- **Vehicle VIN** – the VIN of your vehicle

## Known issues
- None at the moment. Please [open an issue](https://github.com/MichaelOE/homeassistant-ocean_pulse/issues) if you find one.
