from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime, time
import pytz


class ProjectTask(models.Model):
    _inherit = "project.task"

    order_type = fields.Selection(related='project_id.order_type', readonly=True)
    product_id = fields.Many2one('product.product', check_company=True)
    location_id = fields.Many2one('res.partner', 'Source Location', check_company=True)
    location_link = fields.Char('Source Location Link')
    location_dest_id = fields.Many2one('res.partner', 'Destination Location', check_company=True)
    location_dest_link = fields.Char('Destination Location Link')
    vehicle_id = fields.Many2one('fleet.vehicle', check_company=True, tracking=True)
    trailer = fields.Boolean()

    @api.onchange('location_id')
    def _onchange_location_id(self):
        for project in self:
            if not project.location_link :
                project.location_link = project.location_id.location_link

    @api.onchange('location_dest_id')
    def _onchange_location_dest_id(self):
        for project in self:
            if not project.location_dest_link :
                project.location_dest_link = project.location_dest_id.location_link

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)

        # Get today with zeroed time
        date_begin = datetime.combine(fields.Date.context_today(self), time(0, 0, 0))
        # Get user timezone
        user_tz = pytz.timezone(self.env.context.get('tz') or 'UTC')
        # Localize start date
        date_begin = pytz.utc.localize(date_begin).astimezone(user_tz)
        # Set hour and reset timezone info
        date_begin = date_begin.replace(hour=8).astimezone(pytz.utc).replace(tzinfo=None)

        for task in tasks.filtered('order_type'):
            task.write({
                'planned_date_begin': date_begin,
                'planned_date_end': date_begin + timedelta(hours=4),
            })
        return tasks
