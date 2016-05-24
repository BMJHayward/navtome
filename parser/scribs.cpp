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
