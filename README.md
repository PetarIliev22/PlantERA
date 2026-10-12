<div align="center">

<table>
<tr>
<td bgcolor="#ffffff" align="center">

<img src="assets/img/logo/plantera_logo.png" alt="PlantERA Logo" width="180">

</td>
</tr>
</table>

# PlantERA

### ESP32 Provisioning & Device Management Tool

PlantERA is a desktop application for detecting, provisioning, configuring and managing ESP32-based plant care devices.

Built with **Python + PySide6**.

</div>

---

## Overview

PlantERA provides a desktop environment for preparing ESP32 devices before deployment.

The application is designed to handle the complete provisioning workflow — from detecting the connected board and reading its unique identity to firmware installation, device configuration and future security operations.

---

## Current Features

- Automatic ESP32 detection
- COM port discovery and selection
- ESP32 board identification
- Device UID generation from the ESP32 hardware MAC
- Device information display
- Hardware profile detection
- Hardware specifications display
- Copyable device UID
- Connection / disconnection state handling
- BOOT detection dialog
- JSON-based device profiles
- Modular PySide6 interface
- QSS component styling
- Unit tests for UID generation and configuration loading

---

## Planned Provisioning Flow

```text
Detect ESP32
    ↓
Identify hardware
    ↓
Read device UID
    ↓
Select PlantERA model
    ↓
Flash firmware
    ↓
Write configuration
    ↓
Generate device identity
    ↓
Register device
    ↓
Run hardware tests
    ↓
Finalize & secure device