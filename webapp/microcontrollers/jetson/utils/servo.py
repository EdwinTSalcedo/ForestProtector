import asyncio

async def move_servo_to_position(position):
    # TODO: Implement servo motor control here
    print(f"Moving servo to position {position}")
    # Simulate movement
    await asyncio.sleep(2)  # Mock servo delay

async def move_servo_back_n_forth():
    await move_servo_to_position(0)
    await move_servo_to_position(180)
    await move_servo_to_position(0)