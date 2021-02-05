def get_fields_by_role(field_dict, role):
    return {key: value for (key, value) in field_dict.items() if value == role}


def write_to_file(filepath, data):
    with open(filepath, "w") as f:
        for k, v in data.items():
            f.write(str(k) + " " + str(v) + "\n")


def generate_pdf(pdf_input, pdf_output, data):
    import os
    os.system(
        "C:\\Data\\Projects\\Practica\\practicaServer\\controller\\editor\\FormEditor.exe " + pdf_input + " " + pdf_output + " " + data)


def get_total_hours(activities):
    total_hours = 0
    for activity in activities:
        period = activity[0]
        total_hours += int(period.split("/")[1])
    return total_hours


def create_activity_html(parameters, output_filepath):
    html_content = ""
    html_content += "<html><head></head><body><p style=\"text-align:center; font-family:'Times New Roman'; font-size:" + \
                    "20px\"><b>RAPORTUL DE ACTIVITATE A STUDENTULUI</b></p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\"><b>Numele si prenumele studentului " \
                    "practicant: </b> " + parameters["name"] + " </p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\">Facultatea de " + parameters[
                        "faculty"] + "</p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\">Specializarea: " + parameters[
                        "specialization"] + "         Anul de studii:" + parameters["year"] + "</p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\"><b>Numele si prenumele tutorelui de " \
                    "practica:</b> " + \
                    parameters["tutor_name"] + "</p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\"><b>Data inceperii stagiului de " \
                    "practica:</b> " + \
                    parameters["start_date"] + "</p>" + \
                    "<p style=\"font-family:'Times New Roman'; font-size: 20px\"><b>Data finalizarii stagiului de " \
                    "practica:</b> " + \
                    parameters["end_date"] + "</p>"
    html_content += "<table style=\"border-collapse: collapse; width=100%\"><colgroup><col span='1' style='width: 20%;'><col span='1' style='width: 80%;'></colgroup><tr><td style=\"border: 1px solid black; text-align:center; font-family:'Times New Roman'; font-size:20px\">" +\
                    "Data/<br>perioada</td><td style=\"border: 1px solid black; text-align:center; font-family:'Times New Roman'; font-size:20px\">" +\
                    "Descrierea pe scurt a activitatilor realizate</td></tr>"
    activities = parameters["activities"]
    total_no_hours = get_total_hours(activities)
    from datetime import date
    today = date.today()
    d = today.strftime("%d.%m.%Y")
    for activity in reversed(activities):
        html_content += "<tr><td style=\"border: 1px solid black; text-align:center; font-family:'Times New Roman'; font-size:20px\">" + activity[0] + "</td><td style=\"border: 1px solid black; text-align:center; font-family:'Times New Roman'; font-size:20px\">" + activity[1] + "</td></tr>"
    html_content += "<tr><td style=\"border: 1px solid black; text-align:center; font-family:'Times New Roman'; font-size:20px\"></td><td style=\"border: 1px solid black; text-align:left; font-family:'Times New Roman'; font-size:20px\"><b>TOTAL ORE " + str(total_no_hours) + "</b></td></tr>"
    html_content += "</table>"
    html_content += "<p style=\"display: inline; float:left; font-family:'Times New Roman'; font-size: 20px\"><b>Data,</b></p><p style=\"display: inline; float:right; font-family:'Times New Roman'; font-size: 20px\"><b>Semnatura student,</b></p>"
    html_content += "<br><br><br><p>" + d + "</p>"
    html_content += "<p style=\"display: inline; float:right; font-family:'Times New Roman'; font-size: 20px\"><b>Aviz (semnatura) tutore de practica,</b></p>"
    html_content += "</body></html>"
    with open(output_filepath, "w") as f:
        f.write(html_content)

