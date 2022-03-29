from Component import Component


# holds the data and methods for Inspector class
class Inspector:
    __type: int = None  # Specifies if inspector 1 or 2
    __accepted_component_list: list = None
    is_inspecting: bool = None
    __working_on: Component = None
    inspection_time: int = None

    # Constructor:
    # Inputs:
    #       i_type:int -> inspector Type
    def __init__(self, i_type: int):
        if (i_type is not None) and (i_type >= 0) and (i_type <= 2):
            self.__type = i_type
        else:
            raise Exception("InspectionTypeError")

        self.is_inspecting = False
        self.__accepted_component_list = []
        if self.__type == 1:
            self.__accepted_component_list.append(1)
        elif self.__type == 2:
            self.__accepted_component_list.append(2)
            self.__accepted_component_list.append(3)

    # performs actions of inspecting the component
    def inspect_component(self, component, time):
        if self.__type is None:
            raise Exception("InspectorNotInitialised")
        else:
            self.is_inspecting = True
            self.__working_on = component
            self.inspection_time = time

    # perform actions for completing the inspection
    def send_component(self):
        if not self.is_inspecting:
            raise Exception("NoItemToSend")
        else:
            self.is_inspecting = False
            self.inspection_time = None
            self.__working_on = None

    # returns the inspector type
    def get_type(self):
        if self.__type is None:
            raise Exception("NotInitializedComponent")
        else:
            return self.__type
