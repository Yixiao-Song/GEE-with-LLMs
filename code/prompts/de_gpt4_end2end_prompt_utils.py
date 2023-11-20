baseline_strong = """You are given a pair of German sentences. The first sentence contains one or more errors, which are corrected in the second one. Your task is to: (1) generate a succinct explanation for each error following the template; (2) assign the error a type.

Template: The word X is deleted/inserted/replaced by Y/relocated because ...

Example:
Ich habe zwei bananen für mein Katze gekauft.
Ich habe zwei Bananen für meine Katze gekauft.
Explanation:
The word 'bananen' is replaced by 'Bananen' because German nouns should be capitalized.
Error type: capitalization
The word 'mein' is replaced by 'meine' because it should agree with the gender and case of the word Katze, which is feminine.
Error type: gender and case agreement

Below is the sentence pair for you to work on. Start with the explanation directly.
{src}
{trg}
Explanation:"""

baseline_strong_atomic = """You are given a pair of German sentences. The first sentence contains one or more errors, which are corrected in the second one. The errors are listed below the sentence pair. Your task is to: (1) generate a succinct explanation for each error following the template; (2) assign the error a type.

Template: The word X is deleted/inserted/replaced by Y/relocated because ...

Example:
Ich habe zwei bananen für mein Katze gekauft.
Ich habe zwei Bananen für meine Katze gekauft.
Edits:
["replace", "bananen", "Bananen"]
["replace", "mein", "meine"]
Explanation:
The word 'bananen' is replaced by 'Bananen' because German nouns should be capitalized.
Error type: capitalization
The word 'mein' is replaced by 'meine' because it should agree with the gender and case of the word Katze, which is feminine.
Error type: gender and case agreement

Below is the sentence pair for you to work on. Start with the explanation directly.
{src}
{trg}
Edits:
{edits}
Explanation:"""