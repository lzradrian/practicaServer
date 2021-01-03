def get_fields_by_role(field_dict, role):
    return {key: value for (key, value) in field_dict.items() if value == role}


def write_to_file(filepath, data):
    with open(filepath, "w") as f:
        for k, v in data.items():
            f.write(str(k) + " " + str(v) + "\n")


def generate_pdf(pdf_input, pdf_output, data):
    pass
