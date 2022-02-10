# holds the data and methods for products
class Product:

    __type: int = None  # specifies P1 or P2

    # Constructor:
    # Inputs:
    #       p_type:int -> Product Type
    def __init__(self, p_type):
        if (p_type is not None) and (p_type >= 0) and (p_type <= 3):
            self.__type = p_type
        else:
            raise Exception("ProductTypeError")

    # returns the product type
    def get_type(self):
        if self.__type is None:
            raise Exception("NotInitializedProduct")
        else:
            return self.__type
