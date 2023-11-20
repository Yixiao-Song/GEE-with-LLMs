extraction_prompt = """This is an atomic edit extraction task. Given a pair of German sentences and the edits applied to the first sentence to get the second sentence, your task is to break down the edits to the atomic level (i.e., token level) and assign the edit a label. Be case sensitive. Pay attention to punctuation marks and relocated tokens. Pay attention to phonetic similarity when aligning tokens.

Labels:
1. [replace, original_token, editted_token]
2. [delete, original_token, ""]
3. [insert, "", editted_token]
4. [relocate, original_token, editted_token]: pay attention to tokens that are deleted then added again; the relocated token must be the same before and after the edit.

Examples:
Wie oben schon erwähnt ist die Chance erwisht zurweden zwar gering, aber sie ver handen.
Wie oben schon erwähnt ist die Chance, erwischt zu werden, zwar gering, aber sie ist vorhanden.
Edits:
('replace', 'erwisht zurweden', ', erwischt zu werden ,')
('replace', 'ver handen', 'ist vorhanden')
Atomic edits:
["insert", "", ","]
["replace", "erwisht", "erwischt"]
["replace", "zurweden", "zu werden"]
["insert", "", ","]
["insert", "", "ist"]
["replace", "ver handen", "vorhanden"]

ich haben essen zwei Bananen.
Ich habe zwei Bananen gegessen.
Edits:
('replace', 'ich haben essen', 'Ich habe')
('insert', '', 'gegessen')
Atomic edits:
["replace", "ich", "Ich"]
["replace", "haben", "habe"]
["delete", "essen", ""]
["insert", "", "gegessen"]

Ich habe gegessen zwei Bananen.
Ich habe zwei Bananen gegessen.
Edits:
('delete', 'gegessen', '')
('insert', '', 'gegessen')
Atomic edits:
["relocate", "gegessen", "gegessen"]

Below is the sentence pair for you to work on. Follow the format in the examples strictly. 
{src}
{trg}
Edits:
{edits}
Atomic edits:
"""

explain_prompt = """You are given a pair of German sentences and a list atomic edits. An edit is an error in the first sentence, which is corrected in the second one. Generate a succinct explanation for each error using the template. After each explanation, give the error a type.

Template: The word X is deleted/inserted/replaced by Y/relocated because ...

Example:
Ich habe zwei Bananen für mein Katz gekauft.
Ich habe zwei Bananen für meine Katze gekauft.
Edits:
["replace", "Katz", "Katze"]
["replace", "mein", "meine"]
Explanation:
The word 'Katz' is replaced by 'Katze' because 'Katze' is the correct spelling.
Error type: spelling
The word 'mein' is replaced by 'meine' because it should agree with the gender and case of the word Katze, which is feminine and accusative.
Error type: gender and case

Er fliegt nächster Monat Deutschland.
Er fliegt nächsten Monat nach Deutschland.
Edits:
["insert", "", "nach"]
["replace", "nächster", "nächsten"]
Explanation:
The word 'nach' is inserted because the verb 'fliegen' requires a preposition when expressing a destination and 'nach' is usually used for countries.
Error type: preposition
The word 'nächster' is replaced by 'nächsten' because German uses accusative case for time expressions.
Error type: case

Ich gehe in der Schule.
Ich gehe in die Schule.
Edits:
["replace", "der", "die"]
Explanation:
The word 'der' is replaced by 'die' because the preposition 'in' requires the accusative case of a noun when expressing a direction or destination.
Error type: case

Ich kann heute jogge gehe.
Ich kann heute joggen gehen.
Edits:
["replace", "gehe", "gehen"]
["replace", "jogge", "joggen"]
Explanation:
The word "gehe" is replaced by "gehen" because the verb "kann" requires an infinitive form of the verb "gehen".
Error type: infinitive
The word "jogge" is replaced by "joggen" because the verb "gehen" requires an infinitive form of the verb "joggen".
Error type: infinitive

Ich muss mich zur neuen Umgebung gewöhnen.
Ich muss mich an die neue Umgebung gewöhnen.
Edits:
["replace", "zur", "an"]
["insert", "", "die"]
["replace", "neuen", "neue"]
Explanation:
The word "zur" is replaced by "an" because the verb "gewöhnen" requires the preposition "an".
Error type: preposition
The word "die" is inserted because the noun "Umgebung" requires a determiner and "gewöhnen an" requires accusative case.
Error type: determiner
The word "neuen" is replaced by "neue" because the existence of "die" indicates that the adjective need only weak inflection.
Error type: adjective inflection

Es ist im Ende des Flusses.
Es ist am Ende des Flusses.
Edits:
["replace", "im", "am"]
Explanation:
The word "im" is replaced by "am" because "am" is the correct preposition for the word "Ende".

Below is the sentence pair for you to work on. Focus on the given edit and do not add other atomic edits. Start with the explanation directly.
{src}
{trg}
Edits:
{edit}
Explanation:"""
