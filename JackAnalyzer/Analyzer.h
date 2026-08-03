#ifndef ANALYZER_H
#define ANALYZER_H

#include <string>
#include <fstream>

enum Token{
    KEYWORD, SYMBOL, IDENTIFIER, INT_CONST, STRING_CONST
};
enum Keyword{
    CLASS, METHOD, FUNCTION, CONSTRUCTOR, INT, BOOLEAN,
    CHAR, VOID, VAR,STATIC, FIELD, LET, DO, IF ,ELSE,
    WHILE, RETURN, TRUE, FALSE, NULL_K, THIS
};

class JackTokenizer {
    private:
    std::ifstream file;

    public:
    JackTokenizer(std::string fileName);

    bool hasMoreTokens();
    void advance();

    std::string currentToken{};
    Token tokenType{};
};

#endif