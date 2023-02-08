from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)
from . import product

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        res = []
        for rec in self:            
            if rec.location_partner_id:
                res.append((rec.id, product.get_name(rec)))
            else:
                res.append((rec.id, '%s%s' % (rec.default_code and '[%s] ' % rec.default_code or '', rec.name)))
        return res
