from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _action_open_new_timesheet(self, time_spent):
        res = super()._action_open_new_timesheet(time_spent)
        if self.product_id:
            res['context']['default_product_id'] = self.product_id.id
        if self.product_dest_id:
            res['context']['default_product_dest_id'] = self.product_dest_id.id
        return res