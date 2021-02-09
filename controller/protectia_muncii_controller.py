from flask import Blueprint, redirect, flash, render_template, session, request, url_for, Response

from controller.helpers.authorize import verify_role, get_home_route

protectia_muncii = Blueprint('protectia_muncii', __name__)


def get_students_with_documents():
    from service.utility import get_user_service, get_student_info_service,\
        get_declaratie_ubb_service, get_declaratie_firma_service

    user_service = get_user_service()
    student_info_service = get_student_info_service()
    declaratie_ubb_service = get_declaratie_ubb_service()
    declaratie_firma_service = get_declaratie_firma_service()

    students = user_service.filter_by_role(0)

    data = []
    for s in students:
        try:
            si = student_info_service.getOne(s.id)
            try:
                document = declaratie_ubb_service.get_with_student_id(s.id)
                document_type = "UBB"
                data.append((si.name, si.group, si.year, document_type, document.submitted, document.checked, ("UBB", document.id), len(data)))
            except ValueError:
                try:
                    document = declaratie_firma_service.get_with_student_id(s.id)
                    document_type = "Firma"
                    data.append((si.name, si.group, si.year, document_type, document.submitted, document.checked, ("Firma", document.id), len(data)))
                except ValueError:
                    pass
        except ValueError:
            continue
    return tuple(data)

@protectia_muncii.route('/download/<doc_type>&<doc_id>')
def download(doc_type, doc_id):
    from service.utility import get_declaratie_ubb_service, get_declaratie_firma_service
    content = None
    if doc_type == "UBB":
        service = get_declaratie_ubb_service()
        doc = service.getOne(int(doc_id))
        content = doc.content
    elif doc_type == "Firma":
        service = get_declaratie_firma_service()
        doc = service.getOne(int(doc_id))
        content = doc.content

    return Response(content, mimetype="application/pdf", headers={"Content-disposition": "attachment; "
                                                                                         "filename=declaratie.pdf"})

@protectia_muncii.route('/validate/<doc_idx>')
def validate(doc_idx):
    from service.utility import get_declaratie_ubb_service, get_declaratie_firma_service
    data = get_students_with_documents()
    headings = (("Nume", "Grupa", "An", "Tip document", "Data incarcarii", "Status", "Document"))
    doc = data[int(doc_idx)]
    doc_type = doc[-2][0]
    doc_id = doc[-2][1]
    if doc_type == "UBB":
        service = get_declaratie_ubb_service()
        doc_file = service.getOne(doc_id)
        doc_file.checked = True
        service.update(doc_file)
    elif doc_type == "Firma":
        service = get_declaratie_firma_service()
        doc_file = service.getOne(doc_id)
        doc_file.checked = True
        service.update(doc_file)
    data = get_students_with_documents()

    return render_template("protectiaMuncii/viewDocuments.html", headings=headings, data=data)


@protectia_muncii.route('/view_documents', methods=["GET", "POST"])
def view_documents():
    data = get_students_with_documents()
    headings = (("Nume", "Grupa", "An", "Tip document", "Data incarcarii", "Status", "Document"))
    return render_template("protectiaMuncii/viewDocuments.html", headings=headings, data=data)

@protectia_muncii.route('/protectia_muncii', methods=["GET"])
def home():
    if verify_role(4) == 0:
        return  redirect(url_for(get_home_route()))
    return render_template("protectiaMuncii/homeProtectiaMuncii.html")
