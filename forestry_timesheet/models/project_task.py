import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = "project.task"

    qty_total = fields.Float("Total Quantity", compute="_compute_qty_total")

    @api.depends("timesheet_ids")
    def _compute_qty_total(self):
        for task in self:
            task.qty_total = sum(task.timesheet_ids.mapped("product_qty"))

    def _action_open_new_timesheet(self, time_spent):
        res = super()._action_open_new_timesheet(time_spent)
        if self.product_id:
            res["context"]["default_product_id"] = self.product_id.id
        if self.product_dest_id:
            res["context"]["default_product_dest_id"] = self.product_dest_id.id
        return res
