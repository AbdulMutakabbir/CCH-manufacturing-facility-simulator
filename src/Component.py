# Hold the Data and Methods for Components
class Component:
    __type: int = None  # specifies C1 or C2 or C3

    # Constructor:
    # Inputs:
    #       c_type:int -> Component Type
    def __init__(self, c_type: int):
        if (c_type is not None) and (c_type >= 0) and (c_type <= 3):
            self.__type = c_type
        else:
            raise Exception("ComponentTypeError")

    # returns the component type
    def get_type(self):
        if self.__type is None:
            raise Exception("NotInitializedComponent")
        else:
            return self.__type
