from pipeline_definition.types.step_type import StepFactory
from pipeline_definition.types.step_type import Step


class TrimFactory(StepFactory):
  @classmethod
  def type(cls):
    return 'trim'

  @classmethod
  def label(cls):
    return 'trim'

  @classmethod
  def description(cls):
    return cls.label()

  @classmethod
  def describe(cls):
    return {
      'schema': {
        'trimmer': {
          'type': 'string',
          'allowed': ['cutadapt', 'trimmomatic'],
          'default': 'trimmomatic'
        }
      },
      'nullable': True
    }

  @classmethod
  def build(cls, meta, debug=False):
    return TrimStep(meta, debug=debug)


class TrimStep(Step):

  def __init__(self, input_dict, debug=False):
    super().__init__(input_dict, debug=debug)
    if self.meta()['trimmer'] != 'trimmomatic':
      raise Exception('Sorry, only trimmomatic is supported at the moment.')

  def cores(self):
    return 2

  def ram(self):
    return 16000

  def translate(self, step_inputs):
    vf = """${
  self.format = "http://edamontology.org/format_1930";
  return self;
}
"""

    xlate = dict()

    xlate['run'] = '../tools/src/tools/trimmomatic.cwl'
    xlate['requirements'] = {'ResourceRequirement': {'coresMin': self.cores(), 'ramMin': self.ram()}}

    mi = step_inputs[0]
    candidate = next(iter(mi.candidates.values()))
    input_id = candidate['id']
    xlate['in'] = {
      'reads1': {'source': input_id + '_forward', 'valueForm': vf},
      'reads2': {'source': input_id + '_backward', 'valueForm': vf}
    }

    xlate['end_mode'] = {'default': 'PE'}
    xlate['nthreads'] = {'valueFrom': '$(' + str(self.cores()) + ')'}
    xlate['illuminaClip'] = {
      'source': 'adaptors',
      'valueForm': """${
  return {
    "adapters": self,
    "seedMismatches": 1,
    "palindromeClipThreshold": 20,
    "simpleClipThreshold": 20,
    "minAdapterLength": 4,
    "keepBothReads": true };
}
"""
    }

    xlate['out'] = ['output_log', 'reads1_trimmed', 'reads1_trimmed_unpaired', 'reads2_trimmed_paired',
                    'reads2_trimmed_unpaired']

    return {self.id(): xlate}

  def provides(self):
    return [
      {
        Step.STR_ID: "trimmed",
        Step.STR_TYPE: "TrimmedReads"
      }
    ]

  def requires(self):
    return [
      {
        Step.STR_ID: "read",
        Step.STR_TYPE: "SequenceReadArchivePaired"
      }
    ]