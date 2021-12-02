from odoo import models, fields, api


class Category(models.Model):
    _name = 'check.time.category'
    _description = 'category time'

    name = fields.Char(string="Tag Name", required=True)
