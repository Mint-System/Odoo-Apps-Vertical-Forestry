import logging

from odoo import _, models

_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    def _action_remove_inventory(self, product_id, product_stock_uom_id, product_qty):
        """Remove on hand qty."""

        self.ensure_one()

        # Check if line has storable product and is linked to a task
        if self.task_id and product_id.type == "product":

            # Get quant of product
            quant = self.env["stock.quant"].search(
                [
                    ("product_id", "=", product_id.id),
                ],
                limit=1,
            )

            # Convert uom
            line_quantity = product_stock_uom_id._compute_quantity(
                product_qty, product_id.uom_id, rounding_method="HALF-UP"
            )

            # Remove quantity
            if (quant.quantity - line_quantity) < 0.0:
                raise UserError(
                    _(
                        "Cannot apply inventory change for %s as result would be negative."
                    )
                    % product_id.display_name
                )
            quant.inventory_quantity = quant.quantity - line_quantity
            quant.action_apply_inventory()

    def _action_increase_inventory(self, product_id, product_stock_uom_id, product_qty):
        """Increase on hand qty."""

        self.ensure_one()

        # Check if line has storable product and is linked to a task
        if self.task_id and product_id.type == "product":

            # Get quant of product
            quant = self.env["stock.quant"].search(
                [
                    ("product_id", "=", product_id.id),
                ],
                limit=1,
            )

            # Convert uom
            line_quantity = product_stock_uom_id._compute_quantity(
                product_qty, product_id.uom_id, rounding_method="HALF-UP"
            )

            # Increase quantity
            if not quant:
                quant = self.env["stock.quant"].create(
                    {
                        "product_id": product_id.id,
                        "location_id": self.env.ref("stock.stock_location_stock").id,
                    }
                )

            quant.inventory_quantity = quant.quantity + line_quantity
            quant.action_apply_inventory()

    def action_validate_timesheet(self):
        """Set product qty if timesheet entry is validated."""
        for line in self:
            if line.product_id:
                line._action_remove_inventory(
                    product_id=line.product_id,
                    product_stock_uom_id=line.product_stock_uom_id,
                    product_qty=line.product_qty,
                )
            if line.product_dest_id:
                line._action_increase_inventory(
                    product_id=line.product_dest_id,
                    product_stock_uom_id=line.product_dest_stock_uom_id,
                    product_qty=line.product_dest_qty,
                )
        return super().action_validate_timesheet()

    def action_invalidate_timesheet(self):
        """Undo inventory change if move is invalidated."""
        res = super().action_invalidate_timesheet()
        for line in self:
            if line.product_id:
                line._action_increase_inventory(
                    product_id=line.product_id,
                    product_stock_uom_id=line.product_stock_uom_id,
                    product_qty=line.product_qty,
                )
            if line.product_dest_id:
                line._action_remove_inventory(
                    product_id=line.product_dest_id,
                    product_stock_uom_id=line.product_dest_stock_uom_id,
                    product_qty=line.product_dest_qty,
                )
        return res
