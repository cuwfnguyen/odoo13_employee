import json

from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta


class CheckTime(models.Model):
    _name = 'check.time'
    _description = ' ID Check time'
    employ_id = fields.Many2one('hr.employee', store=True, readonly=False, string='Name')
    check_in = fields.Datetime(string='Check in', readonly=True)
    check_out = fields.Datetime(string='Check out', readonly=True)
    timekeeping = fields.Float(string='Timekeeping', compute='_compute_expense')
    date_key = fields.Date('Date', readonly=True)

    def _compute_expense(self):
        res = self.env['check.time'].search([])
        for i in res:
            if i.check_out and i.check_in:
                tp = i.check_out - i.check_in
                tp1 = tp / timedelta(minutes=60)
                if tp1 == 0:
                    i.timekeeping = 0
                if tp1 > 0.02:
                    i.timekeeping = 1
                if tp1 <= 0.02:
                    i.timekeeping = 0.5

    def send_mail(self):
        t = datetime.now()
        #kiem tra nhung id chua check in
        list_id_employee = []
        employee = self.env['hr.employee'].search([('name', '!=', False)])
        for x in employee:
            list_id_employee.append(x.id)
        list_id_check_time = []
        check_time = self.env['check.time'].search([])
        for y in check_time:
            if y.check_in.date() == t.date():
                list_id_check_time.append(int(y.employ_id))
        list_set = set(list_id_employee).difference(list_id_check_time)
        list_send_email = list(list_set)

        template_id = self.env.ref('depends_hr.mail_notification_check_timekeeping').id
        template = self.env['mail.template'].browse(template_id)

        #gui mail cho cac id chua check in
        for res in list_send_email:
            template.send_mail(res, force_send=True)
            print('chua cham cong ngay hom nay: ')
            print('send mail')

        #gui mail cho cac id thieu check in/check out
        check = self.env['check.time'].search([])
        for i in check:
            if i.check_in.date() == t.date() and i.check_in == i.check_out:
                template.send_mail(i.employ_id.id, force_send=True)
                print('chua cham cong ngay hom nay: ', i.date_key)
                print('send mail')

    def send_mail_monthly(self):

        xlsx_report = self.env['report.trans'].create_xlsx_monthly()
        attachment = xlsx_report.get('attachment_id')
        attachment_id = self.env['ir.attachment'].browse(attachment)
        template_id = self.env.ref('depends_hr.timekeeping_monthly').id
        template = self.env['mail.template'].browse(template_id)
        template.attachment_ids = [(6, 0, [attachment_id.id])]

        id_admin = self.env['hr.employee'].search([('name', '=', 'President')]).id

        template.send_mail(id_admin, raise_exception=False, force_send=True)
        template.attachment_ids = [(3, [attachment_id.id])]

    def test_value(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        print(user.id, user.name)

        a = self.env["repair.repair"].search([('id_repair.name', '=', 'managerS1')], limit=1)
        print(a.id_repair.user_id.id)














