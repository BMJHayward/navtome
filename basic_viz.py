import argparse
import os
from Bio import SeqIO, SeqRecord, Seq
from collections import Counter, defaultdict
from dna_features_viewer import BiopythonTranslator, CircularGraphicRecord, GraphicFeature, GraphicRecord
from matplotlib import pyplot as plt
plt.style.use('ggplot')

def naive_backtranslate(seq_object):
    '''
    select ambiguous|unambiguous
    select DNA|RNA
    select codon table from list
    parse given seq_object argument into peptide string
    back translate each amino acid to its potential codons
    eg:
    >>> from Bio.Data import CodonTable
    >>> cerp = CodonTable.ambiguous_dna_by_name['Mycoplasma'].forward_table
    >>> newcerp = dict()
    >>> for cod, ami in cerp.items():
    >>>     if ami not in newcerp.keys():
    >>>         newcerp[ami] = [cod]
    >>>     else:
    >>>         newcerp[ami].append(cod)
    >>> print(newcerp)
    '''
    pass

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
    plt.show()
  
    # circle_record = CircularGraphicRecord(sequence_length=1000, features=features)
    # circle_record.plot_with_bokeh(figure_width=5)
    # seq_record = SeqIO.read('data/Lactobacillus_reuteri/GCA_000016825.1_Lactobacillus_reuteri_DSM_20016_Complete_Genome.fasta', 'fasta')
    # graphic_record = BiopythonTranslator().translate_record(seq_record)
    # ax, _ = graphic_record.plot(figure_width=10)

def ngrams(sequence, n):
    sequence = list(sequence)
    count = max(0, len(sequence) - n + 1)
    return [tuple(sequence[i:i+n]) for i in range(count)]

def make_trigrams(sequence):
    if type(sequence)==SeqRecord.SeqRecord:
        return [''.join([t for t in tup]) for tup in ngrams(str(sequence.seq),3)]
    elif type(sequence)==Seq.Seq:
        return [''.join([t for t in tup]) for tup in ngrams(str(sequence),3)]
    elif type(sequence)==str:
        return [''.join([t for t in tup]) for tup in ngrams(sequence,3)]
    else:
        raise TypeError(
          ('sequence was type: {}, need Biopython.SeqRecord, Biopython.Seq.Seq, or str type'
          .format(type(sequence))))

def nucleotide_distribution(sequence, **kwargs):
     if kwargs['normed']:
       plt.hist(make_trigrams(sequence), normed=True)
     else:
       plt.hist(make_trigrams(sequence))
     plt.xticks(rotation=90)
     plt.show()

def get_peptide_toplot(sequence):
    peptide_alphabet = 'ACDEFGHIKLMNPQRSTVWYBXZJUO*'
    if (type(sequence)==Seq.Seq and sequence.alphabet.letters==peptide_alphabet):
      return sequence
    elif type(sequence)==SeqRecord.SeqRecord:
      return sequence.seq.transcribe().translate()
    elif type(sequence)==Seq.Seq:
      return sequence.transcribe().translate()
    else:
      raise TypeError('sequence was type: {}, need Biopython.SeqRecord, Biopython.Seq.Seq, or str type'.format(type(sequence)))

def peptide_distribution(sequence, **kwargs):
    if kwargs['normed']:
        plt.hist(get_peptide_toplot(sequence), normed=True)
    else:
        plt.hist(get_peptide_toplot(sequence))
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

def main(args):
    if args.filename:
        ext = {'gbk':'genbank','fasta':'fasta'}
        filetype = ext[args.filename.name.split('.')[-1]]
        sequence = SeqIO.read(args.filename, filetype)
        if args.abi_trace:
            plot_ABI(sequence)
        if args.nucleotide_distribution:
            nucleotide_distribution(sequence, normed=args.normed)
        if args.peptide_distribution:
            peptide_distribution(sequence, normed=args.normed)
    elif args.demonstrate:
        demo_dna_features_viewer()
    else:
        print(args)
       

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Basic genomic visualisation and stats',
        epilog='''Plots an abi trace, or distributions of codons
                  or amino acids.
               '''
    )
    parser.add_argument('-demo', '--demonstrate',
        help='will demonstrate graphic record of a small plasmid',
        default=False, action='store_true')
    parser.add_argument('-abi', '--abi-trace',
        help='plot an abi trace',
        default=False, action='store_true')
    parser.add_argument('-nuc', '--nucleotide_distribution',
        help='''plot a naive distribution of codons. I.e.
                does not heed start/stop codons, ORFs etc''',
        default=False, action='store_true')
    parser.add_argument('-pep', '--peptide_distribution',
        help='''Plots distribution of amino acids in a peptide chain.
                If given a nucleotide sequence, will perform translation if RNA, and 
                transcription+translation if DNA''',
        default=False, action='store_true')
    parser.add_argument('-f', '--filename',
        help='''File name for processing. Only genbank and fasta files are
        currently supported. If no filename, then only the 'demo' option
        will work.''',
        default=None,
        nargs='?',
        type=argparse.FileType('r'))
    parser.add_argument('-normed', '--normed',
        help='''plot distribution in normalised form''',
        default=False, action='store_true', dest='normed')
    args = parser.parse_args()
    main(args)
