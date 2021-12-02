from odoo import models, fields, api, _


class ReportXlsx(models.TransientModel):
    _name = 'report.trans'
    value = fields.Integer(string='value input')

    def create_xlsx_monthly(self):
        print('aaa')
        return self.env.ref('depends_hr.partner_xlsx').report_action(self)


