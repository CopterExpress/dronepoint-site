from collections import deque
from typing import Callable

class PrintObserver:
    def __init__(self) -> None:
        self._messages = deque(maxlen=1000)
        self._handler = lambda x: x
    
    def get_messages(self):
        return list(self._messages)
    
    def subscribe_handler(self, func: Callable):
        self._handler = func
    
    def unsubscribe_handler(self):
        self._handler = lambda x: x
    
    def write(self, message: str):
        print(message)
        self._messages.append(message)
        self._handler(self.get_messages())

observer = PrintObserver()