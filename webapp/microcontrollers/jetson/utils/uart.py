import random
import asyncio

async def read_uart_data():
    # TODO: Implement UART data reading
    while True:
        # Mock random UART data
        data = {
            "co2": random.randint(300, 600),
            "temperature": random.uniform(15, 30),
            "humidity": random.uniform(30, 70),
            "pressure": random.uniform(900, 1100),
            "sound": bool(random.choice([0, 1])),
            "smoke": bool(random.choice([0, 1])),
            "node": random.randint(1, 10),
        }
        await asyncio.sleep(1)  # Mock reading interval
        yield data
