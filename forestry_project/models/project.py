from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta

class Project(models.Model):
    _inherit = 'project.project'

    order_type = fields.Selection(selection=[
        ("pile", "Pile Order"),
        ("collection", "Collection Order"),
        ("chopping", "Chopping Order")],
        default='pile',
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
        task = self.env['project.task'].create({
            'name': project.name,
            'project_id': project.id,
            'planned_date_begin': datetime.now(),
            'planned_date_end': datetime.now() + timedelta(minutes=30),
        })
        return project