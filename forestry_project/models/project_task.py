from odoo import _, api, fields, models
import logging
_logger = logging.getLogger(__name__)
from datetime import timedelta, datetime, time
import pytz


class ProjectTask(models.Model):
    _inherit = 'project.task'

    order_type = fields.Selection(selection=[
        ('default', 'Default'),
        ('pile', 'Pile Order'),
        ('collection', 'Collection Order'),
        ('chopping', 'Chopping Order')],
        default='default',
        required=True
    )
    work_type = fields.Selection(selection=[
        ('crane', 'Crane Work'),
        ('transport', 'Transport')],
        default='transport',
        required=True
    )
    code = fields.Char(
        string='Task Code',
        required=True,
        default='/',
        copy=False,
    )
    product_id = fields.Many2one('product.product', check_company=True)
    location_id = fields.Many2one('res.partner', 'Source Location', check_company=True)
    location_link = fields.Char('Source Location Link', related='location_id.location_link', readonly=False)
    location_dest_id = fields.Many2one('res.partner', 'Destination Location', check_company=True)
    location_dest_link = fields.Char('Destination Location Link', related='location_dest_id.location_link', readonly=False)
    vehicle_id = fields.Many2one('fleet.vehicle', check_company=True, tracking=True)
    trailer = fields.Boolean()

    _sql_constraints = [
        ('project_task_unique_code', 'UNIQUE (code)', _('The code must be unique!')),
    ]

    def name_get(self):
        """Set task display name."""
        res = []
        for record in self:
            res.append((record.id, '[%s] %s' % (record.code, record.name)))
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for task in self:
            if not task.location_id :
                task.location_id = task.product_id.location_partner_id

    @api.model_create_multi
    def create(self, vals_list):
        """
        Set default values.
        Generate task code.
        Set default planned date
        """
        for vals in vals_list:
            project_id = vals.get('project_id') or self.env.context.get('default_project_id')
            project_id = self.env['project.project'].browse(project_id)
            if project_id and 'order_type' not in vals:
                vals['order_type'] = project_id.order_type
            if vals.get('code', '/') == '/':
                vals['code'] = self.env['ir.sequence'].next_by_code('project.project')
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
