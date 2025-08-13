import serial
import serial.tools.list_ports
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from collections import deque
import sys
import math

class UltrasonicRadarReader:
    def __init__(self, port=None, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self.is_reading = False
        self.data_lock = threading.Lock()
        
        # Data storage
        self.angles = deque(maxlen=1000)
        self.distances = deque(maxlen=1000)
        self.timestamps = deque(maxlen=1000)
        
        # Current state
        self.current_angle = 0
        self.current_distance = 0
        self.current_direction = "Unknown"
        
        # Detection points (objects within 30cm)
        self.detection_points_x = deque(maxlen=500)  # Store detection coordinates
        self.detection_points_y = deque(maxlen=500)
        self.detection_ages = deque(maxlen=500)      # Age of each detection for fading
        
        # Statistics
        self.total_readings = 0
        self.invalid_readings = 0
        
    def list_available_ports(self):
        """List all available serial ports"""
        ports = serial.tools.list_ports.comports()
        print("Available Serial Ports:")
        for i, port in enumerate(ports):
            print(f"{i+1}. {port.device} - {port.description}")
        return [port.device for port in ports]
    
    def auto_detect_arduino(self):
        """Try to automatically detect Arduino port"""
        ports = serial.tools.list_ports.comports()
        arduino_keywords = ['Arduino', 'CH340', 'USB Serial', 'ttyACM', 'ttyUSB']
        
        for port in ports:
            for keyword in arduino_keywords:
                if keyword.lower() in port.description.lower():
                    print(f"Potential Arduino found: {port.device} - {port.description}")
                    return port.device
        return None
    
    def connect(self, port=None):
        """Connect to the Arduino"""
        if port:
            self.port = port
        elif not self.port:
            detected_port = self.auto_detect_arduino()
            if detected_port:
                self.port = detected_port
            else:
                available_ports = self.list_available_ports()
                if not available_ports:
                    print("No serial ports found!")
                    return False
                
                try:
                    choice = input("Enter port number or full port name: ")
                    if choice.isdigit():
                        port_index = int(choice) - 1
                        if 0 <= port_index < len(available_ports):
                            self.port = available_ports[port_index]
                        else:
                            print("Invalid port number!")
                            return False
                    else:
                        self.port = choice
                except KeyboardInterrupt:
                    return False
        
        try:
            print(f"Connecting to {self.port} at {self.baudrate} baud...")
            self.serial_connection = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)
            self.serial_connection.flushInput()
            print(f"Successfully connected to {self.port}")
            return True
            
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from Arduino"""
        self.stop_reading()
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Disconnected from Arduino")
    
    def parse_data_line(self, line):
        """Parse a line of data from Arduino"""
        line = line.strip()
        
        if line.startswith('#') or not line:
            if "Direction:" in line:
                self.current_direction = line.split("Direction:")[-1].strip()
            return None
        
        try:
            parts = line.split(',')
            if len(parts) != 2:
                return None
            
            angle = float(parts[0])
            
            if parts[1].strip() == "OUT_OF_RANGE":
                distance = -1.0
            else:
                distance = float(parts[1])
            
            return angle, distance
            
        except ValueError:
            return None
    
    def start_reading(self):
        """Start reading data in a separate thread"""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Not connected to Arduino!")
            return False
        
        self.is_reading = True
        self.reading_thread = threading.Thread(target=self._read_data)
        self.reading_thread.daemon = True
        self.reading_thread.start()
        print("Started reading data from Arduino...")
        return True
    
    def stop_reading(self):
        """Stop reading data"""
        self.is_reading = False
        if hasattr(self, 'reading_thread'):
            self.reading_thread.join(timeout=2)
    
    def _read_data(self):
        """Internal method to read data continuously"""
        while self.is_reading:
            try:
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8', errors='ignore')
                    parsed_data = self.parse_data_line(line)
                    
                    if parsed_data:
                        angle, distance = parsed_data
                        current_time = time.time()
                        
                        with self.data_lock:
                            self.angles.append(angle)
                            self.distances.append(distance)
                            self.timestamps.append(current_time)
                            self.current_angle = angle
                            self.current_distance = distance
                            self.total_readings += 1
                            
                            if distance < 0:
                                self.invalid_readings += 1
                            elif distance <= 30.0:  # Object detected within 30cm
                                self._add_detection_point(angle, distance, current_time)
                
                else:
                    time.sleep(0.01)
                    
            except serial.SerialException as e:
                print(f"Serial reading error: {e}")
                break
            except KeyboardInterrupt:
                break
    
    def _add_detection_point(self, angle, distance, timestamp):
        """Add a detection point and convert to cartesian coordinates"""
        # Convert angle from degrees to radians
        angle_rad = math.radians(angle)
        
        # Convert distance from cm to graph units (5 units = 30cm)
        distance_units = (distance / 30.0) * 5.0
        
        # Convert to cartesian coordinates
        x = distance_units * math.cos(angle_rad)
        y = distance_units * math.sin(angle_rad)
        
        self.detection_points_x.append(x)
        self.detection_points_y.append(y)
        self.detection_ages.append(timestamp)
    
    def get_servo_position(self):
        """Get current servo position in cartesian coordinates"""
        with self.data_lock:
            angle_rad = math.radians(self.current_angle)
            # Servo line extends to full radius (5 units)
            x = 5.0 * math.cos(angle_rad)
            y = 5.0 * math.sin(angle_rad)
            return x, y, self.current_angle
    
    def get_detection_points(self, max_age=10.0):
        """Get detection points, removing old ones"""
        current_time = time.time()
        
        with self.data_lock:
            # Filter out old detections
            valid_x = []
            valid_y = []
            valid_ages = []
            
            for i, age in enumerate(self.detection_ages):
                if current_time - age <= max_age:
                    valid_x.append(self.detection_points_x[i])
                    valid_y.append(self.detection_points_y[i])
                    valid_ages.append(current_time - age)
            
            return valid_x, valid_y, valid_ages

class RadarDisplay:
    def __init__(self, radar_reader):
        self.radar_reader = radar_reader
        
        # Setup matplotlib
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-1, 6)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_facecolor('black')
        
        # Labels and title
        self.ax.set_xlabel('X (Distance Units)', color='white')
        self.ax.set_ylabel('Y (Distance Units)', color='white')
        self.ax.set_title('Live Ultrasonic Radar Display\n5 Units = 30cm Range', color='white', fontsize=14)
        
        # Draw coordinate axes
        self.ax.axhline(y=0, color='white', linewidth=1, alpha=0.7)
        self.ax.axvline(x=0, color='white', linewidth=1, alpha=0.7)
        
        # Draw semicircle (detection range)
        theta_semicircle = np.linspace(0, np.pi, 100)
        x_semicircle = 5 * np.cos(theta_semicircle)
        y_semicircle = 5 * np.sin(theta_semicircle)
        self.ax.plot(x_semicircle, y_semicircle, 'green', linewidth=2, alpha=0.8, label='30cm Range')
        
        # Draw range rings
        for radius in [1, 2, 3, 4]:
            theta_ring = np.linspace(0, np.pi, 50)
            x_ring = radius * np.cos(theta_ring)
            y_ring = radius * np.sin(theta_ring)
            distance_cm = (radius / 5.0) * 30
            self.ax.plot(x_ring, y_ring, 'gray', linewidth=1, alpha=0.4)
            self.ax.text(radius, 0.1, f'{distance_cm:.0f}cm', color='gray', fontsize=8, ha='center')
        
        # Initialize plot elements
        self.servo_line, = self.ax.plot([], [], 'red', linewidth=3, label='Servo Position')
        self.servo_point, = self.ax.plot([], [], 'ro', markersize=8)
        self.detection_scatter = self.ax.scatter([], [], c=[], s=[], cmap='plasma', alpha=0.8, label='Detections')
        
        # Status text
        self.status_text = self.ax.text(0.02, 0.98, '', transform=self.ax.transAxes, 
                                       verticalalignment='top', color='white', fontsize=10,
                                       bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        # Legend
        self.ax.legend(loc='upper right', facecolor='black', edgecolor='white')
        
        # Set colors for dark theme
        self.fig.patch.set_facecolor('black')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.tick_params(colors='white')
        
    def update_plot(self, frame):
        """Update the radar display"""
        # Get servo position
        servo_x, servo_y, servo_angle = self.radar_reader.get_servo_position()
        
        # Update servo line
        self.servo_line.set_data([0, servo_x], [0, servo_y])
        self.servo_point.set_data([servo_x], [servo_y])
        
        # Get detection points
        det_x, det_y, det_ages = self.radar_reader.get_detection_points(max_age=15.0)
        
        if det_x and det_y:
            # Create colors and sizes based on age (newer = brighter/larger)
            colors = [1.0 - (age / 15.0) for age in det_ages]  # Newer = closer to 1
            sizes = [100 * (1.0 - (age / 15.0)) + 20 for age in det_ages]  # Newer = larger
            
            # Update scatter plot
            self.detection_scatter.set_offsets(np.column_stack([det_x, det_y]))
            self.detection_scatter.set_array(np.array(colors))
            self.detection_scatter.set_sizes(sizes)
        else:
            # Clear scatter plot if no detections
            self.detection_scatter.set_offsets(np.empty((0, 2)))
            self.detection_scatter.set_array(np.array([]))
            self.detection_scatter.set_sizes([])
        
        # Update status text
        with self.radar_reader.data_lock:
            total = self.radar_reader.total_readings
            invalid = self.radar_reader.invalid_readings
            direction = self.radar_reader.current_direction
            distance = self.radar_reader.current_distance
        
        status_str = f"Angle: {servo_angle:.1f}°\n"
        status_str += f"Distance: {distance:.1f}cm\n" if distance >= 0 else "Distance: OUT OF RANGE\n"
        status_str += f"Direction: {direction}\n"
        status_str += f"Total Readings: {total}\n"
        status_str += f"Valid: {total - invalid} | Invalid: {invalid}\n"
        status_str += f"Detections: {len(det_x)}"
        
        self.status_text.set_text(status_str)
        
        return self.servo_line, self.servo_point, self.detection_scatter, self.status_text
    
    def start_animation(self, interval=50):
        """Start the live animation"""
        self.animation = animation.FuncAnimation(
            self.fig, self.update_plot, interval=interval, blit=True, cache_frame_data=False
        )
        plt.show()

def main():
    """Main function"""
    radar = UltrasonicRadarReader()
    
    try:
        # Connect to Arduino
        if not radar.connect():
            print("Failed to connect to Arduino")
            return
        
        # Start reading data
        if not radar.start_reading():
            print("Failed to start reading data")
            return
        
        print("\nStarting live radar display...")
        print("- Green circle: 30cm detection range")
        print("- Red line: Current servo position")
        print("- Colored dots: Detected objects (brighter = newer)")
        print("- Press Ctrl+C or close window to stop")
        
        # Wait a moment for initial data
        time.sleep(3)
        
        # Create and start the radar display
        display = RadarDisplay(radar)
        display.start_animation(interval=50)  # Update every 50ms
        
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        radar.disconnect()
        print("Program ended")

if __name__ == "__main__":
    # Check required packages
    try:
        import serial
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        print(f"Missing required package: {e}")
        print("Install with: pip install pyserial matplotlib numpy")
        sys.exit(1)
    
    main()