from difflib import SequenceMatcher

def seqmatcher(tok_lst1,tok_lst2):
    matcher = SequenceMatcher(None, tok_lst1, tok_lst2)
    lst1_2_diffs = [x for x in matcher.get_opcodes() if x[0] != "equal"]
    SeqMatcher = []
    for tag, i1, i2, j1, j2 in lst1_2_diffs:
        SeqMatcher.append((tag, " ".join(tok_lst1[i1:i2]).strip(), " ".join(tok_lst2[j1:j2]).strip()))
    edits = "\n".join([str(x) for x in SeqMatcher])
    return edits.strip()
