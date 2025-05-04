import asyncio
from utils.models import get_reinforced_model_result
from utils.servo import move_servo_to_position, move_servo_back_n_forth
import time

class StateMachine:
    scanning_w_movement = False
    __state = None
    result = 0
    
    @property
    def state(self):
        return self.__state
    
    @state.setter
    def state(self, value):
        print(f"State changed from {self.__state} to {value}")
        self.startTime = time.time()
        self.__state = value
    
    def __init__(self):
        self.state = "Standby"
        self.goto_position = None

    async def run(self, servo_controller):
        while True:
            if self.state == "Standby":
                await self.handle_standby(servo_controller)
            elif self.state == "Scanning":
                await self.handle_scanning()
            elif self.state == "GoTo":
                await self.handle_goto(servo_controller)
            await asyncio.sleep(1)

    async def handle_standby(self, servo_controller):
        # TODO: Implement data reception and call reinforced model
        
        # Every 15 minutes, scan with movement
        if time.time() - self.startTime > 900:
            self.scanning_w_movement = True
            self.state = "Scanning"
        else:
            self.scanning_w_movement = False
        
        if self.result != 0:
            self.state = "GoTo"
            self.goto_position = result

    async def handle_scanning(self):
        print("Scanning...")
        if self.scanning_w_movement:
            await move_servo_back_n_forth() # 0º to 180º and back
            # After 3 minutes, stop scanning with movement
            if time.time() - self.startTime > 180:
                self.scanning_w_movement = False
                self.state = "Standby"
        else:
            # After 2 minute, stop scanning without movement
            if time.time() - self.startTime > 120:
                self.state = "Standby"
        await asyncio.sleep(1)  # Mock scanning

    async def handle_goto(self, servo_controller):
        print(f"GoTo position: {self.goto_position}")
        await move_servo_to_position(self.goto_position)
        self.state = "Scanning"
        self.scanning_w_movement = False
