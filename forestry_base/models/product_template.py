from odoo import fields, models, api
from . import product


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char(compute='_compute_name', store=True)
    supplier_id = fields.Many2one('res.partner', check_company=True)
    supplier_code = fields.Char('Supplier Reference')
    location_partner_id = fields.Many2one('res.partner', check_company=True)
    location_link = fields.Char(related='location_partner_id.location_link', readonly=False)

    @api.onchange('location_partner_id')
    def _onchange_location_partner_id(self):
        for product in self:
            if not product.location_link :
                product.location_link = product.location_partner_id.location_link

    def name_get(self):
        res = []
        for rec in self:            
            if rec.location_partner_id:
                res.append((rec.id, product.get_name(rec)))
            else:
                res.append((rec.id, '%s%s' % (rec.default_code and '[%s] ' % rec.default_code or '', rec.name)))
        return res

    @api.depends('default_code', 'location_partner_id', 'supplier_id')
    def _compute_name(self):
        for rec in self.filtered(lambda p: p.location_partner_id):
            rec.name = product.get_name(rec)