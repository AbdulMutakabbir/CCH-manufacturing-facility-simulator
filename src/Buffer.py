# holds the data and methods for Buffer class
class Buffer:
    is_empty: bool = None
    is_full: bool = None
    __priority: int = None
    __queue: list = None
    __queue_limit: int = 2
    _capacity: int = None

    # Constructor:
    # Inputs:
    #       priority:int -> buffers priority: Higher the value higher the priority
    def __init__(self, priority:int):
        if (priority is not None) and (priority >= 0) and (priority <= 3):
            self.__priority = priority
        else:
            raise Exception("BufferPriorityError")

        # init class variables
        self.is_empty = True
        self.is_full = False
        self._capacity = 0
        self.__queue = []

    # returns buffers capacity
    def get_capacity(self):
        if self._capacity is None:
            raise Exception("NotInitializedComponent")
        else:
            return self._capacity

    # performs the actions for inserting component into a buffer
    def insert_component(self, component):
        if self.is_empty is None or self.is_full is None or self.__priority is None or self.__queue is None:
            raise Exception("BufferNotInitialized")
        else:
            if not self.is_full:
                self.__queue.append(component)
                self._capacity = len(self.__queue)
                self.is_empty = False
                if len(self.__queue) >= 2:
                    self.is_full = True
                return True
            else:
                return False

    # performs the actions for removing component from buffer
    def send_component(self):
        if self.is_empty is None or self.is_full is None or self.__priority is None or self.__queue is None:
            raise Exception("BufferNotInitialized")
        else:
            if not self.is_empty:
                component = self.__queue.pop(0)
                self._capacity -= 1
                if len(self.__queue) <= 0:
                    self.is_empty = True
                return True, component
            else:
                return False, None
