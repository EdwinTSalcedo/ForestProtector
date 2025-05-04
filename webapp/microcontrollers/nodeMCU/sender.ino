void setup() {
  Serial.begin(9600);  // Start UART communication at 9600 baud rate
}

void loop() {
  // Simulate sending sensor data
  int sensorData = analogRead(A0);  // Read sensor data (Change by LoRa real data)
  "{'smoke': ... , 'temperature': ... , 'humidity': ...}"
  Serial.println(sensorData);  // Send data over UART
  delay(1000);  // Send data every second
}
