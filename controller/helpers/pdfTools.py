def create_pdf(fisier_input_pdf, fisier_input_txt , fisier_output_pdf):
    '''
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
    :param fisier_input_txt: fisierul din care sa se creeze pdf-ul
    :param fisier_output_pdf: numele pdf-ului generat
                                todo:Nu functioneaza, numele ramane Output.pdf
    '''
    import os
    dir_location = os.getcwd()  # ..practicaServer\controller
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]

    dir_location = dir_location[:-1] + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)
    print(os.getcwd())
    os.system('cmd /c "FormEditor '+fisier_input_pdf+' '+fisier_input_txt+' '+fisier_output_pdf)


def create_pdf_from_conventie(fisier_input_pdf,fisier_input_txt, fisier_output_pdf,conventie):
    '''
    :param fisier_input_pdf: AcordPractica.pdf / ConventiePractica.pdf / DeclaratieActivitateUBB.pdf
                             DeclaratieActivitateFirma.pdf / DeclaratieDeTraseu.pdf
    :param fisier_input_txt: numele fisierului creat temporar pentru generarea pdf-ului
    :param fisier_output_pdf: numele pdf-ului generat
                                todo:Nu functioneaza, numele ramane Output.pdf
    :param conventie: ConventieInput
    '''
    import os
    dir_location = os.getcwd()  # ..practicaServer\controller
    while dir_location[-1] != "\\":
        dir_location = dir_location[:-1]

    #write content from conventie to file
    conventie_input_txt_location = dir_location[:-1]+ '\\forms\\'+fisier_input_txt
    text_file = open(conventie_input_txt_location, "w+")
    text_file.write(conventie.get_content())
    text_file.close()

    dir_location = dir_location[:-1] + "\\forms\\FormEditor\\FormEditor\\bin\\Debug\\netcoreapp3.1"
    os.chdir(dir_location)

    #generate pdf
    os.system('cmd /c "FormEditor '+fisier_input_pdf+' '+fisier_input_txt+' '+fisier_output_pdf)

    #delete used file
    os.remove(conventie_input_txt_location)
