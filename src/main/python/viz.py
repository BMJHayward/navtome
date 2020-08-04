#!/usr/bin/env python3
import argparse
from Bio import PDB, SeqIO, SeqRecord, Seq
from Bio.Data import CodonTable
from collections import Counter, defaultdict
from dna_features_viewer import BiopythonTranslator, CircularGraphicRecord, GraphicFeature, GraphicRecord
from itertools import chain, product
from matplotlib import pyplot as plt
import multiprocessing as mp
import os
from pathlib import Path
import sys
import textdistance as TD
from typing import Iterable, List

plt.style.use('ggplot')

PLOTDIR = 'plots'
if not os.path.exists(PLOTDIR):
    os.mkdir(os.path.join(os.curdir, PLOTDIR))

DATADIR = 'data'
if not os.path.exists(DATADIR):
    os.mkdir(os.path.join(os.curdir, DATADIR))

textdistfuncs = [
    'cosine',
    'damerau_levenshtein',
    'editex',
    'entropy_ncd',
    'gotoh',
    'hamming',
    'identity',
    'jaccard',
    'jaro',
    'jaro_winkler',
    'lcsseq',
    'lcsstr',
    'length',
    'levenshtein',
    'lzma_ncd',
    'matrix',
    'mlipns',
    'monge_elkan',
    'mra',
    'needleman_wunsch',
    'overlap',
    'postfix',
    'prefix',
    'ratcliff_obershelp',
    'rle_ncd',
    'smith_waterman',
    'sorensen',
    'sorensen_dice',
    'sqrt_ncd',
    'strcmp95',
    'tversky',
    'zlib_ncd',
]

def create_distance_matrix(pdbfile, quiet=False):
    derp = PDB.PDBParser(QUIET=quiet).get_structure('pdbfile', pdbfile)
    allatoms = [[atm for atm in res.get_atom()] for res in derp.get_residues()]
    atoms = list(chain(*allatoms))
    return [[rowat - colat for rowat in atoms] for colat in atoms]

def get_translation_table():
    '''
    take user input to select codon table
    table choices and species choices lists are created from
    >>> dir(CodonTable)
    >>> dir(CodonTable.table_choices[choice])
    select ambiguous|unambiguous
    select DNA|RNA
    return codon table from list
    '''
    table_choices = [
        'ambiguous_dna_by_name', 'ambiguous_generic_by_name', 'ambiguous_rna_by_name',
        'generic_by_name', 'standard_dna_table', 'standard_rna_table',
        'unambiguous_dna_by_name', 'unambiguous_rna_by_name'
    ]
    species_choices = [
        'Alternative Flatworm Mitochondrial', 'Alternative Yeast Nuclear', 'Archaeal', 'Ascidian Mitochondrial',
        'Bacterial', 'Blepharisma Macronuclear', 'Candidate Division SR1', 'Chlorophycean Mitochondrial', 'Ciliate Nuclear',
        'Coelenterate Mitochondrial', 'Dasycladacean Nuclear', 'Echinoderm Mitochondrial', 'Euplotid Nuclear',
        'Flatworm Mitochondrial', 'Gracilibacteria', 'Hexamita Nuclear', 'Invertebrate Mitochondrial',
        'Mold Mitochondrial', 'Mycoplasma', 'Pachysolen tannophilus Nuclear Code', 'Plant Plastid',
        'Protozoan Mitochondrial', 'Pterobranchia Mitochondrial', 'SGC0', 'SGC1', 'SGC2', 'SGC3',
        'SGC4', 'SGC5', 'SGC8', 'SGC9', 'Scenedesmus obliquus Mitochondrial', 'Spiroplasma', 'Standard',
        'Thraustochytrium Mitochondrial', 'Trematode Mitochondrial', 'Vertebrate Mitochondrial', 'Yeast Mitochondrial',
    ]
    codontable = 0
    print('please select rna or dna, ambiguous or unambiguous.')
    for index, table in enumerate(table_choices):
        print('{}) {}'.format(index, table))
    codontable = input('please enter table number: ')
    codontable = int(codontable)
    tablechoice = table_choices[codontable]
    if tablechoice == 'standard_dna_table' or tablechoice == 'standard_rna_table':
        return CodonTable.__dict__[tablechoice].forward_table

    speciestable = 0
    print('please select rna or dna, ambiguous or unambiguous.')
    for index, table in enumerate(species_choices):
        print('{}) {}'.format(index, table))
    speciestable = input('please enter table number: ')
    speciestable = int(speciestable)
    specieschoice = species_choices[speciestable]
    if tablechoice == 'ambiguous_dna_by_name' or tablechoice == 'ambiguous_generic_by_name' or tablechoice == 'ambiguous_rna_by_name':
        return CodonTable.__dict__[tablechoice][specieschoice].forward_table.forward_table

    return CodonTable.__dict__[tablechoice][specieschoice].forward_table


def naive_backtranslate(seq_object: str) -> List:
    '''
    parse given seq_object argument into peptide string
    back translate each amino acid to its potential codons
      i.e. reverse the codon table, keeping codons in a list
      if there is more than one for any given amino acid
    eg:
    >>> table = table_choices[codontable]
    >>> species = species_choices[speciestable]
    >>> cerp = CodonTable.__dict__[table][species].forward_table
    >>> newcerp = dict()
    >>> for cod, ami in cerp.items():
    >>>     if ami not in newcerp.keys():
    >>>         newcerp[ami] = [cod]
    >>>     else:
    >>>         newcerp[ami].append(cod)
    >>> print(newcerp)
    >>> new_seq_object = [newcerp[ami] for ami in seq_object]
    >>> new_seq_lengths = [len(codons) for codons in new_seq_object]
    >>> total_permutations = reduce(lambda x,y:x*y, new_seq_lengths)
    >>> print(total_permutations)
    >>> print('there are: ', len(str(total_permutations)), ' digits in the number of total permutations')
    '''
    target_codon_table = get_translation_table()
    back_table = dict()
    for codon, amino in target_codon_table.items():
        if amino not in back_table.keys():
            back_table[amino] = [codon]
        else:
            back_table[amino].append(codon)
    new_seq_object = [back_table[amino] for amino in seq_object]
    return new_seq_object

def get_peptide_index(nuc_sequence: str, prot_sequence: str, codon_count: int) -> None:
    '''
    1. use naive_backtrace to get list of codons for each amino
    2. calculate Cartesian product of potential input codons
      - this creates potential nucleotide sequences to check for
    3. get index of each potential sequence in nuc_sequence
    '''
    potential_codons = naive_backtranslate(prot_sequence)[:codon_count]
    search_nucs = list(product(*potential_codons))
    for seq in search_nucs:
        seq_string = ''.join(seq)
        try:
            return nuc_sequence.index(seq_string)
            # to print all indices, but only works if looking for a single nucleotide:
            # [index for index, value in enumerate(nuc_sequence) if value == seq_string]
        except ValueError:
            continue

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
    return plt

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
    '''
    return plot object of 20 most common trigrams
    call `plt.show()` or `plt.savefig()` to use it
    '''
    gramCount = Counter(make_trigrams(sequence)).most_common(20)
    lab, val = zip(*gramCount)
    plt.bar(lab, val)
    plt.xticks(rotation=90)
    return plt

def get_peptide_toplot(sequence):
    peptide_alphabet = 'ACDEFGHIKLMNPQRSTVWYBXZJUO*'
    if (type(sequence)==Seq.Seq and sequence.alphabet.letters==peptide_alphabet):
        return sequence
    elif type(sequence)==SeqRecord.SeqRecord:
        return sequence.seq.transcribe().translate()
    elif type(sequence)==Seq.Seq:
        return sequence.transcribe().translate()
    elif type(sequence)==str:
        return Seq.Seq(sequence).transcribe().translate()
    else:
        raise TypeError('sequence was type: {}, need Biopython.SeqRecord, Biopython.Seq.Seq, or str type'.format(type(sequence)))

def peptide_distribution(sequence, **kwargs):
    plt.hist(get_peptide_toplot(sequence))
    return plt

def plot_ABI(abifilename):
    record = get_abi(abifilename)
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
    return plt

def get_abi(abifile):
    return SeqIO.read(abifile, 'abi').seq

def get_genbank(gb_file):
    return SeqIO.read(gb_file, 'genbank').seq

def get_fasta(fs_file):
    return SeqIO.read(fs_file, 'fasta').seq

def get_seq(fs_file):
    ext = Path(fs_file).suffixes[0].strip('.')
    print(f'get_seq retrieving file:\n{fs_file}')
    if ext == 'abi': return get_abi(fs_file)
    elif ext == 'gbk': return get_genbank(fs_file)
    elif ext == 'gb': return get_genbank(fs_file)
    elif ext == 'fasta': return get_fasta(fs_file)
    else: return SeqIO.SeqRecord()

def calc_sequence_similarity(func, seq1, seq2, queue):
    result = TD.__dict__[func](seq1, seq2)
    if queue:
        queue.put({func:result})
    else: return {func:result}

def multiprocTextfuncs(seq1, seq2):
    '''
    note this pegs all cores on my old i5 for about a minute
    using genbank files < 1MB
    >>> import viz
    >>> seq1 = viz.get_genbank('sequence.gb')
    >>> seq2 = viz.get_genbank('sequence2.gb')
    >>> resultlist = viz.multiprocTextfuncs(seq1,seq2)
    >>> resultdict = {k:v for x in resultlist for k,v in x.items()}
    '''
    jobs = []
    results = []
    queue = mp.Queue()
    for funcname in textdistfuncs:
        p = mp.Process(target=calc_sequence_similarity, args=(funcname, seq1, seq2, queue))
        jobs.append(p)
        p.start()
    for job in jobs:
        res = queue.get()
        results.append(res)
    for job in jobs:
        job.join()
    return results


def make_parser():
    parser = argparse.ArgumentParser(
        description='Basic genomic visualisation and stats',
        epilog='''Plots an abi trace, or distributions of codons
                  or amino acids.''')
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
    parser.add_argument('-nbt', '--naive_backtrace',
        help='''give indices of protein sequence in DNA sequence
        pass in a genbank or fasta file with the -f switch, and pass
        in a text file following this switch, witn ONLY the peptide
        sequence as a single line inside the file.''',
        default=None,
        nargs='?',
        type=argparse.FileType('r'))
    parser.add_argument('-dmat', '--distance_matrix',
        help='''give the name of a pdbfile, get a distrance matrix of all atoms
        in the protein''',
        default=None,
        nargs='?',
        type=argparse.FileType('r'))
    return parser

def main(args):
    if args.filename:
        ext = {'gbk':'genbank','fasta':'fasta'}
        filename, filetype = args.filename.name.split('.')
        sequence = SeqIO.read(args.filename, filetype)
        if args.abi_trace:
            abiplot = plot_ABI(sequence)
            fname = f"{filename}_abiplot.png"
            fpath = os.path.join(PLOTDIR, fname)
            abiplot.savefig(fpath, transparent=True, bbox_inches='tight')
            print('abiplot.png created')
        if args.nucleotide_distribution:
            nucplot = nucleotide_distribution(sequence, normed=args.normed)
            fname = f"{filename}_nucplot.png"
            fpath = os.path.join(PLOTDIR, fname)
            nucplot.savefig(fpath, transparent=True, bbox_inches='tight')
            print('nucplot.png created')
        if args.peptide_distribution:
            pepplot = peptide_distribution(sequence, normed=args.normed)
            fname = f"{filename}_pepplot.png"
            fpath = os.path.join(PLOTDIR, fname)
            pepplot.savefig(fpath, transparent=True, bbox_inches='tight')
            print('pepplot.png created')
        if args.naive_backtrace:
            prot_seq = args.naive_backtrace.read()
            sys.stdout.write(str(get_peptide_index(str(sequence.seq), prot_seq, 3)))
    if args.distance_matrix:
        sys.stdout.write(str(create_distance_matrix(args.distance_matrix.name, quiet=True)))
    elif args.demonstrate:
        demoplot = demo_dna_features_viewer()
        fpath = os.path.join(PLOTDIR, 'demoplot.png')
        demoplot.savefig(fpath, transparent=True, bbox_inches='tight')
        print('demoplot.png created')

if __name__ == '__main__':
    parser = make_parser()
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(args)
