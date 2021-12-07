from odoo import models, fields, api, _


class ReportXlsx(models.TransientModel):
    _name = 'report.trans'

    def create_xlsx_monthly(self):
        return self.env.ref('depends_hr.partner_xlsx').report_action(self)


