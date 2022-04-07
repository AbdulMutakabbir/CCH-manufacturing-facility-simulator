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
    product = 1


# Class that holds the simulation environment and runs the main simulation code
class Simulator:
    __inspectors = []  # list of inspectors
    __buffers = []  # list of buffers
    __workstations = []   # list of workstations
    sys_clock = 0   # system clock
    __last_buffer = 4  # buffer tracking for policy 2

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
        i1 = Inspector(i_type=1)
        i2 = Inspector(i_type=2)
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

    # returns the buffer_id based on component for policy 1
    def __send_to_buffer_policy_1(self, inspector_id, component) -> int:
        if inspector_id == 1:
            b1_capacity = self.__buffers[0].get_capacity()
            b2_capacity = self.__buffers[1].get_capacity()
            b4_capacity = self.__buffers[3].get_capacity()

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

    # returns the buffer_id based on component for policy 2
    def __send_to_buffer_policy_2(self, inspector_id, component) -> int:
        b1_capacity = self.__buffers[0].get_capacity()
        b2_capacity = self.__buffers[1].get_capacity()
        b4_capacity = self.__buffers[3].get_capacity()

        # apply round robin if any buffer is empty for inspector 1
        if (inspector_id == 1) and ((b1_capacity == 0) or (b2_capacity == 0) or (b4_capacity == 0)):
            if self.__last_buffer == 1:
                self.__last_buffer = 2
                if b2_capacity == 0:
                    self.__last_buffer = 2
                    return 2
                elif b4_capacity == 0:
                    return 4
                else:
                    return 1

            elif self.__last_buffer == 2:
                self.__last_buffer = 4
                if b4_capacity == 0:
                    return 4
                elif b1_capacity == 0:
                    return 1
                else:
                    return 2
            elif self.__last_buffer == 4:
                self.__last_buffer = 1
                if b1_capacity == 0:
                    return 1
                elif b2_capacity == 0:
                    return 2
                else:
                    return 4
            else:
                raise Exception("Unknown Last buffer")
        # else do the old policy 1
        else:
            buffer = self.__send_to_buffer_policy_1(inspector_id, component)
            return buffer

    # returns the buffer_id based on component
    def __send_to_buffer(self, inspector_id, component) -> int:
        buffer = self.__send_to_buffer_policy_2(inspector_id, component)
        return buffer

    # main function running the simulation
    def run_simulation(self, sim_time=499999):
        end_sim_flag = False

        products_count = [0, 0, 0]
        workstations_busy_count = [0, 0, 0]
        buffer_occupancy_count = [0, 0, 0, 0, 0]
        inspector_block_count = [0, 0]

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

        # run simulation till specified time
        while self.sys_clock <= sim_time:
            # get all current events
            events = self.FEL.get_events(self.sys_clock)

            # loop over all events
            for event in events:

                # extract event info
                e_type = event[0]
                i_type = event[1]

                # check if the event is -- Component finished being inspected
                if (e_type == EventType.departure) and (i_type == ItemType.component):
                    component = event[2]
                    # get the inspector for the event
                    inspector_id = 1 if component.get_type() == 1 else 2
                    # get the buffer for the event
                    buffer_id = self.__send_to_buffer(inspector_id=inspector_id, component=component)

                    #   perform the actions:
                    #       inspector sends component
                    #       insert component to buffer
                    self.__inspectors[inspector_id - 1].send_component()
                    self.__buffers[buffer_id - 1].insert_component(component=component)
                    print(f"Log:\tFinished Comp: {component.get_type()}")

                # check if the event is -- Product built
                if (e_type == EventType.departure) and (i_type == ItemType.product):
                    product = event[2]
                    # get the workstation for the event
                    workstation_id = product.get_type()
                    product_type = product.get_type()

                    #   perform the actions:
                    #       finish building product
                    self.__workstations[workstation_id - 1].finish_building_product()

                    # increment product production count
                    products_count[product_type - 1] += 1

                    print(f"Log:\tProduced Product: {product_type}")

            # Check all workstations
            for workstation in self.__workstations:
                can_dequeue = workstation.can_dequeue_buffers()

                workstation_id = workstation.get_type()

                # increment workstation busy time if it is busy
                if workstation.is_making_product:
                    workstations_busy_count[workstation_id - 1] += 1

                # if workstation is ideal and can build products build product
                if (not workstation.is_making_product) and can_dequeue:
                    processing_time = self.__get_workstation_next_processing_time(w_id=workstation_id)

                    # start building product
                    is_building, product = workstation.start_building_product(processing_time)

                    if is_building:
                        # add the product building events
                        self.FEL.put_event((EventType.arrival, ItemType.product, product), self.sys_clock)
                        self.FEL.put_event((EventType.departure, ItemType.product, product), self.sys_clock +
                                           processing_time)
                        print(f"Log:\tStarted building Product: {workstation_id}")

            # Check all inspectors
            for inspector in self.__inspectors:
                inspector_id = inspector.get_type()

                # Check if inspector is not inspecting
                if not self.__inspectors[inspector_id - 1].is_inspecting:
                    new_component = None
                    new_time = None
                    if inspector_id == 1:
                        new_time, new_component = self.__get_i1_next_component()
                    elif inspector_id == 2:
                        new_time, new_component = self.__get_i2_next_component()

                    if new_component is None:
                        print("Component List Finished")
                        end_sim_flag = True
                        break

                    buffer_id = self.__send_to_buffer(inspector_id=inspector_id, component=new_component)

                    # if inspector buffer are not full inspect
                    if not self.__buffers[buffer_id - 1].is_full:
                        # create events for new component
                        self.FEL.put_event((EventType.arrival, ItemType.component, new_component), self.sys_clock)
                        self.FEL.put_event((EventType.departure, ItemType.component, new_component),
                                           self.sys_clock + new_time)

                        # perform actions on the new component
                        self.__inspectors[inspector_id - 1].inspect_component(new_component, new_I1_time)
                        print("Log: \tStarted Inspecting Component:", new_component.get_type())

                    # inspector buffers are full put the component back on hold
                    # and increment inspector block time
                    else:
                        new_component_type = new_component.get_type()
                        if new_component_type == 1:
                            self.I11_queue.insert(0, new_time)
                        elif new_component_type == 2:
                            self.I22_queue.insert(0, new_time)
                        elif new_component_type == 3:
                            self.I23_queue.insert(0, new_time)

                        # increment inspector block time
                        inspector_block_count[inspector_id - 1] += 1

            # Increment buffer capacity count
            for index, buffer in enumerate(self.__buffers):
                buffer_occupancy_count[index] += buffer.get_capacity()

            if end_sim_flag:
                break

            # increment system Clock
            self.__inc_clock()

        #   ----------- Simulation Ends -----------------

        # Print FEL
        # self.FEL.print()

        products_throughput = []
        for product_count in products_count:
            try:
                products_throughput.append(product_count/(self.sys_clock/1000))
            except ZeroDivisionError:
                products_throughput.append(None)

        probability_workstation_busy = []
        avg_wait_time = []
        for index, busy_count in enumerate(workstations_busy_count):
            probability_workstation_busy.append(busy_count/self.sys_clock)
            try:
                avg_wait_time.append(busy_count/products_count[index]/1000)
            except ZeroDivisionError:
                avg_wait_time.append(None)

        avg_buffer_occupancy = []
        for occupancy_count in buffer_occupancy_count:
            avg_buffer_occupancy.append(occupancy_count/self.sys_clock)

        probability_inspector_blocked = []
        for block_time in inspector_block_count:
            probability_inspector_blocked.append(block_time/self.sys_clock)

        for index, throughput in enumerate(products_throughput):
            print(f"Product {index + 1} throughput: {throughput}")
        for index, probability_busy in enumerate(probability_workstation_busy):
            print(f"Workstation {index + 1} busy probability: {probability_busy}")
        for index, wait_time in enumerate(avg_wait_time):
            print(f"Workstation {index + 1} wait time: {wait_time}")
        for index, product_count_value in enumerate(products_count):
            print(f"Workstation {index + 1} products produced: {product_count_value}")
        for index, occupancy in enumerate(avg_buffer_occupancy):
            print(f"Buffer {index + 1} average occupancy: {occupancy}")
        for index, probability_blocked in enumerate(probability_inspector_blocked):
            print(f"Inspector {index + 1} block probability: {probability_blocked}")
