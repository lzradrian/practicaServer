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


def create_pdf_from_conventie(fisier_input_pdf, fisier_output_pdf, conventie):
    '''
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
    :param fisier_output_pdf: numele pdf-ului generat
    :param conventie: ConventieInput
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
    text_file.write(conventie.get_content())
    text_file.close()

    dir_location = dir_location + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)

    # generate pdf
    os.system('cmd /c "FormEditor ' + fisier_input_pdf + ' ' + numeFisierTemporar + ' ' + fisier_output_pdf)

    # delete used file
    os.remove(conventie_input_txt_location)