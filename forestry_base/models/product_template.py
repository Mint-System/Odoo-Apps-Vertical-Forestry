from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    supplier_id = fields.Many2one('res.partner', check_company=True)
    supplier_code = fields.Char('Supplier Reference')
    location_partner_id = fields.Many2one('res.partner', check_company=True)
    location_link = fields.Char()

    @api.onchange('location_partner_id')
    def _onchange_location_partner_id(self):
        for product in self:
            if not product.location_link :
                product.location_link = product.location_partner_id.location_link
