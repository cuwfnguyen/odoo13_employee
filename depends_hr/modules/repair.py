from datetime import datetime
from datetime import timedelta
from odoo import models, fields, api


class Repair(models.Model):
    _name = 'repair.repair'
    _description = 'Repair'

    id_repair = fields.Many2one('hr.employee', string='Employee')
    approve1 = fields.Many2one('hr.employee', compute='check_repair')
    approve2 = fields.Many2one('hr.employee', compute='check_repair')
    date_repair = fields.Datetime(string='Date repair')
    description = fields.Text(string='Note')
    #current_user = fields.Many2one('hr.employee',)

    current_usr = fields.Boolean(string='User access create repair', default=False, compute='get_current_user')
    status = fields.Selection([
        ('draft', 'To Submit'),
        ('cancel', 'Cancelled'),
        ('confirm1', 'Approval'),
        ('confirm2', 'Second Approval'),
      ], string='Status', readonly=True, tracking=True, copy=False, default='draft',)
    button_clicked = fields.Boolean(
        string='Approved',
        default=False,
        readonly=True,
    )

    def check_repair(self):
        self.approve1 = self.id_repair.parent_id
        self.approve2 = self.id_repair.parent_id.parent_id

    def cancel_repair(self):
        self.status = "cancel"
        print('cancel repair')

    def approval_repair(self):
        if self.status == "confirm1":
            self.status = "confirm2"
            for record in self:
                record.write({
                    'button_clicked': True,
                })

            date_repair_correct = self.date_repair + timedelta(hours=7)
            repair = self.env['check.time'].search([('employ_id.id', '=', self.id_repair.id)])
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
            for record in self:
                record.write({
                    'button_clicked': True,
                })

    def get_current_user(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        user_id = user.id

        if self.id_repair.user_id.id == user_id:
            self.current_usr = True
        else:
            self.current_usr = False











