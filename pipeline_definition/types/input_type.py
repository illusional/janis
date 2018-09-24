#
# Input type base class
#
from abc import ABC, abstractmethod


class InputFactory(ABC):
  @classmethod
  @abstractmethod
  def type(cls):
    # The string that identifies this file type in definition files.
    pass

  @classmethod
  @abstractmethod
  def label(cls):
    # A human friendly short label to present in user interfaces.
    pass

  @classmethod
  @abstractmethod
  def description(cls):
    # A longer description of this type to present in user interfaces.
    pass

  @classmethod
  @abstractmethod
  def describe(cls):
    # Describe the schema for this type.
    pass

  @classmethod
  @abstractmethod
  def build(cls, input_dict, debug=False):
    # Build an Input object given the definition in the input_dict
    pass

  @classmethod
  def build_from(cls, input_dict, debug=False):
    input_type = cls.type()
    if debug:
      print(input_type, "factory: Building from", input_dict)
    obj = cls.build(input_dict, debug=debug)
    obj.identify()
    return obj


class Input(ABC):
  def __init__(self, input_dict, debug=False):
    self.__id = next(iter(input_dict.keys()))

    meta = next(iter(input_dict.values()))
    self.__type = next(iter(meta.keys()))
    self.__meta = next(iter(meta.values()))
    self.__debug = debug

  def identify(self):
    if self.__debug:
      print("Instance: [", self.id, " - ", self.type, " - ", self.meta, " ]")

  def id(self):
    # The id by which this input will be referred.
    return self.__id

  def type(self):
    # A string identifying the file type
    return self.__type

  def meta(self):
    # Internal metadata required by this object
    return self.__meta

  @abstractmethod
  def datum_type(self):
    pass

  @abstractmethod
  def is_subtype_of(self, other):
    pass

  def resolve(self):
    # Resolve actual object names in the appropriate store. For example, if the input is a query (regex)
    # the query is executed and resolved objects are returned as part of the translation. If the file
    # is a reference, its existence is checked.
    raise NotImplementedError("resolve not implemented for this type")

  def translate_for_input(self):
    # - Generate the input object list. In the case of CWL, this is typically a separate yml file
    #   specifying a list of actual files.
    # - The expected return is a target language specific dictionary that the translator will render
    #   to the actual language text.
    raise NotImplementedError("A translation has been requested but has not been implemented for this input")

  def translate_for_workflow(self):
    # - Generate the input stanza required by the target language. In the case of CWL, this is the 'inputs'
    #   section
    # - The expected return is a target language specific dictionary that the translator will render
    #   to the actual language text.
    raise NotImplementedError("A translation has been requested but has not been implemented for this input")