# SONAR - Ultrasonic Radar System

A real-time ultrasonic radar system using Arduino and Python that creates a live sonar-style display for object detection and ranging.
<img width="1155" height="783" alt="Screenshot 2025-08-13 at 2 22 16 PM" src="https://github.com/user-attachments/assets/7394264c-fab8-49ad-9ba6-6c3156b6be42" />

![IMG_4668](https://github.com/user-attachments/assets/88156978-a253-4a0e-8f4c-ea60aa7e6511)

## 🎯 Overview

SONAR combines an Arduino-controlled servo-mounted ultrasonic sensor with real-time Python visualization to create a rotating radar system. The system sweeps 180° back and forth, detecting objects within a 30cm range and displaying them on a live matplotlib radar screen.

## ✨ Features

- **🔄 180° Servo Sweep**: Continuous clockwise/counterclockwise rotation
- **📡 Real-time Detection**: HC-SR04 ultrasonic sensor with 2-400cm range
- **📊 Live Visualization**: Professional radar-style display with matplotlib
- **⚡ High Performance**: 50ms refresh rate with threaded data processing
- **🎨 Professional UI**: Dark theme with color-coded detections and status panel
- **📈 Data Logging**: Automatic data collection with statistics tracking
- **🔧 Multi-platform**: Supports Arduino Uno/Nano and ESP32

## 🛠️ Hardware Requirements

| Component | Quantity | Purpose |
|-----------|----------|---------|
| Arduino Uno/Nano or ESP32 | 1 | Main controller |
| HC-SR04 Ultrasonic Sensor | 1 | Distance measurement |
| SG90 Servo Motor | 1 | Sensor rotation |
| Jumper Wires | ~10 | Connections |
| Breadboard | 1 | Prototyping |
| USB Cable | 1 | Programming/Power |

## 📋 Pin Connections

### Arduino Uno/Nano
```
Servo Signal    → Pin 6 (PWM)
Ultrasonic Trig → Pin 9
Ultrasonic Echo → Pin 10
Power (5V/GND)  → Respective power rails
```

### ESP32 (Alternative)
```
Servo Signal    → Pin 18
Ultrasonic Trig → Pin 5
Ultrasonic Echo → Pin 18
Power (3.3V/GND) → Respective power rails
```

## 🚀 Installation

### 1. Hardware Setup
1. Connect components according to pin diagram above
2. Mount ultrasonic sensor on servo horn
3. Ensure stable power supply for servo operation

### 2. Arduino Firmware
```bash
# Using PlatformIO (Recommended)
git clone https://github.com/yourusername/sonar.git
cd sonar/arduino
pio run --target upload

# Or using Arduino IDE
# Open arduino/src/main.cpp in Arduino IDE
# Install Servo library if needed
# Upload to board
```

### 3. Python Dependencies
```bash
# Install required packages
pip install pyserial matplotlib numpy

# Or using requirements.txt
pip install -r requirements.txt
```

## 🎮 Usage

### Quick Start
1. **Upload Arduino firmware** to your board
2. **Connect hardware** according to pin diagram
3. **Run Python visualization**:
   ```bash
   python python/radar_display.py
   ```
4. **Watch the live radar** display objects in real-time!

### Advanced Configuration

#### Arduino Settings (platformio.ini)
```ini
[env:uno]
platform = atmelavr
board = uno
framework = arduino
lib_deps = arduino-libraries/Servo@^1.1.8
monitor_speed = 9600
```

#### Python Parameters
```python
# In radar_display.py
DETECTION_RANGE = 30.0    # cm - maximum detection range
GRAPH_SCALE = 5.0         # units - graph radius (5 units = 30cm)
UPDATE_INTERVAL = 50      # ms - display refresh rate
FADE_TIME = 15.0          # seconds - detection fade duration
```

## 📊 Display Elements

| Element | Description | Color |
|---------|-------------|-------|
| **Green Circle** | 30cm detection boundary | Green |
| **Red Line** | Current servo position | Red |
| **Colored Dots** | Detected objects | Plasma colormap |
| **Range Rings** | Distance markers (6cm intervals) | Gray |
| **Status Panel** | Real-time statistics | White |

### Detection Visualization
- **Bright/Large dots**: Recently detected objects
- **Dim/Small dots**: Older detections (fading out)
- **Position**: Exact location based on angle + distance
- **Persistence**: Detections fade over 15 seconds

## 📁 Project Structure

```
sonar/
├── arduino/                 # PlatformIO Arduino project
│   ├── platformio.ini      # Build configuration
│   ├── src/
│   │   └── main.cpp        # Arduino firmware
│   └── include/
│       └── README.md       # Hardware documentation
├── python/                  # Python visualization
│   ├── radar_display.py    # Main display application
│   └── requirements.txt    # Python dependencies
├── docs/                    # Documentation
│   ├── wiring_diagram.png  # Connection diagram
│   └── screenshots/        # Display examples
└── README.md               # This file
```

## ⚙️ Configuration

### Servo Parameters
```cpp
// In arduino/src/main.cpp
const int ANGLE_STEP = 2;        // Degrees per step (1-5)
const int DELAY_TIME = 50;       // ms between readings
const int MIN_ANGLE = 0;         // Start angle
const int MAX_ANGLE = 180;       // End angle
```

### Detection Sensitivity
```cpp
const unsigned long ECHO_TIMEOUT = 30000;  // Microseconds
// Range validation: 2cm - 400cm for HC-SR04
```

## 📈 Technical Specifications

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Detection Range** | 2-400cm | HC-SR04 sensor limits |
| **Angular Resolution** | 1-5° | Configurable step size |
| **Update Rate** | ~20Hz | Depends on sweep speed |
| **Display Refresh** | 20Hz | 50ms intervals |
| **Serial Baud Rate** | 9600 | Arduino ↔ Python |
| **Power Requirements** | 5V/1A | Arduino + servo |

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---
- [ ] **ESP32 WiFi**: Wireless data transmission

---

**⭐ Star this repository if you found it helpful!**

*Built with ❤️ by [Your Name] - Making electronics accessible to everyone*
