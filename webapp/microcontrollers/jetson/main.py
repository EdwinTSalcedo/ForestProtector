import asyncio
from tasks.state_machine import StateMachine
from tasks.uart_handler import uart_reader
from tasks.smoke_detection import smoke_detector
from tasks.servo_control import ServoController
from config import Config

async def main():
    # Initialize state machine, servo, and other tasks
    state_machine = StateMachine()
    servo_controller = ServoController()

    # Start UART handler and state machine in parallel
    await asyncio.gather(
        uart_reader(state_machine),  # UART data handling
        state_machine.run(servo_controller),  # State machine control
        smoke_detector(state_machine),  # Smoke detection handling
    )

if __name__ == "__main__":
    config = Config()
    asyncio.run(main())
