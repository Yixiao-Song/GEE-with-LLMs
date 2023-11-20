# code
`prompts`:
- `de_gpt4_end2end_prompt_utils.py`: prompts used for Section 3 in the paper
- `de_prompt_utils.py`: prompts for German atomic edit extraction and explanation generation
- `zh_prompt_utils.py`: prompts for Chinese atomic edit extraction and explanation generation

`fine-tune_llama2-7b`:
- `fine-tune_llama2-7b.sh`: parameters for fine-tuning the model
- `qlora.py`: see source code [here](https://github.com/artidoro/qlora/blob/main/qlora.py)

`rule_based_screening.py`: the heuristic rules for screening out low-level mistakes in atomic edit extraction

`SequenceMatcher_rough_edits.py`: use SequenceMatcher from difflib to extract rough edits

# data

`fine-tune_data`: the training and test data of LLM fine-tuning for German and Chinese atomic edit extraction. The data is in the format for fine-tuning ChatGPT. `Sentence pair` is the source and target sentence; `list of edits` are the rough edits extracted by SequenceMatcher; `list of labels` are the labels of the edits; `content` is the gold atomic edits.

`human_annotation_data`: the anonymized raw human annotation data

# Sentence aligner
We modify the paragraph aligner from [here](https://github.com/katherinethai/par3/tree/main/par3_align) to align sentences in the datasets.