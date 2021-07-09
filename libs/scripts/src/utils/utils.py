import os


def return_file_names_with_extension(path, extension=""):
    return list(filter(lambda file: file.endswith(extension), os.listdir(path)))


def obj_to_str(obj):
    obj_dict = {}
    not_private_fields = list(filter(lambda field: not field.startswith("__") 
                                                    and not field.endswith("__"), dir(obj)))

    for field in not_private_fields:
        if getattr(obj, field):
            obj_dict[field] = getattr(obj, field)
    return str(obj_dict)

def return_to_prev_page(iterator, len):
    for i in range(1, len - 1):
        next(iterator)
    return iterator