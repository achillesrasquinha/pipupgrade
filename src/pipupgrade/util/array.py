def compact(arr, type_ = list):
    return type_(filter(bool, arr))