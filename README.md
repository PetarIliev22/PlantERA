<div align="center">

<img src="assets/img/logo/plantera_full_logo.png" alt="PlantERA Logo" width="520" style="margin: 0 auto;">

### ESP32 Provisioning & Device Management Tool

A desktop application for detecting, provisioning, configuring and managing ESP32-based PlantERA devices.

Built with **Python**, **PySide6**, **esptool** and **pyserial**.

</div>

---

## Overview

PlantERA is a desktop provisioning tool designed to prepare ESP32-based devices before deployment.

The application provides a structured workflow for:

- detecting connected ESP32 boards
- identifying the hardware
- generating a stable device UID
- displaying board specifications
- preparing devices for firmware provisioning
- supporting future security and registration workflows

The project is designed with a modular architecture so that new boards, device profiles and provisioning steps can be added without rewriting the entire application.

---

## Current Features

- Automatic COM port discovery
- ESP32 detection through `esptool`
- Hardware chip identification
- Device UID generation from ESP32 hardware identity
- Device information panel
- Hardware profile detection
- Hardware specifications loaded from JSON
- Device connection state handling
- BOOT detection dialog
- Modular PySide6 interface
- Component-based QSS styling
- Resource path handling for future packaging
- Unit tests for critical helper logic

---
