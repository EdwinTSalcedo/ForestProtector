#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// LoRa module pins
#define SCK 5
#define MISO 19
#define MOSI 27
#define SS 18
#define RST 14
#define DIO0 26

// LoRa frequency (915E6 for America)
#define BAND 915E6

// Sensor pins
#define MQ2_PIN 36        // MQ2 gas sensor connected to GPIO 36
#define RAIN_SENSOR_PIN 39 // Rain sensor connected to GPIO 39

// BME280 configuration
#define BME280_ADDRESS 0x76 // Adjust if needed

// Variables
Adafruit_BME280 bme;
int mq2ValueMapped;

void setup() {
  Serial.begin(115200);

  // Initialize sensor pins
  pinMode(MQ2_PIN, INPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT);

  // Initialize BME280
  if (!bme.begin(BME280_ADDRESS)) {
    Serial.println("Failed to initialize BME280 sensor.");
    while (1);
  }

  // Initialize LoRa
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }

  Serial.println("LoRa transmitter successfully started!");
}

void loop() {
  // Read sensors
  int mq2Digital = digitalRead(MQ2_PIN);
  mq2ValueMapped = (mq2Digital == 0) ? 1 : 0;

  int rainValue = analogRead(RAIN_SENSOR_PIN);
  float temperature = bme.readTemperature();
  float humidity = bme.readHumidity();
  float pressure = bme.readPressure() / 100.0F; // Convert to hPa

  // Create data string
  String dataToSend = "1:" + String(mq2ValueMapped) + "," + 
                      String(rainValue) + "," + 
                      String(temperature) + "," + 
                      String(humidity) + "," + 
                      String(pressure);

  // Send data via LoRa
  LoRa.beginPacket();
  LoRa.print(dataToSend);
  LoRa.endPacket();

  // Print to serial monitor
  Serial.print("Data sent: ");
  Serial.println(dataToSend);

  delay(5000); // Wait 5 seconds before sending again
}
