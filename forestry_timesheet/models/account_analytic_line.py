from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    product_id = fields.Many2one('product.product', check_company=True)
    location_id = fields.Many2one('stock.location', 'Source Location', check_company=True)
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', check_company=True)