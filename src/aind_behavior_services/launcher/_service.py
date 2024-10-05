import abc


class IService(abc.ABC):
    "A base class for all services that defines a minimal interface"

    @abc.abstractmethod
    def validate(self, *args, **kwargs) -> bool:
        pass
