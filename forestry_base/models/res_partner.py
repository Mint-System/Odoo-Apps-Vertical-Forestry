from odoo import fields, models
import logging
_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = "res.partner"

    location_link = fields.Char()
    is_location = fields.Boolean("Location")