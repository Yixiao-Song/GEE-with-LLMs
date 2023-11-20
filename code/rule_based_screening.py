import json
from ast import literal_eval

# file_dir = INPUT_FILE in jsonl format
# out_dir = OUTPUT_FILE in jsonl format
with open(file_dir, "r") as f:
    data = [json.loads(line) for line in f.readlines()]

out_lst = []
for dict in data:
    #dict = {src: str, trg: str, response: model_output_edit_str}
    src, trg = dict["src"], dict["trg"]
    # model_out = dict["ft_response"]
    model_out = dict['response']
    model_out_lst = [literal_eval(item) for item in model_out.split("\n")]
    clean_edit = []
    for edit in model_out_lst:
        type, orig, new = edit[0], edit[1], edit[2]
        if type not in ["delete", "insert", "relocate", "replace"]: continue
        elif type == "delete":
            if len(new.strip()) != 0: continue
            elif orig not in src: continue
            else: clean_edit.append(edit)
        elif type == "insert":
            if orig != "": continue
            elif new not in trg: continue
            else: clean_edit.append(edit)
        elif type == "relocate":
            if orig not in src: continue
            elif new not in trg: continue
            if orig != new: continue
            else: clean_edit.append(edit)
        elif type == "replace":
            if orig == new: continue
            elif orig not in src: continue
            elif new not in trg: continue
            elif len(new) == 0 or len(orig) == 0: continue
            else: clean_edit.append(edit)
            
    dict["rule-based"] = "\n".join([str(x) for x in clean_edit])
    out_lst.append(dict)

with open(out_dir, "w") as f:
    for dict in out_lst:
        json.dump(dict, f)
        f.write("\n")
