# -*- coding: utf-8 -*-
# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
import openerp.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    # Columns Section
    margin = fields.Float(
        'Margin', compute='_compute_multi_margin', store=True,
        multi='multi_margin',
        digits_compute=dp.get_precision('Product Price'))

    purchase_price = fields.Float(
        'Cost Price', compute='_compute_multi_margin', store=True,
        multi='multi_margin',
        digits_compute=dp.get_precision('Product Price'))

    # Compute Section
    @api.multi
    @api.depends(
        'product_id', 'quantity', 'price_subtotal', 'invoice_id.type',
        'invoice_id.currency_id')
    def _compute_multi_margin(self):
        company_currency = self.env.user.company_id.currency_id
        for line in self.filtered(
                lambda l: l.product_id and
                l.invoice_id.type in ('out_invoice', 'out_refund')):
            line.purchase_price = line.product_id.standard_price
            price_subtotal = line.invoice_id.currency_id.compute(
                line.price_subtotal, company_currency)
            line.margin = price_subtotal - (
                line.product_id.standard_price * line.quantity)
