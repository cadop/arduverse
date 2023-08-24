#include "MadgwickAHRS.h"
#include <Arduino_LSM6DSOX.h>
#include <WiFiNINA.h>


// Code modified from:
// https://stackoverflow.com/questions/64998271/arduino-imu-attempt-errors-lagging-drifting

// initialize a Madgwick filter:
Madgwick filter;

// UDP Connection info
char ssid[] = "WIFIName";
char pass[] = "secretpassword";
int status = WL_IDLE_STATUS;
WiFiUDP Udp;

// Change which port to use for each device
unsigned int localPort = 8882;
String deviceID = "2";

float beta = 0.1;  // Madgwick filter parameter
float q1 = 1, q2 = 0, q3 = 0, q4 = 0;  // Quaternion elements

// sensor's sample rate is fixed at 104 Hz:
const float sensorRate = 104.00;

float sax, say, saz, sgx, sgy, sgz;

void setup() {
  Serial.begin(9600);
  // attempt to start the IMU:
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU");
    // stop here if you can't access the IMU:
    while (true);
  }

  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to WPA SSID: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid, pass);
    delay(5000);
  }
  Serial.println("Connected to WiFi");
  Serial.print("Arduino IP address: ");
  Serial.println(WiFi.localIP());

  Udp.begin(localPort);
  // start the filter to run at the sample rate:
  filter.begin(sensorRate);
}

long nz = 0;
float x = 0, y = 0, z = 0;

void loop() {
  // values for acceleration and rotation:
  float xAcc, yAcc, zAcc;
  float xGyro, yGyro, zGyro;

  // values for orientation:
  float roll, pitch, heading;
  // check if the IMU is ready to read:
  if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) 
  {
    // read accelerometer &and gyrometer:
    IMU.readAcceleration(xAcc, yAcc, zAcc);
    IMU.readGyroscope(xGyro, yGyro, zGyro);

    //initial calibration time
    nz++;
    if (nz < 500)   
    {
      sgz += zGyro;
      sgx += xGyro;
      sgy += yGyro;
      x = sgx / nz;
      y = sgy / nz;
      z = sgz / nz;
    }

    // update the filter, which computes orientation:
    filter.updateIMU(xGyro - x, yGyro - y, zGyro - z, xAcc, yAcc, zAcc);

    roll = filter.getRoll();
    pitch = filter.getPitch();
    heading = filter.getYaw();
       
    String data = deviceID + "," + String(roll) + "," + String(pitch) + "," + String(heading);
    Serial.println(data);
    // Send to the computer
    Udp.beginPacket("192.168.1.2", localPort);
    Udp.write(data.c_str());
    Udp.endPacket();
    
  }
  
}
