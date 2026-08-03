#include "Analyzer.h"
#include <string>
#include <fstream>
#include <iostream>

class JackAnalyzer{
    private:
        std::ofstream file;

    public:
    JackAnalyzer(std::string fileName):file(fileName){
        file << "<token>" << '\n';
    }

    void writeToken(std::string tokenName, std::string text){
        file << '<' << tokenName << "> " << text << " </" << tokenName << '>' << '\n';
    }
    void end(){
        file << "</token>";
        file.close();
    }
};

std::string stringifyToken(const Token& tokenType){
    switch (tokenType)
    {
    case Token::KEYWORD:
        return "keyword";
    case Token::SYMBOL:
        return "symbol";
    case Token::IDENTIFIER:
        return "identifier";
    case Token::INT_CONST:
        return "intergerConstant";
    case Token::STRING_CONST:
        return "stringConstant";
    default:
        return "";
    }
}

int main(int argc, char* argv[]){
    std::string fileName=argv[2];
    JackTokenizer JK{fileName};
    JackAnalyzer JA{"MainT.xml"};
    while(JK.hasMoreTokens()){
        JK.advance();
        JA.writeToken(stringifyToken(JK.tokenType),JK.currentToken);
    }
    JA.end();
    
    return 0;
}