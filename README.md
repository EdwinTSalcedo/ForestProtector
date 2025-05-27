<h1 align="center">ForestProtector: An IoT Architecture Integrating Machine Vision and Deep Reinforcement Learning for Efficient Wildfire Monitoring</h1> 

This repository contains supplementary material for the conference paper [*"ForestProtector: An IoT Architecture Integrating Machine Vision and Deep Reinforcement Learning for Efficient Wildfire Monitoring"*](https://arxiv.org/abs/2501.09926) (ICARA 2025 Oral session). **Authors:** [Kenneth Bonilla-Ormachea](https://www.linkedin.com/in/kenneth-bonilla-ormachea-58b7a9240/), [Horacio Cuizaga](https://www.linkedin.com/in/horacuizr/), [Edwin Salcedo](https://www.linkedin.com/in/edwinsalcedo), [Sebastian Castro](https://www.linkedin.com/in/sebastian-castro-3969641a6), [Sergio Fernandez-Testa](https://www.linkedin.com/in/sergio5919/), and [Misael Mamani](https://www.linkedin.com/in/misaelmq680/).  

[[Project page]](https://edwinsalcedo.com/publication/forest-protector) [[arXiv]](https://arxiv.org/abs/2501.09926) 

<p align="center">
<img src="images/insitu-validation1.png" width="80%">
</p>

<p align='right'><i>  Status: Repo Under Construction  </i></p> 

## Contents
[1. Overview](#overview) </br>
* [Motivation](#motivation) </br>
* [IoT architecture](#iotarchitecture) </br>
* [Hardware prototype](#hardwareprototype) </br>

<!-- [2. Computer vision system](#cvsystem) </br>
* [Data collection](#datacollection) </br>
* [Computer vision pipeline](#cvpipeline) </br>
* [3DCNN](#3dcnn) </br>

[3. Deep reinforcement learning agent](#drlagent) </br>

[4. Validation](#validation) </br>

[5. Getting started](#gettingstarted) </br>
* [Initial inference samples](#initialinference) </br>
* [Graphical user interface (GUI)](#gui) </br>
* [On-device deployment](#deployment) </br> -->

[2. Citation](#citation) </br>
<br>

<a id="overview"></a> 
## 1. Overview

<a id="motivation"></a> 
### Motivation

Early detection of forest fires is crucial to minimising environmental and socioeconomic damage, as longer-burning fires are significantly harder and costlier to extinguish. However, current detection systems using technologies like remote sensing, PTZ cameras, and UAVs are often expensive and require human involvement, limiting their practicality for continuous large-scale monitoring. To address this, we propose a system that uses a low-cost central gateway with computer vision to monitor a 360° field of view for smoke at long distances. A deep reinforcement learning agent enhances surveillance by dynamically adjusting the camera's orientation based on real-time data from distributed IoT sensors measuring smoke, temperature, and humidity.

<a id="iotarchitecture"></a> 
### IoT architecture
The proposed system architecture consists of two main components: IoT sensor nodes and a central gateway. The sensor nodes, deployed near forests, monitor environmental conditions using various sensors, including those for temperature, humidity, barometric pressure, smoke and water. The central gateway, based on a NVIDIA Jetson Nano card, collects data from these nodes via the LoRa protocol. The gateway then utilizes a DRL agent to control the gateway camera's perspective, focusing on potential nearby campfires, and employs a computer vision algorithm to verify the presence of smoke in the high-risk region. 

<p align="center">
<img src="images/iot-architecture.jpg" width="80%">
</p>

<a id="hardwareprototype"></a> 
### Hardware prototype

We designed custom enclosures for the IoT nodes and gateway using SolidWorks and 3D-printed them with PETG (Polyethylene Terephthalate Glycol) material. The hardware implementation details for both modules are provided below:

|  <a href="https://github.com/EdwinTSalcedo/ForestProtector/tree/main/iot_node">IoT Node Documentation</a>  |  <a href="https://github.com/EdwinTSalcedo/ForestProtector/tree/main/gateway">Gateway Documentation</a> |   
|---|---|
|<a href="https://github.com/EdwinTSalcedo/ForestProtector/tree/main/iot_node"><img src="images/iotdevice.jpg" width="250px"/></a> | <a href="https://github.com/EdwinTSalcedo/ForestProtector/tree/main/gateway"><img src="images/gateway.jpg"  width="250px"/></a> |  

<!-- <a id="cvsystem"></a>
## 2. Computer vision system

<a id="datacollection"></a> 
### Data collection 

<a id="cvpipeline"></a> 
### Computer vision pipeline

<a id="3dcnn"></a> 
### 3DCNN

<a id="dlragent"></a>
## 3. Deep reinforcement learning agent

<a id="validation"></a> 
## 4. Validation 

<a id="gettingstarted"></a>
## 5. Getting started

<a id="initialinference"></a> 
### Initial inference samples

<a id="gui"></a> 
### Graphical User Interface (GUI)

<a id="deployment"></a> 
### On-device deployment -->


<a id="citation"></a>
## 2. Citation

If you find *ForestProtector* useful in your project, please consider citing the following paper:

```
@INPROCEEDINGS{bonilla2025,
  author={Bonilla-Ormachea, Kenneth and Cuizaga, Horacio and Salcedo, Edwin and Castro, Sebastian and Fernandez-Testa, Sergio and Mamani, Misael},
  booktitle={2025 11th International Conference on Automation, Robotics, and Applications (ICARA)}, 
  title={ForestProtector: An IoT Architecture Integrating Machine Vision and Deep Reinforcement Learning for Efficient Wildfire Monitoring}, 
  year={2025},
  volume={},
  number={},
  pages={70-75},
  doi={10.1109/ICARA64554.2025.10977677}}
```
