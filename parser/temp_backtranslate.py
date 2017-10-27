#!/usr/bin/env python
# see fastfind paper here:
# https://bmcbioinformatics.biomedcentral.com/track/pdf/10.1186/1471-2105-7-1?site=bmcbioinformatics.biomedcentral.com
# 1. define codon table
codon_table = {
    'A': ('GCT', 'GCC', 'GCA', 'GCG'),
    'C': ('TGT', 'TGC'),
    'D': ('GAT', 'GAC'),
    'E': ('GAA', 'GAG'),
    'F': ('TTT', 'TTC'),
    'G': ('GGT', 'GGC', 'GGA', 'GGG'),
    'I': ('ATT', 'ATC', 'ATA'),
    'H': ('CAT', 'CAC'),
    'K': ('AAA', 'AAG'),
    'L': ('TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'),
    'M': ('ATG',),
    'N': ('AAT', 'AAC'),
    'P': ('CCT', 'CCC', 'CCA', 'CCG'),
    'Q': ('CAA', 'CAG'),
    'R': ('CGT', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'),
    'S': ('TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'),
    'T': ('ACT', 'ACC', 'ACA', 'ACG'),
    'V': ('GTT', 'GTC', 'GTA', 'GTG'),
    'W': ('TGG',),
    'Y': ('TAT', 'TAC'),
    '*': ('TAA', 'TAG', 'TGA'),
}

# 2. create dictionary of base possibilities mapped to ambiguous bases 
ambiguous_bases = {
    frozenset(['A']): 'A',
    frozenset(['C']): 'C',
    frozenset(['G']): 'G',
    frozenset(['T']): 'T',
    frozenset(['U']): 'T',
    frozenset(['A', 'G']): 'R',
    frozenset(['C', 'T']): 'Y',
    frozenset(['G', 'C']): 'S',
    frozenset(['A', 'T']): 'W',
    frozenset(['G', 'T']): 'K',
    frozenset(['A', 'C']): 'M',
    frozenset(['C', 'G', 'T']): 'B',
    frozenset(['A', 'G', 'T']): 'D',
    frozenset(['A', 'C', 'T']): 'H',
    frozenset(['A', 'C', 'G']): 'V',
    frozenset(['A', 'C', 'G', 'T']): 'N',
}

# 3. naively determine ambiguous codons from ambiguous bases
ambiguous_codon_table = {}
for amino_acid, codons in codon_table.iteritems():
    ambiguous_codon = ''
    for i in range(3): # len(codon)
        bases = frozenset([codon[i] for codon in codons])
        ambiguous_codon += ambiguous_bases[bases]
    ambiguous_codon_table[amino_acid] = (ambiguous_codon,)

# 4. correct the incorrectly determined codons from 2 
ambiguous_codon_table['L'] = ('TTR', 'CTN')
ambiguous_codon_table['R'] = ('CGN', 'AGR')
ambiguous_codon_table['S'] = ('TCN', 'AGY')
ambiguous_codon_table['*'] = ('TAR', 'TGA')

# backtranslation functions that work for any string with a codon_table that is
# a dict mapping characters to a sequence of strings.

def backtranslate_permutations(protein, codon_table=codon_table):
    '''Returns the number of back-translated nucleotide sequences for a protein
    and codon table combination.

    >>> protein = 'ACDEFGHIKLMNPQRSTVWY*'
    >>> backtranslate_permutations(protein)
    1019215872
    >>> backtranslate_permutations(protein, codon_table=ambiguous_codon_table)
    16
    '''
    permutations = 1
    for amino_acid in protein:
        permutations *= len(codon_table[amino_acid])
    return permutations

def backtranslate(protein, codon_table=codon_table):
    '''Returns the back-translated nucleotide sequences for a protein and codon 
    table combination.

    >>> protein = 'FVC'
    >>> len(backtranslate(protein))
    16
    '''
    # create initial sequences == list of codons for the first amino acid
    sequences = [codon for codon in codon_table[protein[0]]]
    for amino_acid in protein[1:]:
        # add each codon to each existing sequence replacing sequences
        # leaves (num_codons * num_sequences) for next amino acid 
        to_extend = sequences
        sequences = []
        for codon in codon_table[amino_acid]:
            for sequence in to_extend:
                sequence += codon
                sequences.append(sequence)
    return sequences

# 5. reverse ambiguous_bases to get a kind of codon table 
ambiguous_bases_reversed = dict((value, sorted(list(key))) for (key, value) in ambiguous_bases.iteritems())

# 6. Reuse the backtranslation functions with ambiguous nucleotides instead
def disambiguate(ambiguous_dna):
    '''Call backtranslate with ambiguous DNA and reversed ambiguous bases.

    >>> ambiguous_dna = 'ACGTRYSWKMBDHVN'
    >>> backtranslate_permutations(ambiguous_dna, ambiguous_bases_reversed)
    20736
    >>> len(disambiguate(ambiguous_dna))
    20736
    '''
    return backtranslate(ambiguous_dna, ambiguous_bases_reversed)

if __name__ == '__main__':
    import doctest
    doctest.testmod()


def clean_sequence( sequence ):
    """Given a sequence string, return a crap-free, standardized DNA version."""
    s = sequence.replace( '\r', '' ).split( '\n' )  # separate each line
    if s[0][0] == '>': s = s[ 1 :]                  # remove defline
    s = ''.join( s )                                # make one long string
    s = s.replace( ' ', '' ).replace( '\t', '' )    # remove spaces
    return s.upper().replace( 'U', 'T' )

# Then, a function to let you know if there are characters in your sequence that shouldn’t be:
def report_bad_chars( sequence ):
    """Given a string 'sequence', return a dictionary of any non-AGCT characters."""
    bad_chars = {}
    for l in sequence:
        if l not in 'AGCT':
            if l in bad_chars: bad_chars[ l ] += 1
            else: bad_chars[ l ] = 1
    if bad_chars != {}: print( bad_chars )

# After the jump, functions for translation, calculating amino acid and nucleotide frequencies, and making random DNA sequences.

# To make a random DNA sequence:
import random
 
def random_sequence( length ):
    """Return a random string of AGCT of size length."""
    return ''.join([ random.choice( 'AGCT' ) for i in range(int( length ))])

And to get the frequency of each nucleotide:
def nuc_frequencies( sequence ):
    """Return a dictionary of base:frequency pairs."""
    return { b: sequence.count(b)/len(sequence) for b in 'AGCT'}

# A genetic code table (as a dictionary):
gencode = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
    'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

# And the function for translation (using the above table):
def translate( sequence ):
    """Return the translated protein from 'sequence' assuming +1 reading frame"""
    return ''.join([gencode.get(sequence[3*i:3*i+3],'X') for i in range(len(sequence)//3)])

# Lastly, to get a codon distribution:
def codon_dict( filler=0 ):
    """Return a dictionary of codon:filler pairs for all 64 codons."""
    d = {}
    for one in 'AGCT':
        for two in 'AGCT':
            for three in 'AGCT':
                d.update({ one+two+three:filler })
    return d
 
def codon_frequencies( seq ):
    """Return a dictionary of codon:frequency pairs for all 64 codons."""
    table = codon_dict()
    for i in range(len(seq)):
        try: table[seq[i:i+3]] += 1
        except: pass
    seq = seq[::-1]
    for i in range(len(seq)):
        try: table[seq[i:i+3]] += 1
        except: pass
    return table
    