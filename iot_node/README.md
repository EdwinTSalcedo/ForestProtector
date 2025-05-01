<h1 align="center">IoT Sensor Node</h1> 

This directory contains the firmware, hardware design, and assembly documentation for the IoT sensor nodes used in the ForestProtector wildfire monitoring system. These nodes collect environmental data (gas, temperature, humidity, rain) and send it wirelessly to the central gateway via LoRa communication.

<p align='right'><i> Status: Node module validated and field-tested </i></p> 

## Contents  
[1. Components](#components) </br>
[2. Wiring and schematic](#wiring) </br>
[3. Files included](#files) </br>
[4. Physical design and assembly](#design) </br>
[5. Library setup](#libraries) </br>
[6. Firmware behavior](#firmware) </br>
[7. Field deployment considerations](#considerations) </br>
<br>

<a id="components"></a>
## 1. Components

- **TTGO LoRa32 V1.0** – ESP32 microcontroller with built-in SX1276 LoRa module  
- **BME280** – environmental sensor for temperature, humidity, and pressure (I2C)  
- **MQ2** – gas and smoke sensor (analog output)  
- **T1592** – rain sensor (analog output)  
- **3D printed enclosure** – printed in PETG for outdoor resistance  
- **5V power source** – LiPo battery or USB power bank

<a id="wiring"></a>
## 2. Visual schematic

<p align="center">
  <img src="../images/iot_node_schematic.png" width="60%">
</p>

The diagram above illustrates the physical wiring between the TTGO LoRa32 board and the environmental sensors. Note that the LoRa transceiver is integrated into the TTGO board, and its SPI pins must be explicitly set in the firmware. The BME280 communicates over I2C, while the MQ2 and T1592 sensors use analog outputs connected to GPIO36 and GPIO39, respectively. Ensure that sensors requiring 3.3V or 5V are connected accordingly to avoid damage.

<a id="files"></a>
## 3. Files included

- [`iot_node_code.ino`](iot_node_code.ino): Arduino code for the sensor node. It reads data from the sensors and sends it to the T3S3 board at the gateway via LoRa using a structured string array. The code evaluates thresholds for temperature, humidity, and gas levels, and sends only key status indicators. To deploy this firmware, upload it to the TTGO LoRa32 board using the Arduino IDE.

- `cad_files/`: Editable 3D design files created in SolidWorks.  
  - The main part file for customizing the node's structure is [`design1.SLDPRT`](cad_files/design1.SLDPRT).  
  - [`new_roof.SLDPRT`](cad_files/new_roof.SLDPRT) contains an alternative version of the rain shield.  
  - [`iot_node.SLDASM`](cad_files/iot_node.SLDASM) assembles all parts and includes virtual models of the electronic components in their correct positions.

- `3d_printing_files/`: STL files ready for 3D printing.  
  - This folder also includes [`iot_node_all_parts.3mf`](3d_printing_files/iot_node_all_parts.3mf), a pre-arranged printing layout with all parts positioned and oriented for slicing and export.

<a id="design"></a>
## 4. Physical design and assembly

The enclosure was designed in SolidWorks and optimized for 3D printing in PETG, making it suitable for outdoor use. It is shaped to fit securely on top of a standard 4-inch PVC pipe, allowing for easy elevation in the field.

**Recommended 3D printing settings:**
- Material: PETG (offers better UV and humidity resistance than PLA)
- Layer height: 0.2 mm
- Infill: 20–30%

**Assembly steps:**
1. Print both the top and bottom casing parts from the [`3d_printing_files`](../3d_printing_files) folder.
2. Mount the TTGO LoRa32 board inside the main body using built-in supports in the model.
3. Place the MQ2 and rain sensor through the dedicated side cutouts; secure them with hot glue or bolts if needed.
4. Insert the BME280 sensor through the top opening aligned for proper airflow.
5. Connect all sensors according to the [schematic](#wiring).
6. Optionally, apply silicone or weatherproof sealant around joints to improve durability in humid environments.

**Assembly reference:**

<p align="center">
  <img src="../images/iot_node_assembly.png" width="80%">
</p>

<a id="libraries"></a>
## 5. Library setup

This code must be compiled using **Arduino IDE** with the **ESP32 Dev Module** selected.  
Make sure to install the following libraries:

- `LoRa` by Sandeep Mistry
- `Adafruit BME280`
- `Adafruit Unified Sensor`
- `Wire` (built-in)

**Upload settings:**
- Board: ESP32 Dev Module
- Port: USB port where TTGO is connected
- Baud rate: 115200

<a id="firmware"></a>
## 6. Firmware behavior

The node executes the following operations in 5-second intervals:

1. Reads values from the MQ2, BME280, and rain sensors.
2. Maps the MQ2 output to a 0–100 scale.
3. Flags temperature above 50°C and humidity above 45%.
4. Formats the data as:

<a id="considerations"></a>
## 7. Field deployment considerations
