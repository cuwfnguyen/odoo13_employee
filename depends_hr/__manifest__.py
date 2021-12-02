# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)
{
    'name': 'Employee custom',
    'version': "1.0",
    'category': 'Human Resources/Staff',
    'author': 'Cuwfnguyen',
    'website': "odoo.com",
    'description': "",

    "depends": [
        'hr',
        'base_setup',
        'mail',
        'resource',
        'report_xlsx'
    ],

    'sequence': -102,
    "external_dependencies": {"python": ["requests"]},
    "data": [
        'security/security.xml',
        'security/rule_repair.xml',
        'security/ir.model.access.csv',
        'data/cron.xml',
        'wizard/report.xml',
        'views/check_in.xml',
        'data/job_checkin.xml',
        'data/send_mail.xml',
        'data/mail_template.xml',
        #'data/timekeeping_job.xml',
        'wizard/report_xlsx.xml',
        'data/mail_template2.xml',


        ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
