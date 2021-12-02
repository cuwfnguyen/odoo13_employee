import odoo.odoo.modules.registry
from odoo import http
from odoo.http import request
import json
from datetime import datetime

class CheckIn(http.Controller):
    _name = 'check.in'

    @http.route(['/check_in/time/'], method=['POST'], type="json", auth='public', csrf=False)
    def handler(self, **kw):
        id = request.params['id']

        t = datetime.now()
        rec = request.env["hr.employee"].sudo().search([('id', '=', id), ('name', '!=', False)], limit=1)
        if not rec.id:
            return "Nhap sai ID"

        request.env["time.check.in"].sudo().create({
            'employee_id': id,
            'time_check_in': t
        })

        a = request.env["time.check.in"].sudo().search([])
        for i in a:
            print(i.employee_id, i.time_check_in)

        tmp = {
                'content': {
                    'name': rec.name,
                    'time_check_in': t.strftime("%m/%d/%Y, %H:%M:%S")
                }
        }
        #data = json.dumps(tmp, default=str)
        # response = request.make_response(data, [
        #     ('Content-Type', 'application/json')
        # ])
        return tmp








