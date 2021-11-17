from abc import ABC, ABCMeta, abstractmethod


class Appliance(metaclass=ABCMeta):
    def __init__(self):
        self.is_on = False

    @abstractmethod
    def start(self):
        self.is_on = True
    
    @abstractmethod
    def stop(self):
        self.is_on = False


class AC(Appliance):
    def __init__(self):
        super().__init__()
        self.compressor_on = False
        self.valve_on = False
        self.fans_on = False
        self.hatches_open = False
    
    def start(self):
        self.compressor_on = True
        self.valve_on = True
        self.fans_on = True
        self.hatches_open = True
        super().start()

    def stop(self):
        self.compressor_on = False
        self.valve_on = False
        self.fans_on = False
        self.hatches_open = False
        super().stop()


class Refrigerator(Appliance):
    def __init__(self):
        super().__init__()
        self.evaporator_on = False
        self.valve_on = False
        self.pump_on = False
    
    def start(self):
        self.evaporator_on = True
        self.valve_on = True
        self.pump_on = True
        print('*Humming starts*')
        super().start()

    def stop(self):
        self.evaporator_on = False
        self.valve_on = False
        self.pump_on = False
        print('*Humming stops*')
        super().stop()


class Fan(Appliance):
    def __init__(self):
        super().__init__()
        self.blades_speed = 0
    
    def start(self):
        self.blades_speed = 3
        super().start()

    def stop(self):
        self.blades_speed = 0
        super().stop()

    
class TV(Appliance):
    def __init__(self):
        super().__init__()
        self.display_on = False
        self.indicator_state = False
    
    def start(self):
        self.display_on = True
        self.indicator_state = True
        super().start()

    def stop(self):
        self.display_on = False
        self.indicator_state = False
        super().stop()


class GateOpener(Appliance):
    def __init__(self):
        super().__init__()
        self.left_gate_angle = 0
        self.right_gate_angle = 0
    
    def start(self):
        while self.left_gate_angle <= 90:
            self.left_gate_angle += 5
        print('*Left gate hits the frame*')
        while self.right_gate_angle <= 90:
            self.right_gate_angle += 5
        print('*Right gate hits the frame*')
        super().start()

    def stop(self):
        while self.left_gate_angle >= 0:
            self.left_gate_angle -= 5
        while self.right_gate_angle >= 0:
            self.right_gate_angle -= 5
        print('*Left and right gates hit each other*')
        super().stop()


class Switch(metaclass=ABCMeta):
    def __init__(self, appliance: Appliance):
        self.appliance = appliance
    
    def turn_on(self):
        self.appliance.start()

    def turn_off(self):
        self.appliance.stop()


class AutomaticRemoteController(Switch):
    def __init__(self, appliance: Appliance):
        super().__init__(appliance)
        self.possible_tasks = {
            'on': self.turn_on,
            'off': self.turn_off
        }
        self.task_list = []
    
    def add_task(self, task: str):
        if task in self.possible_tasks:
            self.task_list.append(self.possible_tasks[task])
    
    def perform_tasks(self):
        for i in range(len(self.task_list)):
            self.task_list[i]()
        
        self.task_list = []


class ManualRemoteController(Switch):
    def __init__(self, appliance: Appliance):
        super().__init__(appliance)
        self.buttons = {
            'on': self.turn_on,
            'off': self.turn_off
        }
    
    def press_button(self, button: str):
        if button in self.buttons:
            self.buttons[button]()


refrigerator = Refrigerator()
gate_opener = GateOpener()

manual_remote = ManualRemoteController(refrigerator)
automatic_remote = AutomaticRemoteController(gate_opener)

print('\n Refrigerator:')
manual_remote.press_button('on')
manual_remote.press_button('off')
manual_remote.press_button('on')
manual_remote.press_button('off')

print('\n Gate Opener:')
automatic_remote.add_task('on')
automatic_remote.add_task('off')
automatic_remote.perform_tasks()