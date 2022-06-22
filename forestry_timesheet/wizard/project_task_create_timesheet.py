from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime


class ProjectTaskCreateTimesheet(models.TransientModel):
    _inherit = 'project.task.create.timesheet'

    order_type = fields.Selection(related='task_id.order_type', readonly=True)

    product_id = fields.Many2one('product.product', check_company=True)
    category_id = fields.Many2one('product.category', string='Product Category')
    product_qty = fields.Float(string='Product Quantity')
    product_stock_uom_category_id = fields.Many2one('uom.category', string='Stock Category', related='product_id.uom_id.category_id')
    product_stock_uom_id = fields.Many2one('uom.uom', string='Stock Unit of Measure', domain="[('category_id', '=', product_stock_uom_category_id)]")
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.company)
    location_id = fields.Many2one('res.partner', 'Source Location')
    location_dest_id = fields.Many2one('res.partner', 'Destination Location')
    carrier_id = fields.Many2one('res.partner', 'Carrier', check_company=True)
    trips = fields.Integer()

    @api.onchange('product_id')
    def onchange_product(self):
        self.category_id = self.product_id.categ_id
        self.product_stock_uom_id = self.product_id.uom_id
        self.location_id = self.task_id.location_id
        self.location_dest_id = self.task_id.location_dest_id
        # quant = self.env['stock.quant'].search([('product_id', '=', self.product_id.id)], limit=1)
        # if quant:
        #     self.location_id = quant.location_id

    def button_save_timesheet(self):
        """Relace save_timesheet method."""
        values = {
            'task_id': self.task_id.id,
            'project_id': self.task_id.project_id.id,
            'date': fields.Date.context_today(self),
            'name': self.description,
            'user_id': self.env.uid,
            'unit_amount': self.task_id._get_rounded_hours(self.time_spent * 60),
            'product_id': self.product_id.id,
            'category_id': self.category_id.id,
            'product_qty': self.product_qty,
            'product_stock_uom_id': self.product_stock_uom_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'carrier_id': self.carrier_id.id,
            'trips': self.trips,
        }
        self.task_id.user_timer_id.unlink()
        return self.env['account.analytic.line'].create(values)
        # res = super().save_timesheet()
        # res.write({
        #     'product_id': self.product_id.id,
        #     'category_id': self.category_id.id,
        #     'product_qty': self.product_qty,
        #     'product_stock_uom_id': self.product_stock_uom_id.id,
        #     'location_id': self.location_id.id,
        #     'location_dest_id': self.location_dest_id.id,
        #     'trips': self.trips,
        # })
        # return res