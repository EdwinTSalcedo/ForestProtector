#include <LoRa.h>

// LoRa pins for the T3S3
#define SCK 5
#define MISO 3
#define MOSI 6
#define SS 7
#define RST 8
#define DIO0 33

#define BAND 915E6  // LoRa operating frequency (915 MHz)

// Structure to store data from each node
struct NodeData {
  int mq2Value;
  int rainValue;
  int temperature; // 0 or 1 based on threshold
  int humidity;    // 0 or 1 based on threshold
  unsigned long lastUpdate;
};

// Node instances
NodeData node1 = {0, 0, 0, 0, 0};
NodeData node2 = {0, 0, 0, 0, 0};
NodeData node3 = {0, 0, 0, 0, 0};

// Interval to display data on serial monitor (milliseconds)
const unsigned long displayInterval = 5000;
unsigned long lastDisplayTime = 0;

void setup() {
  Serial.begin(115200);

  // Initialize LoRa
  SPI.begin(SCK, MISO, MOSI, SS);
  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(BAND)) {
    Serial.println("LoRa initialization failed.");
    while (1);
  }
}

void loop() {
  // Check if there are incoming packets
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedData = "";
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    processReceivedData(receivedData);
  }

  // Display data periodically
  if (millis() - lastDisplayTime >= displayInterval) {
    lastDisplayTime = millis();
    displayNodeData();
  }
}

// Process received data and assign it to the correct node
void processReceivedData(String receivedData) {
  int nodeId = receivedData.substring(0, 1).toInt();
  String data = receivedData.substring(2);  // Rest of the message

  // Split values by comma
  String values[5];
  int index = 0;
  while (data.length() > 0 && index < 5) {
    int pos = data.indexOf(",");
    if (pos == -1) {
      values[index++] = data;
      break;
    }
    values[index++] = data.substring(0, pos);
    data = data.substring(pos + 1);
  }

  // Assign values to the correct node
  NodeData* node = nullptr;
  if (nodeId == 1) node = &node1;
  else if (nodeId == 2) node = &node2;
  else if (nodeId == 3) node = &node3;
  else {
    Serial.println("Unrecognized node.");
    return;
  }

  if (node) {
    node->mq2Value = mapValue(values[0].toInt(), 0, 4095, 0, 100);  // MQ2 mapping
    node->rainValue = values[1].toInt();                             // Rain sensor value
    node->temperature = values[2].toFloat() > 50 ? 1 : 0;            // Temperature threshold
    node->humidity = values[3].toFloat() > 45 ? 1 : 0;               // Humidity threshold
    node->lastUpdate = millis();                                     // Update timestamp
  }
}

// Maps a value from one range to another
int mapValue(float value, float minIn, float maxIn, int minOut, int maxOut) {
  return (int)((value - minIn) * (maxOut - minOut) / (maxIn - minIn) + minOut);
}

// Display data of all nodes on the serial monitor
void displayNodeData() {
  Serial.print("Node1,");
  printNodeData(node1);
  Serial.print("Node2,");
  printNodeData(node2);
  Serial.print("Node3,");
  printNodeData(node3);
}

// Prints the data of a single node
void printNodeData(NodeData node) {
  if (millis() - node.lastUpdate > displayInterval * 2) {
    Serial.println("No recent data received.");
    return;
  }

  Serial.print(node.mq2Value);
  Serial.print(",");
  Serial.print(node.temperature);
  Serial.print(",");
  Serial.println(node.humidity);
}
