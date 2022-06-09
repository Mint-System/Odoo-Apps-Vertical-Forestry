from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    order_type = fields.Selection(related='project_id.order_type',readonly=True)

    product_id = fields.Many2one('product.product', check_company=True)
    location_id = fields.Many2one('res.partner', 'Source Location', check_company=True)
    location_dest_id = fields.Many2one('res.partner', 'Destination Location', check_company=True)
    distance = fields.Integer()
    location_link = fields.Char('Destination Location Details')
    vehicle_id = fields.Many2one('fleet.vehicle', check_company=True)
    trailer = fields.Boolean()