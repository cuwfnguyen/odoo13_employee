from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.depends_hr.report_monthly'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, partners):
        res = self.env['check.time'].search([])
        sheet = workbook.add_worksheet('Timekeeping')
        bold = workbook.add_format({'bold': True})
        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 12)

        row = 0
        col = 0
        sheet.write(row, col, 'Date', bold)
        sheet.write(row, col+1, 'Name', bold)
        sheet.write(row, col+2, 'Timekeeping', bold)
        for rec in res:
            row += 1
            sheet.write(row, col, str(rec.check_in.date()))
            sheet.write(row, col+1, str(rec.employ_id.name))
            sheet.write(row, col+2, str(rec.timekeeping))


