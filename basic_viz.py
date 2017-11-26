from Bio import SeqIO, SeqRecord, Seq
from collections import Counter, defaultdict
from dna_features_viewer import BiopythonTranslator, CircularGraphicRecord, GraphicFeature, GraphicRecord
from matplotlib import pyplot as plt

def demo_dna_features_viewer():
  features=[
      GraphicFeature(start=0, end=20, strand=+1, color="#ffd700",
                     label="Small feature"),
      GraphicFeature(start=20, end=500, strand=+1, color="#ffcccc",
                     label="Gene 1 with a very long name"),
      GraphicFeature(start=400, end=700, strand=-1, color="#cffccc",
                     label="Gene 2"),
      GraphicFeature(start=600, end=900, strand=+1, color="#ccccff",
                     label="Gene 3")
  ]
  record = GraphicRecord(sequence_length=1000, features=features)
  record.plot(figure_width=5)

  record = CircularGraphicRecord(sequence_length=1000, features=features)
  record.plot_with_bokeh(figure_width=5)

  # seq_record = SeqIO.read('data/Lactobacillus_reuteri/GCA_000016825.1_Lactobacillus_reuteri_DSM_20016_Complete_Genome.fasta', 'fasta')
  # graphic_record = BiopythonTranslator().translate_record(seq_record)
  ax, _ = graphic_record.plot(figure_width=10)


def ngrams(sequence, n):
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)]

def nucleotide_distribution(sequence):
  if type(sequence)==SeqRecord.SeqRecord:
    trigrams = [''.join([t for t in tup]) for tup in ngrams(sequence.seq.tostring(),3)]
  elif type(sequence)==Seq.Seq:
    trigrams = [''.join([t for t in tup]) for tup in ngrams(sequence.tostring(),3)]
  elif type(sequence)==str:
    trigrams = [''.join([t for t in tup]) for tup in ngrams(sequence,3)]
  else:
    raise TypeError('sequence was type: {}, need Biopython.SeqRecord, Biopython.Seq.Seq, or str type'.format(type(sequence)))
  plt.hist(trigrams)
  plt.show()

def peptide_distribution(sequence):
  peptide_alphabet = 'ACDEFGHIKLMNPQRSTVWYBXZJUO*'
  if (type(sequence)==Seq.Seq and sequence.alphabet.letters==peptide_alphabet):
    plt.hist(sequence)
  elif type(sequence)==SeqRecord.SeqRecord:
    plt.hist(sequence.seq.transcribe().translate())
  elif type(sequence)==Seq.Seq:
    plt.hist(sequence.transcribe().translate())
  else:
    raise TypeError('sequence was type: {}, need Biopython.SeqRecord, Biopython.Seq.Seq, or str type'.format(type(sequence)))
  plt.show()

def plot_ABI(abifilename):
  record = SeqIO.read(abifilename, 'abi')
  record.annotations.keys()
  record.annotations['abif_raw'].keys()
  channels = ['DATA9', 'DATA10', 'DATA11', 'DATA12']
  trace = defaultdict(list)
  for c in channels:
      trace[c] = record.annotations['abif_raw'][c]
  plt.plot(trace['DATA9'], color='blue')
  plt.plot(trace['DATA10'], color='red')
  plt.plot(trace['DATA11'], color='green')
  plt.plot(trace['DATA12'], color='yellow')
  plt.show()
