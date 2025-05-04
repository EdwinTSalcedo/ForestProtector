# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Variables to show

| # | Variable    | Range               |
|---|-------------|---------------------|
| 1 | CO2         | 0 to 1023 ppm       |
| 2 | Temperature | -40 °C to 85 °C     |
| 3 | Humidity    | 0% to 100% RH       |
| 4 | Pressure    | 300 hPa to 1100 hPa |
| 5 | Sound       | true or false       |
| 6 | Smoke       | true or false       |

I need a node code that send a post request to a server 'http://localhost:3000/:node' with the variables above. Every 30 seconds the variables change randomly and a new post request should be sent.
Also send node number between 1 and 9.