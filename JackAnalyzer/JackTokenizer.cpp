#include <iostream>
#include <fstream>
#include <cctype>
#include "Analyzer.h"

bool isEpsilon(char);

JackTokenizer::JackTokenizer(std::string fileName):file(fileName){}

bool JackTokenizer::hasMoreTokens(){
    char k{};
    while (true){
        k=file.peek();
        if (k == std::ifstream::traits_type::eof()) {
            return 0;
        }
        if (isEpsilon(k)){
            file.ignore();
        } else {
            return 1;
        }
    }
}

bool isSymbol(char ch){
    char symbols[19] = {'{','}','[',']','(',')','.',',',';','+','-','*','/','&','|','<','>','=','~'};
    for (char& sym:symbols){
        if (ch==sym) return 1;
    }
    return 0;
}
bool isEpsilon(char ch){
    return (ch==' '||ch=='\n'||ch=='\t');
}
bool isKeyword(std::string& s){
    std::string kws[21] = {
        "class", "method", "function", "constructor",
        "int", "boolean", "char", "void", "var", "static",
        "field", "let", "do", "if", "else", "while",
        "return", "true", "false", "null", "this"
    };
    for (std::string& st:kws){
        if (s==st) return 1;
    }
    return 0;
}

void JackTokenizer::advance(){
    std::string a{};
    while (true){
        char b{};
        char k=file.peek();
        //symbol
        if (isSymbol(k)){
            tokenType=Token::SYMBOL;
            file.get(b);
            k=file.peek();
            if (k=='/' && b=='/'){
                file.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                continue;
            } else{
                if      (b=='<') a="&lt;";
                else if (b=='>') a="&gt;";
                else if (b=='"') a="&quot;";
                else if (b=='&') a="&amp;";
                else    a=b;
                break;
            }
        //alpabet
        } else if   ((std::isalpha(k)) || (k=='_')){
            while(true){
                file.get(b);
                a+=b;
                k=file.peek();
                if (!(std::isalpha(k) || std::isdigit(k) || (k=='_'))){
                    break;
                }
            }
            if (isKeyword(a)){
                tokenType=Token::KEYWORD;
            } else {
                tokenType=Token::IDENTIFIER;
            }
            break;
        //numeric
        } else if   (std::isdigit(k)){
            tokenType=Token::INT_CONST;
            while(true){
                file.get(b);
                a+=b;
                k=file.peek();
                if (!std::isdigit(k)){
                    break;
                }
            }
            break;
        //string
        } else if   (k=='\"'){
            tokenType=Token::STRING_CONST;
            file.ignore();
            while(true){
                k=file.peek();
                if (k=='\"'){
                    file.ignore();
                    break;
                } else {
                    file.get(b);
                    a+=b;
                }
            }
            break;
        } else {
            file.ignore();
            continue;
        }
    }


    currentToken=a;
}