import viz

testPDBfile = '''HEADER    EXTRACELLULAR MATRIX                    22-JAN-98   1A3I
TITLE     X-RAY CRYSTALLOGRAPHIC DETERMINATION OF A COLLAGEN-LIKE
TITLE    2 PEPTIDE WITH THE REPEATING SEQUENCE (PRO-PRO-GLY)
EXPDTA    X-RAY DIFFRACTION
AUTHOR    R.Z.KRAMER,L.VITAGLIANO,J.BELLA,R.BERISIO,L.MAZZARELLA,
AUTHOR   2 B.BRODSKY,A.ZAGARI,H.M.BERMAN
REMARK 350 BIOMOLECULE: 1
REMARK 350 APPLY THE FOLLOWING TO CHAINS: A, B, C
REMARK 350   BIOMT1   1  1.000000  0.000000  0.000000        0.00000
REMARK 350   BIOMT2   1  0.000000  1.000000  0.000000        0.00000
SEQRES   1 A    9  PRO PRO GLY PRO PRO GLY PRO PRO GLY
SEQRES   1 B    6  PRO PRO GLY PRO PRO GLY
SEQRES   1 C    6  PRO PRO GLY PRO PRO GLY
ATOM      1  N   PRO A   1       8.316  21.206  21.530  1.00 17.44           N
ATOM      2  CA  PRO A   1       7.608  20.729  20.336  1.00 17.44           C
ATOM      3  C   PRO A   1       8.487  20.707  19.092  1.00 17.44           C
ATOM      4  O   PRO A   1       9.466  21.457  19.005  1.00 17.44           O
ATOM      5  CB  PRO A   1       6.460  21.723  20.211  1.00 22.26           C
HETATM  130  C   ACY   401       3.682  22.541  11.236  1.00 21.19           C
HETATM  131  O   ACY   401       2.807  23.097  10.553  1.00 21.19           O
HETATM  132  OXT ACY   401       4.306  23.101  12.291  1.00 21.19           O
'''

def test_create_distance_matrix():
    pass

def test_get_translation_table():
    pass


def test_naive_backtranslate():
    pass

def test_get_peptide_index():
    pass

def test_demo_dna_features_viewer():
    pass

def test_ngrams():
    pass

def test_make_trigrams():
    pass

def test_nucleotide_distribution():
    pass

def test_get_peptide_toplot():
    pass

def test_peptide_distribution():
    pass

def test_plot_ABI():
    pass

def test_get_genbank_sequence():
    pass

def test_get_fasta_sequence():
    pass

def test_iter_calc_sequence_similarity():
    pass

def test_calc_sequence_similarity():
    pass

def test_multiprocess_similarity():
    result = viz.multiprocess_similarity
    print(result)

def test_make_parser():
    pass

def test_main():
    pass
