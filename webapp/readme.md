# ForestProtector Web App

## Description

This web app provides real-time visualization, alerting, and data ingestion for the ForestProtector system. It is split into three parts:

- backend: receives IoT sensor data, serves APIs/WebSockets, and sends WhatsApp alerts.
- frontend: displays the live dashboard and alerts.
- microcontrollers:
  - Jetson: runs the edge vision logic and reports detections to the backend.
  - NodeMCU: bridges sensor data to the Jetson.
  - Pi Pico: collects sensor data and sends it over LoRa to the NodeMCU.

## Folder Structure

```bash
.
├── backend # Node.js API + WebSockets + WhatsApp alerts.
├── frontend # React/Vite dashboard.
├── microcontrollers
│   ├── jetson # Python services for Jetson.
│   ├── nodeMCU # Arduino firmware for NodeMCU.
│   └── piPico # MicroPython firmware for Raspberry Pi Pico.
└── readme.md
```

## Backend

### Requirements
- Node.js 18+
- MongoDB (local or hosted)
- pnpm (recommended)

### Setup
```bash
cd webapp/backend
cp .env.example .env
```

Update `.env` with your MongoDB connection and runtime mode:
```
MONGO_URI=...
ENVIRONMENT=development
PORT=3000
```

### Run
```bash
pnpm install
pnpm dev
```

The server starts on `http://localhost:3000` and exposes:
- REST endpoints under `/node/:node` for IoT data ingestion.
- WebSocket updates for live dashboards.
- Swagger docs at `/api-docs`.

## Frontend

### Run
```bash
cd webapp/frontend
pnpm install
pnpm dev
```

The UI starts on the Vite dev server and connects to the backend over HTTP/WebSockets.

## Microcontrollers

Reference implementations are under `webapp/microcontrollers`:
- Jetson Python code: `webapp/microcontrollers/jetson`
- NodeMCU firmware: `webapp/microcontrollers/nodeMCU`
- Pi Pico firmware: `webapp/microcontrollers/piPico`

Each folder contains platform-specific code and requirements.
