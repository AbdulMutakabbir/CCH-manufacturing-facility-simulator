from Product import Product


# holds the data and methods for workstations
class Workstation:
    __buffers = None
    __type = None
    is_making_product = None
    is_built = None
    __processing_time = None

    # Constructor:
    # Inputs:
    #       w_type:int -> workstation Type
    #       buffers:list -> holds an array of buffers for the workstation
    def __init__(self, w_type: int, buffers: list):
        if (w_type is not None) or (w_type >= 0) or (w_type <= 3) or (buffers is not None) or (len(buffers) >= 0) or \
                (len(buffers) <= 0):
            self.__type = w_type
            self.__buffers = buffers
        else:
            raise Exception("WorkstationInitializationError")

        # init class variables
        self.is_making_product = False
        self.is_built = False

    # perform the actions for start of the product build
    def start_building_product(self, build_time):
        if build_time is not None and build_time <= 0:
            raise Exception("WorkstationBuildTimeNotSpecified")
        if (self.__buffers is None) or (self.__type is None) or (self.is_making_product is None):
            raise Exception("WorkstationNotInitialised")
        if self.is_making_product:
            raise Exception("WorkstationInProduction")
        else:
            product = None
            can_dequeue = self.can_dequeue_buffers()
            self.dequeue_buffers()
            if can_dequeue:
                self.is_making_product = True
                self.__processing_time = build_time
                self.is_built = False
                product = self.get_product()
                return True, product
            else:
                return False, product

    # remove components from buffers to build the product
    def dequeue_buffers(self):
        if self.can_dequeue_buffers():
            if self.__type == 1:
                self.__buffers[0].send_component()
            if self.__type == 2 or self.__type == 3:
                self.__buffers[0].send_component()
                self.__buffers[1].send_component()

    # check if there are enough components to build the product
    def can_dequeue_buffers(self):
        if not self.__buffers[0].is_empty:
            if self.__type == 1:
                return True
            if self.__type == 2 or self.__type == 3:
                if not self.__buffers[1].is_empty:
                    return True
                else:
                    return False
        else:
            return False

    # perform the action to make the product
    def finish_building_product(self):
        if self.is_built is not None:
            self.is_built = False
            self.is_making_product = False
            self.__processing_time = None
        else:
            raise Exception("ProductionInProcess")

    # get workstations product
    def get_product(self):
        if self.is_built is not None and (self.is_making_product == True):
            return Product(self.__type)
        else:
            raise Exception("ProductionInProcess")

    # returns the workstation  type
    def get_type(self):
        if self.__type is None:
            raise Exception("NotInitializedWorkstation")
        else:
            return self.__type

    # def progress_build(self):
    #     if self.processing_time is not None and self.processing_time == 0:
    #         self.is_built = True
    #         self.processing_time = None
    #         return
    #     if self.processing_time is not None and self.processing_time > 0:
    #         self.processing_time -= 1
    #         return
    #     if self.processing_time is None:
    #         raise Exception("ProcessingTimeNotSpecified")
