from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _action_apply_inventory(self, operation='remove'):
        # Check if has storable product and is linked to a task
        for line in self.filtered(lambda l: l.task_id and l.product_id and l.product_id.type == 'product'):
            # Get quant of product
            quant = self.env['stock.quant'].search([
                ('product_id', '=', line.product_id.id),
            ],limit=1)

            # Convert uom
            line_quantity = line.product_stock_uom_id._compute_quantity(line.product_qty, line.product_id.uom_id, rounding_method='HALF-UP')

            # Set quant
            if operation == 'remove' and not line.validated:
                if (quant.quantity - line_quantity) < 0.0:
                    raise UserError(_("Cannot apply inventory change for %s as result would be negative.") % line.product_id.display_name)
                quant.inventory_quantity = quant.quantity - line_quantity
                quant.action_apply_inventory()
            if operation == 'add' and line.validated:
                # Raise error if quant is not positive
                if quant.quantity < 0.0:
                    raise UserError(_("No empty or positive inventory has been found for product %s.") % line.product_id.display_name)
                quant.inventory_quantity = quant.quantity + line_quantity
                quant.action_apply_inventory()

    def action_validate_timesheet(self):
        """Set product qty if timesheet entry is validated."""
        self._action_apply_inventory()
        return super().action_validate_timesheet()

    def action_reset_validation_timesheet(self):
        """Undo inventory change if move is validated."""
        self._action_apply_inventory(operation='add')
        self.write({'validated': False})