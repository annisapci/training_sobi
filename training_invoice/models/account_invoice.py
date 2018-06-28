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

    discount_global = fields.Float(string="Discount Global")
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type', 'discount_global')
    def _compute_amount(self):
        round_curr = self.currency_id.round
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(round_curr(line.amount_total) for line in self.tax_line_ids)
        if self.discount_global > 0 :
            self.amount_total = (self.amount_untaxed + self.amount_tax) - self.discount_global
        else:
            self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

