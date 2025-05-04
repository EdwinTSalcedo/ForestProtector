from utils.servo import move_servo_to_position

class ServoController:
    async def move_to_position(self, position):
        await move_servo_to_position(position)
