== Structure ==

=== Task ===
* ID SQL
* context (date/ordi/magasin/toilettes/nothing to do/work) 
(* project )
* taskname
* position
 

* pourquoi?
 * il ne 'devrait' pas y avoir 'trop' de taches ouvertes (backlog tant que running pas fini)
 * pas trouvé d'autre methode sauf pickle pour stocker des chained list
 * requete 'bourrine' du type: 
    UPDATE table SET position = 1 WHERE itemname = 'foo'
    UPDATE table SET position = position + 1 WHERE itemname != 'foo' AND position < 4

=== SQL ===
==== Create tables ====

  create table tasks( id INTEGER PRIMARY KEY, name text, context text, position NUMERIC);

