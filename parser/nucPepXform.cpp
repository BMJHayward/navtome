#include <cmath>
#include <exception>
#include <iostream>
#include <string>
#include <boost/algorithm/string.hpp>

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


    std::string intToStr(int inInt, std::string outBase, int maxDigits)
    {
        int remainder = inInt;
        std::string retStr = "";

        for (int i = maxDigits; i >= 0; --i)
        {
            retStr += outBase.at(trunc(remainder / (int)pow(outBase.length(), i)));
            remainder = trunc(remainder % (int)pow(outBase.length(), i));
        }

        return retStr;
    };


    std::string verify(std::string inStr, std::string strBase)
    {
        boost::to_upper(inStr);
        std::string outStr = "";

        for (auto i: inStr)
        {
            if (strBase.find(inStr.at(i)) >=0)
            { 
                outStr += inStr.at(i);
            } else {
                std::cout << inStr.at(i) << ": invalid character, removing from value." << std::endl;
            };
        };

        return outStr;
    };
};

