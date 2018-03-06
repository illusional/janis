#
#
#
from abc import ABC, abstractmethod


class StepFactory(ABC):
    @classmethod
    @abstractmethod
    def type(cls):
        pass

    @classmethod
    @abstractmethod
    def label(cls):
        pass

    @classmethod
    @abstractmethod
    def description(cls):
        pass

    @classmethod
    @abstractmethod
    def describe(cls):
        pass

    @classmethod
    @abstractmethod
    def build(cls, meta):
        pass

    @classmethod
    def buildFrom(self, dict):
        type = self.type()
        print(type, "factory: Building from", dict)
        obj = self.build(dict)
        obj.identify()
        return obj


class Step(ABC):
    def __init__(self, dict):
        self.id = next(iter(dict.keys()))

        meta = next(iter(dict.values()))

        if meta is not None:
            self.type = next(iter(meta.keys()))
            self.meta = next(iter(meta.values()))
        else:
            self.type = self.id
            self.meta = None

    @abstractmethod
    def provides(self):
        # A set of optionally tagged input data
        pass

    @abstractmethod
    def requires(self):
        # A set of optionall tagged output data
        pass

    def identify(self):
        print("Instance: [", self.id, " - ", self.type, " - ", self.meta, " ]" )

    #@abstractmethod
    #def type(self):
    #    pass

    # @classmethod
    #@abstractmethod
    #def label(self):
    #    pass

    # @classmethod
    #@abstractmethod
    #def description(self):
    #    pass

    # @classmethod
    #@abstractmethod
    #def save(self):
    #    pass

    # @classmethod
    #@abstractmethod
    #def can_default(self):
    #    pass

class TaggedDatum(ABC):
    @abstractmethod
    def tags(self):
        # A set tags that can select among similar types
        pass

    @abstractmethod
    def datum_type(self):
        # A datum_type
        pass

    def satisfies(self, datum):
        # A concrete implementation here
        pass

