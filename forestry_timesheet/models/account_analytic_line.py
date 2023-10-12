import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    order_type = fields.Selection(related="project_id.order_type", readonly=True)

    product_id = fields.Many2one(
        "product.product", "Source Product", check_company=True
    )
    category_id = fields.Many2one("product.category", "Source Product Category")
    product_qty = fields.Float(string="Source Product Quantity")
    product_stock_uom_category_id = fields.Many2one(
        "uom.category", "Source Stock Category", related="product_id.uom_id.category_id"
    )
    product_stock_uom_id = fields.Many2one(
        "uom.uom",
        "Source Stock Unit of Measure",
        domain="[('category_id', '=', product_stock_uom_category_id)]",
    )
    location_id = fields.Many2one("res.partner", "Source Location")

    product_dest_id = fields.Many2one(
        "product.product", "Target Produt", check_company=True
    )
    category_dest_id = fields.Many2one("product.category", "Target Product Category")
    product_dest_qty = fields.Float(string="Target Product Quantity")
    product_dest_stock_uom_category_id = fields.Many2one(
        "uom.category", "Target Stock Category", related="product_id.uom_id.category_id"
    )
    product_dest_stock_uom_id = fields.Many2one(
        "uom.uom",
        "Target Stock Unit of Measure",
        domain="[('category_id', '=', product_stock_uom_category_id)]",
    )
    location_dest_id = fields.Many2one("res.partner", "Destination Location")

    carrier_id = fields.Many2one("res.partner", "Carrier", check_company=True)
    trips = fields.Integer()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """Set defaults when source product is selected."""
        self.category_id = self.product_id.categ_id
        self.product_stock_uom_id = self.product_id.uom_id
        self.location_id = self.task_id.location_id
        self.location_dest_id = self.task_id.location_dest_id

    @api.onchange("product_dest_id")
    def _onchange_product_dest_id(self):
        """Set defaults when target product is selected."""
        self.category_dest_id = self.product_dest_id.categ_id
        self.product_dest_stock_uom_id = self.product_dest_id.uom_id

    @api.onchange("product_qty", "product_stock_uom_id", "product_dest_stock_uom_id")
    def _onchange_product_qty(self):
        if self.product_dest_id:
            self.product_dest_qty = self.product_stock_uom_id._compute_quantity(
                self.product_qty, self.product_dest_stock_uom_id
            )
