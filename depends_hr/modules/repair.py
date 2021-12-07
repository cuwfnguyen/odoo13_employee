from datetime import datetime
from datetime import timedelta
from odoo import models, fields, api


class Repair(models.Model):
    _name = 'repair.repair'
    _description = 'Repair'

    repair = fields.Many2one('hr.employee.public', 'Employee', default=lambda self: self.env.user.employee_id, readonly=True)
    # approve1 = fields.Many2one('hr.employee', compute='check_repair')
    # approve2 = fields.Many2one('hr.employee', compute='check_repair')
    date_repair = fields.Datetime(string='Date repair')
    description = fields.Text(string='Note')

    status = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm1', 'Approval'),
        ('confirm2', 'Second Approval'),
      ], string='Status', readonly=True, tracking=True, copy=False, default='draft',)

    current_usr = fields.Selection([
        ('self', 'Self'),
        ('none', 'None'),
        ('approve1', 'Approve1'),
        ('approve2', 'Approve2'),
    ], string='Approve', readonly=True, tracking=True, copy=False, default='none', compute='get_current_user')

    # def check_repair(self):
    #     self.approve1 = self.id_repair.parent_id
    #     self.approve2 = self.id_repair.parent_id.parent_id

    def cancel_repair(self):
        self.status = "cancel"
        print('cancel repair')

    def approval_repair(self):
        if self.status == "confirm1":
            self.status = "confirm2"

            date_repair_correct = self.date_repair + timedelta(hours=7)
            repair = self.env['check.time'].search([('employ_id.id', '=', self.repair.id)])
            for res in repair:
                if res.check_in.date() == date_repair_correct.date():
                    print(res.employ_id.name)
                    res.write({
                        'check_in': res.check_in,
                        'check_out': res.check_in + timedelta(hours=8)
                    })

        if self.status == 'draft':
            self.status = 'confirm1'
            print('comfirm1')

    def get_current_user(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        users = user.id

        if self.repair.user_id.id == users:
            self.current_usr = 'self'
        elif self.repair.parent_id.user_id.id == users:
            self.current_usr = 'approve1'
        elif self.repair.parent_id.parent_id.user_id.id == users:
            self.current_usr = 'approve2'
        else:
            self.current_usr = 'none'












