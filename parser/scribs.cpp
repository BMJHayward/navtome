#include <map>
//leaving this here to try when there is a way around
//the unique keys requirement for boost::bimaps:
#include <boost/bimap.hpp> 

std::map <char, char> trnscrb;
trnscrb['A'] = 'A';
trnscrb['G'] = 'G';
trnscrb['T'] = 'U';
trnscrb['C'] = 'C';

std::map <char, char> revtrnscrb;
revtrnscrb['A'] = 'A';
revtrnscrb['G'] = 'G';
revtrnscrb['U'] = 'T';
revtrnscrb['C'] = 'C';

std::map <char, char> trnslt;
trnslt['UUU'] = 'Phe'
trnslt['UCU'] = 'Ser'
trnslt['UAU'] = 'Tyr'
trnslt['UGU'] = 'Cys'
trnslt['UUC'] = 'Phe'
trnslt['UCC'] = 'Ser'
trnslt['UAC'] = 'Tyr'
trnslt['UGC'] = 'Cys'
trnslt['UUA'] = 'Leu'
trnslt['UCA'] = 'Ser'
trnslt['UAA'] = 'STOP'
trnslt['UGA'] = 'STOP'
trnslt['UUG'] = 'Leu'
trnslt['UCG'] = 'Ser'
trnslt['UAG'] = 'STOP'
trnslt['UGG'] = 'Trp'
trnslt['CUU'] = 'Leu'
trnslt['CCU'] = 'Pro'
trnslt['CAU'] = 'His'
trnslt['CGU'] = 'Arg'
trnslt['CUC'] = 'Leu'
trnslt['CCC'] = 'Pro'
trnslt['CAC'] = 'His'
trnslt['CGC'] = 'Arg '
trnslt['CUA'] = 'Leu'
trnslt['CCA'] = 'Pro'
trnslt['CAA'] = 'Gln'
trnslt['CGA'] = 'Arg '
trnslt['CUG'] = 'Leu'
trnslt['CCG'] = 'Pro'
trnslt['CAG'] = 'Gln'
trnslt['CGG'] = 'Arg '
trnslt['AUU'] = 'Ile'
trnslt['ACU'] = 'Thr'
trnslt['AAU'] = 'Asn'
trnslt['AGU'] = 'Ser'
trnslt['AUC'] = 'Ile'
trnslt['ACC'] = 'Thr'
trnslt['AAC'] = 'Asn'
trnslt['AGC'] = 'Ser '
trnslt['AUA'] = 'Ile'
trnslt['ACA'] = 'Thr'
trnslt['AAA'] = 'Lys'
trnslt['AGA'] = 'Arg'
trnslt['AUG'] = 'Met'
trnslt['ACG'] = 'Thr'
trnslt['AAG'] = 'Lys'
trnslt['AGG'] = 'Arg '
trnslt['GUU'] = 'Val'
trnslt['GCU'] = 'Ala'
trnslt['GAU'] = 'Asp'
trnslt['GGU'] = 'Gly'
trnslt['GUC'] = 'Val'
trnslt['GCC'] = 'Ala'
trnslt['GAC'] = 'Asp'
trnslt['GGC'] = 'Gly'
trnslt['GUA'] = 'Val'
trnslt['GCA'] = 'Ala'
trnslt['GAA'] = 'Glu'
trnslt['GGA'] = 'Gly'
trnslt['GUG'] = 'Val'
trnslt['GCG'] = 'Ala'
trnslt['GAG'] = 'Glu'
trnslt['GGG'] = 'Gly'
