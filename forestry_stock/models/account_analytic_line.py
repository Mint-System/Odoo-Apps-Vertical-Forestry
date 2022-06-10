from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def action_validate_timesheet(self):
        """Set product qty if timesheet entry is validated."""

        res = super().action_validate_timesheet()
        # Check if has storable product and is linked to a task
        for line in self.filtered(lambda l: l.task_id and l.prdouct_id and l.product_id.type == 'product'):
            # Get quant of product
            quant = self.env['stock.quant'].search([
                ('product_id', '=', line.product_id.id),
                ('quantity', '>', 0)
            ],limit=1)
            _logger.warning(quant)

            # Convert uom
            line_quantity = line.product_id.uom_id._compute_quantity(line.quantity, line.product_stock_uom_id, rounding_method='HALF-UP')
            _logger.warning(quant)
            
            # Set quant
            quants.inventory_quantity = quant.quantity - line_quantity
            quant.inventory_quantity_set = True

        return res