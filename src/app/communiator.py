

class Communicator:
    """This class will be used to communicate between frontend and backend code"""

    __frontend_object = None

    @classmethod

    def log_message(cls, message):
        """Log message to frontend"""

        if not cls.__frontend_object:
            raise AttributeError("Frontend object is not set. Please use 'set_frontend_obj' method first.")

        cls.__frontend_object.append_message(message) 

    @classmethod
    def set_frontend_obj(cls, obj):
        cls.__frontend_object = obj 