def get_if_empty(a, b):
    return a if a else b
    
def list_filter(v, filter_):
    filtered = filter(filter_, v)
    filtered = list(filtered)

    return filtered