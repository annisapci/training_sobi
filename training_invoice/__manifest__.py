# -*- coding: utf-8 -*-
{
    'name' : 'Training Invoice',
    'description': """
        Created by SAR & AM
    """,
    'author' : 'SAR',
    'category': 'Accounting',      
    'depends' : ['account'],
    'data': [
        'views/account_report_views.xml',
        'views/report_invoice_views.xml',
        'views/account_invoice_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}