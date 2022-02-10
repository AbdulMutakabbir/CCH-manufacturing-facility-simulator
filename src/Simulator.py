import pandas as pd
from random import random
import os
import enum
from Component import Component
from Inspector import Inspector
from Buffer import Buffer
from Workstation import Workstation


# This class acts as the future event list
class FEL:
    __queue = None  # queue

    # constructor
    def __init__(self):
        self.__queue = {}

    # adds events to FEL
    def put_event(self, event, time):
        if time not in self.__queue:
            self.__queue[time] = []
        self.__queue[time].append(event)

    # retrieve event list by time
    def get_events(self, time) -> list:
        if time not in self.__queue:
            return []
        else:
            return self.__queue[time]

    # prints FEL
    def print(self):
        print(self.__queue)


# Enumerated class to hold event types
class EventType(enum.Enum):
    arrival = 0
    departure = 1
    delay = 2


# Enumerated class to hold on which item the event occurred
class ItemType(enum.Enum):
    component = 0
    product = 0


# Class that holds the simulation environment and runs the main simulation code
class Simulator:
    __inspectors = []  # list of inspectors
    __buffers = []  # list of buffers
    __workstations = []   # list of workstations
    sys_clock = 0   # system clock

    # dataset file locations
    base_path = os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + "dataset" + os.sep
    WS1_TIME_DATA_FILE = base_path + "ws1.dat"
    WS2_TIME_DATA_FILE = base_path + "ws2.dat"
    WS3_TIME_DATA_FILE = base_path + "ws3.dat"
    I11_TIME_DATA_FIlE = base_path + "servinsp1.dat"
    I22_TIME_DATA_FIlE = base_path + "servinsp22.dat"
    I23_TIME_DATA_FIlE = base_path + "servinsp23.dat"

    # Future Event List Object
    FEL = FEL()

    # Constructor
    def __init__(self):
        self.sys_clock = 0

        # init dataset queues
        self.I11_queue = self.__get_list_from_file(self.I11_TIME_DATA_FIlE)
        self.I22_queue = self.__get_list_from_file(self.I22_TIME_DATA_FIlE)
        self.I23_queue = self.__get_list_from_file(self.I23_TIME_DATA_FIlE)
        self.WS1_queue = self.__get_list_from_file(self.WS1_TIME_DATA_FILE)
        self.WS2_queue = self.__get_list_from_file(self.WS2_TIME_DATA_FILE)
        self.WS3_queue = self.__get_list_from_file(self.WS3_TIME_DATA_FILE)

        # init inspectors
        i1 = Inspector(type=1)
        i2 = Inspector(type=2)
        self.__inspectors.append(i1)
        self.__inspectors.append(i2)

        # init buffers
        b1 = Buffer(priority=3)
        b2 = Buffer(priority=2)
        b3 = Buffer(priority=2)
        b4 = Buffer(priority=1)
        b5 = Buffer(priority=1)
        self.__buffers.append(b1)
        self.__buffers.append(b2)
        self.__buffers.append(b3)
        self.__buffers.append(b4)
        self.__buffers.append(b5)

        # init workstations
        w1_buffers = [b1]
        w2_buffers = [b2, b3]
        w3_buffers = [b4, b5]
        w1 = Workstation(1, w1_buffers)
        w2 = Workstation(2, w2_buffers)
        w3 = Workstation(3, w3_buffers)
        self.__workstations.append(w1)
        self.__workstations.append(w2)
        self.__workstations.append(w3)

    # returns a queue of data from from data file
    @staticmethod
    def __get_list_from_file(file_name) -> list:
        df = pd.read_csv(file_name, header=None)
        time_queue = df.to_numpy().flatten().tolist()
        return time_queue

    # returns the next processing time for workstations
    def __get_workstation_next_processing_time(self, w_id) -> int:
        processing_time = None
        if w_id == 1:
            if len(self.WS1_queue) == 0:
                return None
            processing_time = self.WS1_queue.pop(0)
        if w_id == 2:
            if len(self.WS2_queue) == 0:
                return None
            processing_time = self.WS2_queue.pop(0)
        if w_id == 3:
            if len(self.WS3_queue) == 0:
                return None
            processing_time = self.WS3_queue.pop(0)
        return self.__convert_time_to_int(processing_time)

    # returns a component C1 for Inspector 1
    def __get_i1_next_component(self) -> tuple:
        if len(self.I11_queue) == 0:
            return None, None
        inspection_time = self.I11_queue.pop(0)
        component = Component(1)
        return self.__convert_time_to_int(inspection_time), component

    # returns randomly a component to Inspector 2
    def __get_i2_next_component(self) -> tuple:
        if len(self.I22_queue) == 0 and len(self.I23_queue) == 0:
            return None, None
        elif len(self.I22_queue) == 0:
            inspection_time = self.I23_queue.pop(0)
            component = Component(3)
        elif len(self.I23_queue) == 0:
            inspection_time = self.I22_queue.pop(0)
            component = Component(2)
        elif random() <= 0.5:
            inspection_time = self.I22_queue.pop(0)
            component = Component(2)
        else:
            inspection_time = self.I23_queue.pop(0)
            component = Component(3)
        return self.__convert_time_to_int(inspection_time), component

    # increment system clock
    def __inc_clock(self):
        self.sys_clock += 1

    # converts float dataset to integer dataset
    @staticmethod
    def __convert_time_to_int(time) -> int:
        return int(1000 * time)

    # returns the buffer_id based on component
    def __send_to_buffer(self, inspector_id, component) -> int:
        if inspector_id == 1:
            b1_capacity = self.__buffers[0].capacity
            b2_capacity = self.__buffers[1].capacity
            b4_capacity = self.__buffers[3].capacity

            if b1_capacity <= b2_capacity and b1_capacity <= b4_capacity:
                return 1
            if b2_capacity <= b4_capacity:
                return 2
            return 4
        elif inspector_id == 2:
            c_type = component.get_type()
            if c_type == 2:
                return 3
            if c_type == 3:
                return 5

    # main function running the simulation
    def run_simulation(self):
        # get first components to Inspector 1 & 2
        (new_I1_time, I1_component) = self.__get_i1_next_component()
        (new_I2_time, I2_component) = self.__get_i2_next_component()

        # add inspection events to FEL
        self.FEL.put_event((EventType.arrival, ItemType.component, I1_component), 0)
        self.FEL.put_event((EventType.arrival, ItemType.component, I2_component), 0)
        # perform inspection
        self.__inspectors[0].inspect_component(I1_component, new_I1_time)
        self.__inspectors[1].inspect_component(I2_component, new_I2_time)
        # add completion events to FLE
        self.FEL.put_event((EventType.departure, ItemType.component, I1_component), new_I1_time)
        self.FEL.put_event((EventType.departure, ItemType.component, I2_component), new_I2_time)

        self.__inc_clock()  # finish first cycle

        __sim_time = 99999999
        # run simulation till specified time
        while self.sys_clock <= __sim_time:

            # get all current events
            events = self.FEL.get_events(self.sys_clock)

            # loop over all events
            for event in events:

                # extract event info
                e_type = event[0]
                i_type = event[1]
                component = event[2]

                # get the inspector for the event
                inspector_id = 1 if component.get_type() == 1 else 2

                # get the buffer for the event
                buffer_id = self.__send_to_buffer(inspector_id=inspector_id, component=component)

                # check if the event either:
                #       1. Component finished being inspected
                #       2. Component inspection is halted due to full buffer
                if ((e_type == EventType.departure) or (e_type == EventType.delay)) and (i_type == ItemType.component):
                    # if 2 add a delay event to check later
                    if self.__buffers[buffer_id - 1].is_full:
                        self.FEL.put_event((EventType.delay, ItemType.component, component), self.sys_clock + 1)
                    # if 1
                    #   perform the actions
                    #   get new component for inspection
                    #   create events for new component
                    #   perform actions for the new Component
                    else:
                        # performing actions for the event
                        self.__inspectors[inspector_id - 1].send_component()
                        self.__buffers[buffer_id - 1].insert_component(component=component)

                        # get new component for inspection time
                        new_component = None
                        new_time = None
                        if inspector_id == 1:
                            (new_time, new_component) = self.__get_i1_next_component()
                        elif inspector_id == 2:
                            (new_time, new_component) = self.__get_i2_next_component()

                        # create events for new component
                        self.FEL.put_event((EventType.arrival, ItemType.component, new_component), self.sys_clock)
                        self.FEL.put_event((EventType.departure, ItemType.component, new_component),
                                           self.sys_clock + new_time)

                        # perform actions on the new component
                        self.__inspectors[inspector_id - 1].inspect_component(I1_component, new_I1_time)

            # Check all workstations
            for workstation in self.__workstations:
                # if workstation is ideal and can build products build product
                if not workstation.is_making_product and workstation.can_dequeue_buffers():
                    w_id = workstation.type
                    processing_time = self.__get_workstation_next_processing_time(w_id=w_id)

                    # add the product building events
                    self.FEL.put_event((EventType.arrival, ItemType.product), self.sys_clock)
                    self.FEL.put_event((EventType.departure, ItemType.product), self.sys_clock + processing_time)

            # increment system Clock
            self.__inc_clock()

        #   ----------- Simulation Ends -----------------

        # Print FEL
        self.FEL.print()
