from controller import db


class CompanyInfo(db.Model):
    __tablename__ = 'CompanyInfo'
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    city = db.Column("city", db.String)
    street = db.Column("street", db.String)
    streetNo = db.Column("streetNo", db.String)
    phone = db.Column("phone", db.String)
    fax = db.Column("fax", db.String)
    fiscalCode = db.Column("fiscalCode", db.String)
    bank = db.Column("bank", db.String)
    iban = db.Column("IBAN", db.String)
    legalRepresentative = db.Column("legalRepresentative", db.String)

    def __init__(self, idRepres, nameRepres, name, city, street, nr, phone, fax, fiscal, bank, iban):
        self._id = idRepres
        self.name = name
        self.city = city
        self.street = street
        self.streetNo = nr
        self.phone = phone
        self.fax = fax
        self.fiscalCode = fiscal
        self.bank = bank
        self.iban = iban
        self.legalRepresentative = nameRepres

    def set_id(self, value):
        self._id = value

    def set_name(self, value):
        self.name = value

    def set_city(self, value):
        self.city = value

    def set_street(self, value):
        self.street = value

    def set_streetNo(self, value):
        self.streetNo = value

    def set_phone(self, value):
        self.phone = value

    def set_fax(self, value):
        self.fax = value

    def set_fiscalCode(self, value):
        self.fiscalCode = value

    def set_bank(self, value):
        self.bank = value

    def set_iban(self, value):
        self.iban = value

    def set_legalRepresentative(self, value):
        self.legalRepresentative = value

    def get_id(self):
        return self._id

    def get_name(self):
        return self.name

    def get_city(self):
        return self.city

    def get_street(self):
        return self.street

    def get_streetNo(self):
        return self.streetNo

    def get_phone(self):
        return self.phone

    def get_fax(self):
        return self.fax

    def get_fiscalCode(self):
        return self.fiscalCode

    def get_bank(self):
        return self.bank

    def get_iban(self):
        return self.iban

    def get_legalRepresentative(self):
        return self.legalRepresentative
