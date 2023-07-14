from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple(
            [
                (enum.value, name.replace("_", " ").capitalize())
                for name, enum in cls.__members__.items()
            ]
        )

    @classmethod
    def get_enum(cls, name):
        return cls.__members__[name]

    @classmethod
    def get_description(cls, value):
        return dict(cls.choices()).get(value)


class IntEnum(int, BaseEnum):
    pass


class CharEnum(str, BaseEnum):
    pass


class NotifyActionType(CharEnum):
    INVITE = "invite.html"
    VERIFICATION = "verify.html"
    RESET_PASSWORD = "reset.html"