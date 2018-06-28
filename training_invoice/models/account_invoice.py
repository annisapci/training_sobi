# coding: utf-8

from openerp import api, fields, models, _
from odoo.addons import decimal_precision as dp

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    contact_id = fields.Many2one('res.partner', string='Contact')

    @api.multi
    @api.onchange('partner_id')
    def partner_id_change(self):

        res= {}
        contact_list= []

        for abc in self:
            record = abc.partner_id.child_ids.filtered(lambda x: x.type == 'contact')
            contact_list.append(record.ids)

            res= {'domain':{'contact_id':[('id','in',contact_list[0])]}} 
        return res

