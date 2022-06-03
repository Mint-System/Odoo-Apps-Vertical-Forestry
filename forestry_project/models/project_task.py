from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    product_id = fields.Many2one('product.product', check_company=True)
    location_id = fields.Many2one('res.partner', 'Source Location', check_company=True)
    location_dest_id = fields.Many2one('res.partner', 'Destination Location', check_company=True)
    vehicle_id = fields.Many2one('fleet.vehicle', check_company=True)