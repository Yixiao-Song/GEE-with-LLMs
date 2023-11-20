extraction_prompt_template = """You are a {language} teacher. Given a pair of {language} sentences and the edits applied to the input sentence to get the output sentence, your task is to break down the edits to the atomic level (i.e., token level) and assign the edit a label. Pay attention to punctuation marks and relocated tokens.

Labels:
1. [replace, original_token, editted_token]
2. [delete, original_token, ""]
3. [insert, "", editted_token]
4. [relocate, original_token1, editted_token1]: pay attention to tokens that are deleted then added again; the relocated token must be the same before and after the edit.

Examples:
我去市菜场水果买。
我去菜市场买水果。
Edits:
("replace", "市菜场水果买", "菜市场买水果")
Atomic edits:
["replace", "市菜场", "菜市场"]
["relocate", "水果", "水果"]

我吃了早饭今天。
我今天吃了早饭。
Edits:
("insert", "今天", "")
("delete", "", "今天")
Atomic edits:
["relocate", "今天", "今天"]

再子细的学习相关课题后，我意识到了这个问题的严重。
在仔细地学习了相关课题后，意识到了这个问题的严重性。
Edits:
("replace", "再子细的", "在仔细地")
("insert", "", "了")
("insert", "", "我")
("insert", "", "性")
Atomic edits:
["replace", "再", "在]
["replace", "子细", "仔细"]
["replace", "的", "地"]
["insert", "", "了"]
["insert", "", "我"]
["replace", "严重", "严重性"]

她打算明儿天的午前去北京。
她打算明天上午去北京。
Edits:
("replace", "明儿天的午前", "明天上午")
Atomic edits:
["replace", "明儿天", "明天"]
["delete", "的", ""]
["replace", "午前", "上午"]

Below is the sentence pair for you to work on. Follow the format in the examples strictly. 
{original_sentence}
{corrected_sentence}
Edits:
{edits}
Atomic edits:
"""

explain_prompt = """You are given a pair of Mandarin Chinese sentences and a list atomic edits. An edit is an error in the first sentence, which is corrected in the second one. Generate a succinct explanation for each error using the template. After each explanation, give the error a type.

Template: The word X is replaced by Y/deleted/inserted/relocated because ...

Example:
昨天我买四只平果们。
昨天我买了四个苹果。
Edits:
["insert", "", "了"]
["replace", "只", "个"]
["replace", "平果", "苹果"]
["delete", "们", ""]
Explanation:
The word '了' is inserted because '了' indicate the completion of the action '买'.
Error type: usage of '了'
The word '只' is replaced with '个' because '个' is the correct measure word for '苹果'.
Error type: measure word
The word '平果' is replaced with '苹果' because '苹果' is the correct word for 'apple'.
Error type: miswritten character/word
The word '们' is deleted because '们' is only used after pronouns or human nouns to indicate plurality.
Error type: '们'

间而说之，他唱地很好。
简而言之，他唱得很好。
Edits:
["replace", "间而说之", "简而言之"]
["replace", "地", "得"]
Explanation:
The word '间而说之' is replaced with '简而言之' because '简而言之' is the correct way of writing the phrase which means 'in short' or 'in brief'.
Error type: miswritten character/word
The word '地' is replaced with '得' because '得' is the correct 'de' particle to use when it follows a verb and the word after '得' modifies the verb.
Error type: "de" particles

许多人们做了一差误。
许多人犯了一个错误。
Edits:
["replace", "许多人们", "许多人"]
["replace", "做", "犯"]
["insert", "", "个"]
["replace", "差误", "错误"]
Explanation:
The word '许多人们' is replaced with '许多人' because when a noun is preceded by a numeral, the plural marker '们' is not needed.
Error type: '们'
The word '做' is replaced with '犯' because '犯' is the correct verb to use for the noun 'mistake'.
Error type: verb-object collocaiton
The word '个' is inserted because a measure word is needed between the numeral and the noun and '个' is the correct measure word for '错误'.
Error type: measure word
The word '差误' is replaced with '错误' because '差误' is not a word in Chinese and '错误' is the correct word for 'mistake'.
Error type: miswritten character/word

我在查找我的知音。
我在寻找我的知音。
Edits:
["replace", "查找", "寻找"]
Explanation:
The word '查找' is replaced with '寻找' because '查找' suggests a systematic and methodological search. It usually means searching for information or data. On the other hand, '寻找' suggests a more intangible search with a sense of exploration. '寻找' fits the context better.
Error type: word choice

Below is the sentence pair for you to work on. Focus on the given edit and do not add other atomic edits. Start with the explanation directly.
{src}
{trg}
Edits:
{edit}
Explanation:"""
