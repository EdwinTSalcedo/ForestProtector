import aiohttp
from utils.uart import read_uart_data
from config import Config

async def uart_reader(state_machine):
    config = Config()
    async with aiohttp.ClientSession() as session:
        async for data in read_uart_data():
            print(f"Received UART data: {data}")
            node = data["node"] # This is extracted to send it as path parameter
            del data["node"]
            # Send data to endpoint
            async with session.post(config.endpoint_url + f"/node/{node}", json=data) as resp:
                print(f"Sent data, status: {resp.status}")

            # TODO: Send to reinforced model in standby mode
            # state_machine = modelResult(data)
