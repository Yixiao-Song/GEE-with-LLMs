# extraction prompt is used for atomic edit extraction task using gpt4, gpt3.5, and claude
extraction_prompt = """This is an atomic edit extraction task. Given a pair of English sentences and the edits applied to the first sentence to get the second sentence, your task is to break down the edits to the atomic level (i.e., token or phrase level) and assign the edit a label. Be case sensitive. Pay attention to punctuation marks and relocated tokens. Pay attention to phonetic similarity when aligning tokens.

Labels:
1. [replace, original_token, editted_token]
2. [delete, original_token, ""]
3. [insert, "", editted_token]
4. [relocate, original_token, editted_token]: pay attention to tokens that are deleted then added again; the relocated token must be the same before and after the edit.

Examples:
i don't have two babanas fr my cat
I won't have two bananas for my cat.
Edits:
('replace', 'i do', 'I wo')
('replace', 'babanas fr', 'bananas for')
('insert', '', '.')
Atomic edits:
["replace", "i", "I"]
["replace", "don't", "won't"]
["replace", "babanas", "bananas"]
["replace", "fr", "for"]
["insert", "", "."]

Despite of it is an industrial city. There is many shops and department stores.
Although it is an industrial city, there are many shops and department stores.
Edits:
('replace', 'Despite of', 'Although')
('replace', '. There is', ', there are')
Atomic edits:
["replace", "Despite of", "Although"]
["replace", ". There", ", there"]
["replace", "is", "are"]

There are a comercial zone along the widdest street in the city where you are able to find all kind of establishments; banks, bars, chemists, cinemas, pet shops, restaurants, fast food restaurants, groceries, travel agencies, supermarkets and other.
There is a commercial zone along the widest street of the city where you can find all kinds of businesses: banks, bars, chemists, cinemas, pet shops, restaurants, fast food restaurants, grocers, travel agencies, supermarkets and others.
Edits:
('replace', 'are', 'is')
('replace', 'comercial', 'commercial')
('replace', 'widdest', 'widest')
('replace', 'in', 'of')
('replace', 'are able to', 'can')
('replace', 'kind', 'kinds')
('replace', 'establishments ;', 'businesses :')
('insert', '', ',')
('replace', 'groceries', 'grocers')
('replace', 'other', 'others')
Atomic edits:
["replace", "are", "is"]
["replace", "comercial", "commercial"]
["replace", "widdest", "widest"]
["replace", "in", "of"]
["replace", "are able to", "can"]
["replace", "kind", "kinds"]
["replace", "establishments", "businesses"]
["replace", ";", ":"]
["insert", "", ","]
["replace", "groceries", "grocers"]
["replace", "other", "others"]

She don't see shoe you bought her.
She didn't see the shoes you bought her.
Edits:
('replace', 'do', 'did')
('replace', 'shoe', 'the shoes')
Atomic edits:
["replace", "don't", "didn't"]
["replace", "shoe", "the shoes"]

Below is the sentence pair for you to work on. Follow the format in the examples strictly. 
{src}
{trg}
Edits:
{edits}
Atomic edits:
"""

explain_prompt = """This is a grammar error explanation task. You are given a pair of English sentences and a list atomic edits. An edit is an error in the first sentence that is corrected in the second one. Generate a grammar explanation for each error using the format in the following examples. After each explanation, give the error a type.

The explanations need to be specific. Avoid explanations which only say that one word is more appropriate than another. Instead, explain why a word is more appropriate. For a word that is deleted, be sure to explain why it is not needed in a sentence.

Example:
He love watching birds. He devote much of his time to find bird all over the world.
He loves watching birds. He devotes much of his time to finding birds all over the world. 
Edits:
["replace", "love", "loves"]
["replace", "devote", "devotes"]
["replace", "find", "finding"]
["replace", "bird", "birds"]
Explanation:
The word 'love' is replaced by 'loves' because the subject 'he' requires the verb to be in the 3rd person singular form.
Error type: person and number
The word 'devote' is replaced by "devotes" because the subject 'he' requires the verb to be in the 3rd person singular form.
Error type: person and number
The word 'find' is replaced by 'finding' because the verb 'devotes to' requires the gerund (-ing) form of the verb 'find'.
Error type: word form
The word 'bird' is replaced by 'birds' because the plural form of 'bird' indicates multiple types/individuals of birds.
Error type: word form

However the chair only is for Charlotte. She uses it when she comes to villa during summer.
However, the chair is only for Charlotte. She uses it when she comes to the villa during summer
Edits:
["insert", "", ","]
["relocate", "only", "only"]
["insert", "", "the"]
["insert", "", "."]
Explanation:
A comma is inserted because it's commly inserted after 'however' which is used to introduce a contrast.
Error type: punctuation
The word 'only' is relocated from before 'is' to after 'is' because when 'be' is used as the main verb, 'only' usually follows 'be'.
Error type: word order
The word 'the' is inserted before 'villa' because it is needed to refer to a specific villa in the context.
Error type: determiner
A period is inserted at the end of the sentence because a period is commonly used to end a sentence.
Error type: punctuation

Its my pleasure to be invited to visit Shanghai. I really like the city, specially it's vitality.
It's my pleasure to be invited to visit Shanghai. I really like the city, especially its vitality.
Edits:
["replace", "Its", "It's"]
["replace", "specially", "especially"]
["replace", "it's", "its"]
Explanation:
The word 'Its' is replaced by "It's" because "It's" is the contraction of "It is" while "Its" is the possessive form of "it".
Error type: word form
The word 'specially' is replaced by 'especially' because 'especially' is commonly used to emphasize one thing over others. while "specially" means "for a special reason".
Error type: word choice

It's yours decision, you should take the responsibility of it and let others know once you make.
It's your decision. You should take the responsibility for it and let others know once you make it.
Edits:
["replace", "yours", "your"]
["replace", ", you", ". You"]
["replace", "of", "for"]
["insert", "", "it"]
Explanation:
The word 'yours' is replaced by 'your' because 'your' is the possesive form of 'you' which is followed by a noun while 'yours' is a pronoun that cannot be followed by a noun.
Error type: word form
', you' is replaced by '. You' because a period should be used to separate two independent clauses, and the beginning of the second clause should be capitalized.
Error type: punctuation
The word 'of' is replaced by 'for' because 'take the responsibility for' is the correct collocation.
Error type: collocation
A pronoun 'it' is inserted after 'make' because 'make' is a transitive verb and should be followed by an object.
Error type: missing word

Who I should talk to about get a new computer?
Who should I talk to about getting a new computer?
Edits:
["relocate", "should", "should"]
["replace", "get", "getting"]
Explanation:
The word 'should' is relocated from after 'I' to before 'I' because the word order of a question should be subject-auxiliary inversion.
Error type: word order
The word 'get' is replaced by 'getting' because the preposition 'about' requires the gerund (-ing) form of the verb 'get'.
Error type: word form

Below is the sentence pair for you to work on. Focus on the given edit and do not add other atomic edits. Start with the explanation directly.

{src}
{trg}
Edits:
{edit}
Explanation:"""