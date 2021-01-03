class CompanyInfoRepository:

    def getAll(self):
        from domain.company_info import CompanyInfo
        c = CompanyInfo.query.all()
        return c

    def getOne(self, id):
        from domain.company_info import CompanyInfo
        c = CompanyInfo.query.get(id)
        return c

    def add(self, c):
        from controller import db
        db.session.add(c)
        db.session.commit()
        return c

    def remove(self, c):
        from controller import db
        db.session.delete(c)
        db.session.commit()

    def update(self, c):
        from controller import db
        from domain.company_info import CompanyInfo
        found = CompanyInfo.query.get(c.get_id())
        found.set_name(c.get_name())
        found.set_city(c.get_city())
        found.set_street(c.get_street())
        found.set_streetNo(c.get_streetNo())
        found.set_phone(c.get_phone())
        found.set_fax(c.get_fax())
        found.set_fiscalCode(c.get_fiscalCode())
        found.set_bank(c.get_bank())
        found.set_iban(c.get_iban())
        found.set_legalRepresentative(c.get_legalRepresentative())
        db.session.commit()
        return c
