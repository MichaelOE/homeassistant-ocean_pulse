# Fisker Ocean Pulse custom integration for Home Assistant
[![BuyMeCoffee][buymecoffeebadge]][michaeloe-buymecoffee]

##### 2026-06-09: Renamed integration to 'Ocean Pulse' and testing towards Pulse connection...

##### 2026-04-24: Still waiting for 'pulse' to arrive. Fully expecting this to come back alive after that... 🤞

##### 2025-05-16: Possible issues with cloud access due to AL cutting connection

Custom integration for getting information about your Fisker Ocean presented in Home Assistant.

## Target
The project is meant to get all available sensor values from Fisker Ocean cars via the Ocean Pulse device.

## Method
At regularly intervals poll the cloud service for updated values.

## Sensors
All values exposed by the cloud api are available as sensors in Home Assistant.

# Features
Currently only sensor values are present

# Installation and setup
This integration can be installed through HACS.

Alternatively, you can get the custom repository here: https://github.com/MichaelOE/home-assistant-ocean_pulse

## Setup
- QR code: Enter QR code digits to connect to cloud
- Alias: Prefix, which is used on all entity names created by the integration

# Usage
For showing the vehicle on a map, this can be used:

```python
alias: Fisker Ocean update location
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.fisker_location_latitude
      - sensor.fisker_location_longitude
condition: []
action:
  - service: device_tracker.see
    metadata: {}
    data:
      dev_id: my_fisker_location
      gps:
        - "{{ states('sensor.fisker_location_latitude') }}"
        - "{{ states('sensor.fisker_location_longitude') }}"
mode: single
```

I have used [apexchart](https://github.com/RomRider/apexcharts-card) for visualization.
In the screenshot above showing remaining range/battery I used the following (note the 'battery-calculation', which is because Fisker API sometimes returns zero miles):

```python
type: custom:apexcharts-card
apex_config:
  chart:
    height: 250px
    toolbar:
      show: true
      tools:
        selection: true
        download: false
        zoom: false
        zoomin: true
        zoomout: true
        pan: true
        reset: true
    zoom:
      enabled: true
header:
  show: true
  title: Range
  colorize_states: true
  show_states: true
graph_span: 24h
yaxis:
  - id: range
    min: 0
    max: 700
    apex_config:
      tickAmount: 10
  - id: battery
    opposite: true
    min: 0
    max: 100
    apex_config:
      tickAmount: 10
series:
  - entity: sensor.fisker_battery_max_miles
    transform: 'return x == 0 ? null : x;'
    extend_to: false
    yaxis_id: range
    fill_raw: last
    stroke_width: 2
  - entity: sensor.fisker_battery_percent
    yaxis_id: battery
    fill_raw: last
    stroke_width: 2
```

# Known issues
- n/a
