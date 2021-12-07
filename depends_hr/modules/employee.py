from odoo import models, fields, api
from datetime import datetime
from datetime import timedelta


class Category(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'
    t = str((datetime.now() - timedelta(hours=24)).date())


