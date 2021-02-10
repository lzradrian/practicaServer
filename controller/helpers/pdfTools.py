def create_pdf(fisier_input_pdf, fisier_input_txt, fisier_output_pdf):
    '''
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
    :param fisier_input_txt: fisierul din care sa se creeze pdf-ul
    :param fisier_output_pdf: numele pdf-ului generat
    '''
    import os
    dir_location = os.getcwd()  # ..practicaServer\controller
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]

    dir_location = dir_location[:-1] + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)
    print(os.getcwd())
    print("nume fisie:" + fisier_input_txt)
    os.system('cmd /c "FormEditor ' + fisier_input_pdf + ' ' + fisier_input_txt + ' ' + fisier_output_pdf)


def create_pdf_from_files_and_doc(fisier_input_pdf, fisier_output_pdf, doc):
    '''
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
    :param fisier_output_pdf: numele pdf-ului generat
    :param conventie: ConventieInput / AcordPractica
    '''
    import os

    dir_location = os.path.dirname(os.path.abspath(__file__))  # ..practicaServer\controller\helpers
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location = dir_location[:-1]
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location = dir_location[:-1]
    # dir_location = ..practicaServer

    # write content from conventie to file
    numeFisierTemporar = "temporar_file.txt"
    conventie_input_txt_location = dir_location + '\\forms\\' + numeFisierTemporar

    text_file = open(conventie_input_txt_location, "w+")
    text_file.write(doc.get_content())
    text_file.close()

    dir_location = dir_location + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)

    # generate pdf
    os.system('cmd /c "FormEditor ' + fisier_input_pdf + ' ' + numeFisierTemporar + ' ' + fisier_output_pdf)

    # delete used file
    os.remove(conventie_input_txt_location)


def create_pdf_from_dic(fisier_input_pdf, fisier_output_pdf,data):
    '''
       :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                                DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
       :param fisier_output_pdf: numele pdf-ului generat
       :param data: dict(zip(fields.keys(), params))
       output: generates a pdf file with given name
       '''
    import os
    dir_location = os.path.dirname(os.path.abspath(__file__))  # ..practicaServer\controller\helpers
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location = dir_location[:-1]
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]
    dir_location = dir_location[:-1]
    # dir_location = ..practicaServer

    # write content from conventie to file
    #input_txt_location = dir_location + '\\forms\\' + numeFisierTemporar



    dir_location = dir_location + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)

    numeFisierTemporar = "temporar_file.txt"
    with open(numeFisierTemporar, "w+") as f:
        for k, v in data.items():
            f.write(str(k) + " " + str(v) + "\n")

    # generate pdf
    os.system('cmd /c "FormEditor ' + fisier_input_pdf + ' ' + numeFisierTemporar + ' ' + fisier_output_pdf)

    content = open(fisier_output_pdf, 'rb').read()
    # delete used file
    os.remove(numeFisierTemporar)
    os.remove(fisier_output_pdf)

    return content


def _get_fields_from_pdf(pdf_filepath):
    import PyPDF2
    f = PyPDF2.PdfFileReader(pdf_filepath)
    return f.getFields()


def get_fields_from_pdf(pdf_content):
    import os
    with open('temp_pdf.pdf', "wb") as f:
        f.write(pdf_content)
    fields = _get_fields_from_pdf('temp_pdf.pdf')
    os.remove('temp_pdf.pdf')
    return fields


def are_no_hours_valid(current_year, start_date, end_date, no_hours):
    # current year - 2010
    # start date - "10.10.2010"
    # end date - "20.10.2010"
    import numpy as np
    import datetime as dt

    vacation_multiplier = 8
    college_multiplier = 2

    college_start = dt.date(current_year, 10, 1)
    college_end = dt.date(current_year + 1, 7, 1)

    start = dt.date(start_date.split('-')[2], start_date.split('-')[1], start_date.split('-')[0])
    end = dt.date(end_date.split('-')[2], end_date.split('-')[1], end_date.split('-')[0])

    amount = 0

    if start < college_start:
        if end < college_start:
            amount += np.busday_count(start, end) * vacation_multiplier
        else:
            amount += np.busday_count(start, college_start) * vacation_multiplier
            amount += np.busday_count(college_start + 1, end) * college_multiplier
    else:
        if end < college_end:
            amount += np.busday_count(start, end) * college_multiplier
        else:
            amount += np.busday_count(start, college_end) * college_multiplier
            amount += np.busday_count(college_end + 1, end) * vacation_multiplier

    return amount >= no_hours
