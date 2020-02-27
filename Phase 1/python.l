%{
#include <stdio.h> 
#include<stdlib.h>
#include "SymbolTable.h" 

extern FILE *yyin;
extern FILE *yyout;
	
int lineno = 1; // initialize to 1
void ret_print(char* token_type);

%}

%% 
\.  ret_print("DOT"); //return DOT; 
\n  lineno+=1;
#.* 
[ ] 
\t 
False  ret_print("FALSE"); //return FALSE; 
None  ret_print("NONE"); //return NONE; 
True  ret_print("TRUE"); //return TRUE; 
and  ret_print("LAND"); //return LAND; 
break  ret_print("BREAK"); //return BREAK; 
continue  ret_print("CONTINUE"); //return CONTINUE; 
elif  ret_print("ELIF"); //return ELIF;
del  ret_print("DEL");  //return DEL;
else  ret_print("ELSE");  //return ELSE;
for  ret_print("FOR");  //return FOR;
if  ret_print("IF");  //return IF;
in  ret_print("IN"); //return IN;
not  ret_print("NOT");  //return NOT;
or  ret_print("LOR"); //return LOR; 
while  ret_print("WHILE"); //return WHILE; 
input  ret_print("INPUT"); //return INPUT;
print  ret_print("PRINT"); //return PRINT; 
int  ret_print("INT");  //return INT;
float  ret_print("FLOAT");  //return FLOAT;
str  ret_print("STR"); //return STR; 
list  ret_print("LIST");  //return LIST;
split  ret_print("SPLIT"); //return SPLIT; 
map  ret_print("MAP"); //return MAP;
append  ret_print("APPEND");  //return APPEND;
pop  ret_print("POP");  //return POP;
insert  ret_print("INSERT");  //return INSERT;
len  ret_print("LEN");  //return LEN;
range  ret_print("RANGE"); //return RANGE;
;  ret_print("SEMI"); //return SEMI; 
:  ret_print("COLON"); //return COLON; 
,  ret_print("COMMA"); //return COMMA; 
\".*\"  ret_print("CSTR");  //return CSTR;
\*\*  ret_print("EPOP"); //return EPOP; 
\*  ret_print("MUL"); //return MUL;
\/  ret_print("DIV"); //return DIV;
\/\/  ret_print("FDIV"); //return FDIV;
\%  ret_print("MOD"); //return MOD;
\+  ret_print("ADD"); //return ADD;
\-  ret_print("SUB");  //return SUB;
=  ret_print("ASOP");  //return ASOP;
\<   ret_print("L");  //return L;
>  ret_print("G"); //return G;
'>='  ret_print("GE"); //return GE;
'<='  ret_print("LE"); //return LE;
'=='  ret_print("EOP"); //return EOP;
'!='  ret_print("NEOP"); //return NEOP;
\^  ret_print("XOR");  //return XOR;
\&  ret_print("BAND");  //return BAND;
\|  ret_print("BOR"); //return BOR;
\{  ret_print("LBRACE"); //return LBRACE; 
\}  ret_print("RBRACE"); //return RBRACE; 
\(  ret_print("LPAREN"); //return LPAREN;
\)  ret_print("RPAREN"); //return RPAREN;
\[  ret_print("LBRACKET"); //return LBRACKET;
\]  ret_print("RBRACKET"); //return RBRACKET;
[a-zA-Z_][a-zA-Z0-9_]*  ret_print("ID"); insert("ID",yytext,NULL,NULL,lineno);//return ID;
^[^a-zA-Z _] printf("ERROR (Wrong Identifier) at line no %d\n",lineno);
[0-9]*  ret_print("CINT");  //return CINT;
[0-9]*\.[0-9]*  ret_print("CFLOAT"); //return CFLOAT; 
. printf("Unknown Symbol %s at line no %d\n",yytext,lineno); 

%% 

int yywrap()  
{  
   //return 1;
}
void ret_print(char *token_type)
{
	printf("yytext: %s\ttoken: %s\tlineno: %d\n", yytext, token_type, lineno);
}

int main()
{
  yylex();
  printf("\nSymbol Table : \n");
  display();
}
