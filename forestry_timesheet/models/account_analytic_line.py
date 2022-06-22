from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    order_type = fields.Selection(related='project_id.order_type', readonly=True)
    product_id = fields.Many2one('product.product', check_company=True)
    category_id = fields.Many2one('product.category', string='Product Category')
    product_qty = fields.Float(string='Product Quantity')
    product_stock_uom_category_id = fields.Many2one('uom.category', string='Stock Category', related='product_id.uom_id.category_id')
    product_stock_uom_id = fields.Many2one('uom.uom', string='Stock Unit of Measure', domain="[('category_id', '=', product_stock_uom_category_id)]")
    location_id = fields.Many2one('res.partner', 'Source Location')
    location_dest_id = fields.Many2one('res.partner', 'Destination Location')
    carrier_id = fields.Many2one('res.partner', 'Carrier', check_company=True)
    trips = fields.Integer()

    # stock_location_id = fields.Many2one('stock.location', 'Source Location', check_company=True)
    # stock_location_dest_id = fields.Many2one('stock.location', 'Destination Location', check_company=True)

    @api.onchange('product_id')
    def onchange_product(self):
        """Set defaults product is selected."""
        self.category_id = self.product_id.categ_id
        self.product_stock_uom_id = self.product_id.uom_id
        self.location_id = self.task_id.location_id
        self.location_dest_id = self.task_id.location_dest_id

        # quant = self.env['stock.quant'].search([('product_id', '=', self.product_id.id)], limit=1)
        # if quant:
        #     self.location_id = quant.location_id
        # self.location_dest_id = self.task_id.partner_id.property_stock_customer

    # @api.model_create_multi
    # def create(self, vals_list):
    #     lines = super(AccountAnalyticLine, self).create(vals_list)
    #     _logger.warning([lines,vals_list])
    #     return lines
