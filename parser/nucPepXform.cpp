#include <string>
#include <cmath>

class NucPepXform
{
    std::string baseDNA = "ACGT";
    std::string baseRNA = "ACGU";
    std::string basePEP = "KNKNTTTTRSRSIIMIQHQHPPPPRRRRLLLLEDEDAAAAGGGGVVVV.Y.YSSSS.CWCLFLF";


    int strToInt(std::string inStr, std::string inBase)
    {
        int retNum = 0;
        for (auto i:inStr)
        {
            retNum += pow(inBase.length(), inStr.length()-i-1) * (inBase.at(inStr.at(i)));
        }

        return retNum;
     };


    std::string intToStr(){};
};

