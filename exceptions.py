class InternalServerException(Exception):
    __err_temp = "Internal Server Error: {}"
    __err_msg: str

    def __init__(self, err):
        self.__err_msg = err

    def __str__(self):
        return self.__err_temp.format(self.__err_msg)
