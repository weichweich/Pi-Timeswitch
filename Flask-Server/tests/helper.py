

class Bunch:
    """Class which adds all key word arguments as members to the object created
    """
    def __init__(self, **kwds):
        self.__dict__.update(kwds)
