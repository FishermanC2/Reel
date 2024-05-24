from queue import Queue

class CommandManager:
    def __init__(self) -> None:
        self.command_queue = Queue()

    def put_new_command(self, command: str):
        self.command_queue.put(command, block=True)

    def get_new_command(self):
        self.command_queue.get(block=True)

    def __str__(self):
        curr_approx_size = self.command_queue.qsize()
        max_size = self.command_queue.maxsize
        return f"Current approx. queue command queue size: {curr_approx_size}.\n Queue max size: {max_size}."
        