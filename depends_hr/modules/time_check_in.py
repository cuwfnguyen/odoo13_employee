from odoo import models, fields, api
import datetime
from datetime import datetime
from datetime import timedelta


class TimeKeeping(models.Model):

    _name = 'time.check.in'
    employee_id = fields.Integer()
    time_check_in = fields.Datetime('Check time', store=True)
    list_id = []

    def _compute_timesheet(self):
        rec = self.env['time.check.in'].search([])
        t = datetime.now()
        for i in rec:
            b = i.time_check_in - timedelta(hours=12)
            a = i.time_check_in - timedelta(hours=1)
            print(a, b)
            print(i.time_check_in.date(), t.date())
            if i.time_check_in.date() == t.date() and a.date() != b.date():
                if i.employee_id in self.list_id:
                    self.env["check.time"].sudo().search([('employ_id', '=', i.employee_id)]).write({
                        'check_out': i.time_check_in})

                else:
                    self.env["check.time"].sudo().create({
                        'employ_id': i.employee_id,
                        'check_in': i.time_check_in,
                        'check_out': i.time_check_in,
                        'date_key': t.date()
                        })
                self.list_id.append(i.employee_id)
                print(self.list_id)

