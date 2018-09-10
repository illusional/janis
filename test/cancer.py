import unittest

from pipeline_definition.pipeline_translator import PipelineTranslator
import json
import examples.bio_informatics

_yml = """
inputs:
  tumour:
    SequenceReadArchivePaired:
      forward-pattern: '*_R1.fastq.gz'
      backward-pattern: '*_R2.fastq.gz'
  normal:
    SequenceReadArchivePaired:
      forward-pattern: '*_R1.fastq.gz'
      backward-pattern: '*_R2.fastq.gz'
  ref:
    REFERENCE:
      path: 'path/to/reference'

steps:
  - step1:
      tag: 'tumour'
      trim:
        trimmer : 'trimmomatic'
  - step2:
      tag: 'tumour'
      align:
        aligner: 'bwa'
  - step3:
      tag: 'tumour'
      call:
  - step4:
      tag: 'normal'
      trim:
        trimmer : 'trimmomatic'
  - step5:
      tag: 'normal'
      align:
        aligner: 'bwa'
  - step6:
      tag: 'normal'
      call:
  - step7:
      joint_call:
        caller: mutect
        tumour_tag: 'tumour'
        normal_tag: '#normal'

"""

_expected = json.loads("""
{
    "workflow": {
        "inputs": {
            "tumour": {
                "type": "SequenceReadArchivePaired"
            },
            "normal": {
                "type": "SequenceReadArchivePaired"
            },
            "ref": {
                "type": "REFERENCE"
            }
        },
        "flow": {
            "tumour": {
                "steps": {
                    "1": {
                        "step": "step1",
                        "type": "trim",
                        "step-inputs": {
                            "read": {
                                "type": "SequenceReadArchivePaired",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "tumour",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "trimmed": {
                                "type": "SequenceReadArchivePaired"
                            }
                        }
                    },
                    "2": {
                        "step": "step2",
                        "type": "align",
                        "step-inputs": {
                            "read": {
                                "type": "SequenceReadArchivePaired",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "trimmed",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "step1",
                                            "tag": "tumour"
                                        },
                                        "2": {
                                            "id": "tumour",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            },
                            "reference": {
                                "type": "REFERENCE",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "ref",
                                            "type": "REFERENCE",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "alignedbamfile": {
                                "type": "BAM"
                            }
                        }
                    },
                    "3": {
                        "step": "step3",
                        "type": "call",
                        "step-inputs": {
                            "alignedbamfile": {
                                "type": "BAM",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "alignedbamfile",
                                            "type": "BAM",
                                            "step": "step2",
                                            "tag": "tumour"
                                        }
                                    }
                                }
                            },
                            "reference": {
                                "type": "REFERENCE",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "ref",
                                            "type": "REFERENCE",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "read": {
                                "type": "VCF"
                            }
                        }
                    }
                }
            },
            "normal": {
                "steps": {
                    "1": {
                        "step": "step4",
                        "type": "trim",
                        "step-inputs": {
                            "read": {
                                "type": "SequenceReadArchivePaired",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "normal",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "trimmed": {
                                "type": "SequenceReadArchivePaired"
                            }
                        }
                    },
                    "2": {
                        "step": "step5",
                        "type": "align",
                        "step-inputs": {
                            "read": {
                                "type": "SequenceReadArchivePaired",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "trimmed",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "step4",
                                            "tag": "normal"
                                        },
                                        "2": {
                                            "id": "normal",
                                            "type": "SequenceReadArchivePaired",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            },
                            "reference": {
                                "type": "REFERENCE",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "ref",
                                            "type": "REFERENCE",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "alignedbamfile": {
                                "type": "BAM"
                            }
                        }
                    },
                    "3": {
                        "step": "step6",
                        "type": "call",
                        "step-inputs": {
                            "alignedbamfile": {
                                "type": "BAM",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "alignedbamfile",
                                            "type": "BAM",
                                            "step": "step5",
                                            "tag": "normal"
                                        }
                                    }
                                }
                            },
                            "reference": {
                                "type": "REFERENCE",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "ref",
                                            "type": "REFERENCE",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "read": {
                                "type": "VCF"
                            }
                        }
                    }
                }
            },
            "untagged": {
                "steps": {
                    "1": {
                        "step": "step7",
                        "type": "joint_call",
                        "step-inputs": {
                            "normal_tag": {
                                "type": "BAM",
                                "mapping": {
                                    "provided": "#normal",
                                    "candidates": {
                                        "1": {
                                            "id": "alignedbamfile",
                                            "type": "BAM",
                                            "step": "step5",
                                            "tag": "normal"
                                        }
                                    }
                                }
                            },
                            "tumour_tag": {
                                "type": "BAM",
                                "mapping": {
                                    "provided": "tumour",
                                    "candidates": {
                                        "ERROR": "Failed to find any candidate!!!!!"
                                    }
                                }
                            },
                            "references": {
                                "type": "REFERENCE",
                                "mapping": {
                                    "provided": "",
                                    "candidates": {
                                        "1": {
                                            "id": "ref",
                                            "type": "REFERENCE",
                                            "step": "input-step",
                                            "tag": "input"
                                        }
                                    }
                                }
                            }
                        },
                        "step-outputs": {
                            "out1": {
                                "type": "VCF"
                            }
                        }
                    }
                }
            }
        }
    }
}""")


class TumourNormalPipeline(unittest.TestCase):

  def test_graph(self):
    translator = PipelineTranslator(debug=True)
    translation = translator.translate_string(_yml)
    tr_json = json.loads(translation)
    self.assertTrue(tr_json == _expected)


if __name__ == '__main__':
    unittest.main()


