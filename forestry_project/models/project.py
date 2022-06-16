from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime, time
import pytz


class Project(models.Model):
    _inherit = 'project.project'

    order_type = fields.Selection(selection=[
        ("pile", "Pile Order"),
        ("collection", "Collection Order"),
        ("chopping", "Chopping Order")],
        default='pile',
        required=True
    )
    work_type = fields.Selection(selection=[
        ("crane", "Crane Work"),
        ("transport", "Transport")],
        default='transport',
        required=True
    )

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """Set order type value as task label."""
        order_type_values = dict(self._fields['order_type']._description_selection(self.env))
        self.label_tasks = order_type_values.get(self.order_type)

    @api.model
    def create(self, vals):
        """Create default task on project creation."""
        project = super(Project, self).create(vals)

        # Get today with zeroed time
        date_begin = datetime.combine(fields.Date.context_today(self), time(0, 0, 0))
        # Get user timezone
        user_tz = pytz.timezone(self.env.context.get('tz') or 'UTC')
        # Localize start date
        date_begin = pytz.utc.localize(date_begin).astimezone(user_tz)
        # Set hour and reset timezone info
        date_begin = date_begin.replace(hour=8).astimezone(pytz.utc).replace(tzinfo=None)

        task = self.env['project.task'].create({
            'name': project.name,
            'project_id': project.id,
            'planned_date_begin': date_begin,
            'planned_date_end': date_begin + timedelta(hours=4),
        })
        project._onchange_order_type()
        return project