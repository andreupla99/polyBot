grammar Poly;

//L'entrada pot ser una o varies líneas

root : (linea)+ EOF ;

linea : crea comentari? ENDL*
    | consulta comentari? ENDL*
    | imatge comentari? ENDL*
    | comentari ENDL*
    ;

//expr : crea comentari? | consulta comentari? | comentari ;

comentari : COM text;

text : anychar+ ;

crea : nom IGUAL poligon ;

poligon : parentesi
        | vertex 
        | nom
        | poligon UNION poligon
        | poligon INTER poligon
        | capsa
        | random
        ;

capsa : BOUND poligon ;

//unio : poligon UNION poligon ;

//interseccio : poligon INTER poligon ;

random : RAND DIGITS ;

parentesi : PARINI poligon PARFI ;

vertex : CORINI point+ CORFI ;

point : num num ;


nom : character+ ;

consulta : COLOR poligon DIVISOR rgb
        | PINTA poligon
        | AREA poligon
        | PERIMITER poligon
        | VERTICES poligon
        | CENTROID poligon
        | EQUAL poligon DIVISOR poligon
        | INSIDE poligon DIVISOR poligon
        | PINTA contingut
        ;

contingut : STR text STR ;

rgb : BRACEINI num num num BRACEFI ;

imatge : DRAW STR text STR (DIVISOR poligon)+ ;

//comandes
COLOR : 'color' ;
PINTA : 'print' ;
AREA : 'area' ;
PERIMITER : 'perimeter' ;
VERTICES : 'vertices' ;
CENTROID : 'centroid' ;
EQUAL : 'equal' ;
INSIDE : 'inside' ;
DRAW : 'draw' ;



anychar : character | DIVISOR | SIMBOL | UNION | INTER | BOUND | CORINI | CORFI | BRACEINI | BRACEFI | PARINI | PARFI;
character : DIGITS | LLETRA | GUIO | PUNT | MENYS;

num : MENYS? DIGITS (PUNT DIGITS)? ;

IGUAL : ':=' ;
UNION : '+' ;
INTER : '*' ;
BOUND : '#' ;
CORINI : '[' ;
CORFI : ']' ;
BRACEINI : '{' ;
BRACEFI : '}' ;
PARINI : '(' ;
PARFI : ')' ;
DIGITS : [0-9]+ ;
PUNT : '.' ;
DIVISOR : ',' ;
STR : '"' ;
ENDL : '\n';
LLETRA : 'a'..'z' | 'A'..'Z' ;
GUIO : '_';
MENYS : '-' ;
//ESPAI : ' ' ;
RAND : '!';
SIMBOL : '&' | '?' | ':' | ';' | '/' | '\\' | '\t' | '@' | '=' ;

WS : [ ]+ -> skip ;

COM : '//' ;
