import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = "project.task.create.timesheet"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    order_type = fields.Selection(related="task_id.order_type", readonly=True)

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
        self.product_dest_qty = self.product_stock_uom_id._compute_quantity(
            self.product_qty, self.product_dest_stock_uom_id
        )

    def button_save_timesheet(self):
        """Relace save_timesheet method."""
        values = {
            "task_id": self.task_id.id,
            "project_id": self.task_id.project_id.id,
            "date": fields.Date.context_today(self),
            "name": self.description,
            "user_id": self.env.uid,
            "unit_amount": self.task_id._get_rounded_hours(self.time_spent * 60),
            "product_id": self.product_id.id,
            "category_id": self.category_id.id,
            "product_qty": self.product_qty,
            "product_stock_uom_id": self.product_stock_uom_id.id,
            "location_id": self.location_id.id,
            "product_dest_id": self.product_dest_id.id,
            "category_dest_id": self.category_dest_id.id,
            "product_dest_qty": self.product_dest_qty,
            "product_dest_stock_uom_id": self.product_dest_stock_uom_id.id,
            "location_dest_id": self.location_dest_id.id,
            "carrier_id": self.carrier_id.id,
            "trips": self.trips,
        }
        self.task_id.user_timer_id.unlink()
        return self.env["account.analytic.line"].create(values)
