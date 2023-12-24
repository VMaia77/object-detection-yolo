


class BaseError:
    def to_dict(self):
        return dict(message_code=self.message_code, 
                    message_type=self.message_type,
                    message=self.message)


class InvalidImage(BaseError):
    def __init__(self):
        self.message_code = 700
        self.message_type = "INVALID_IMAGE"
        self.message = "Image extension is not valid"
