<table width="100%">
<tr>
<td align="center" bgcolor="#ffffff">

<br>

<img
    src="assets/img/logo/plantera_full_logo.png"
    alt="PlantERA"
    width="520"
/>

<br>

### ESP32 Provisioning & Device Management

A modern desktop provisioning application for preparing, identifying, configuring and securing PlantERA ESP32 devices.

<br>

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![ESP32](https://img.shields.io/badge/ESP32-Espressif-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://www.espressif.com/)
[![esptool](https://img.shields.io/badge/esptool-5.4.0-222222?style=for-the-badge&logo=espressif&logoColor=white)](https://github.com/espressif/esptool)
[![PySerial](https://img.shields.io/badge/pyserial-3.5-306998?style=for-the-badge&logo=python&logoColor=white)](https://pyserial.readthedocs.io/)
[![pytest](https://img.shields.io/badge/pytest-9.1.1-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

<br>

**Detect · Identify · Provision · Secure**

<br>

</td>
</tr>
</table>

---

## PlantERA

**PlantERA** is a desktop provisioning and device-management application built for ESP32-based PlantERA hardware.

The application is designed to prepare devices before deployment by identifying connected hardware, generating a stable device identity, presenting hardware information and providing the foundation for firmware provisioning, security configuration and backend registration.

The project is built with a modular architecture so new hardware profiles, provisioning stages and security features can be added without restructuring the entire application.

---

## Current Features

- Automatic COM port discovery and USB monitoring
- ESP32 detection through `esptool`
- Hardware chip identification
- Stable device UID generation from ESP32 hardware identity
- Device connection state management
- Automatic UI reset when a USB device is disconnected
- Device information panel
- Hardware profile matching
- Hardware specifications loaded from JSON
- Interactive BOOT detection workflow
- Retry and failure states
- Responsive desktop interface
- Custom frameless application window
- Component-based PySide6 UI architecture
- Independent QSS stylesheets
- Application resource-path handling
- Fade animations
- Unit tests for critical application logic

---
