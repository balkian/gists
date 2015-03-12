def check_dict(indic, template):
    return all(item in indic.items() for item in template.items())
