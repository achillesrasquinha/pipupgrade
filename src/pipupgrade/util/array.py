def compact(arr, type_ = list):
    return type_(filter(bool, arr))

def squash(seq):
    value = seq

    if isinstance(value, (list, tuple)) and len(value) == 1:
        value = value[0]
    
    return value