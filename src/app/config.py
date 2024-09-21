class Config:
    """This class will hold variables value set by user.
    For example: url and output file format
    """

    __url = None
    __format = None

    @classmethod
    def get_url(cls):
        if cls.__url is None:
            raise ValueError(
                "URL has not been set. Please call 'set_url' to initialize it."
            )
        return cls.__url

    @classmethod
    def get_format(cls):
        if cls.__format is None:
            raise AttributeError(
                "Format has not been set. Please call 'set_format' to initialize it."
            )
        return cls.__format

    @classmethod
    def set_url(cls, url):
        cls.__url = url

    @classmethod
    def set_format(cls, format):
        cls.__format = format
