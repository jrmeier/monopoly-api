def get_dot_notation(obj, dot_string):
    """
    Purpose: Get value from object where the key/path may not exist
    Params: 
        obj: Dictionary to search within
        dot_string: dot notation of path of where to look
    """

    if not dot_string:
        return
    dot_split = dot_string.split(".",1)
    if len(dot_split) <= 1:
        try:
            return obj[dot_split.pop()]
        except KeyError:
            return None

    if obj.get(dot_split[0]):
        new_obj = obj[dot_split[0]]
        new_dot_string = dot_split[1:].pop()
        return d(new_obj, new_dot_string)

    return None