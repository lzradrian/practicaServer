from controller.helpers.emailTools import send_email


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

def remove_empty_lines(filename):
    """Overwrite the file, removing empty lines and lines that contain only whitespace."""
    with open(filename) as in_file, open(filename, 'r+') as out_file:
        out_file.writelines(line for line in in_file if line.strip())
        out_file.truncate()

def create_pdf_from_files_and_doc(fisier_input_pdf, fisier_output_pdf, doc,subject):
    '''
    Create a pdf and send email
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf

    :param fisier_output_pdf: numele pdf-ului generat
    :param doc : ConventieInput etc (objects)
    :param subject: subject of sending email; if subject = None email is not send
    returns content of created pdf
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
    #conventie_input_txt_location = dir_location + '\\forms\\' + numeFisierTemporar

    #text_file = open(conventie_input_txt_location, "w+")
    #text_file.write(doc.get_content())
    #text_file.close()

    dir_location = dir_location + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    text_file = open(dir_location+"\\"+numeFisierTemporar, "w+")
    text_file.write(doc.get_content())
    text_file.close()

    remove_empty_lines(dir_location+"\\"+numeFisierTemporar)
    f = open(dir_location+"\\"+numeFisierTemporar, 'r')
    file_contents = f.read()
    #print(file_contents)
    f.close()
    os.chdir(dir_location)


    # generate pdf
    os.system('cmd /c "FormEditor ' + fisier_input_pdf + ' ' + numeFisierTemporar + ' ' + fisier_output_pdf)
    if (subject != None):
        send_email(subject,None,dir_location+"\\"+fisier_output_pdf,fisier_output_pdf)


    if (subject ==None): #sa nu se efectueze cand apeleaza decanul, doar la student
        content = open(fisier_output_pdf, 'rb').read()
        os.remove(dir_location + "\\" + numeFisierTemporar)
        os.remove(dir_location + "\\" + fisier_output_pdf)
        return content

    os.remove(dir_location+"\\"+numeFisierTemporar)
    os.remove(dir_location+ "\\" +fisier_output_pdf)




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
