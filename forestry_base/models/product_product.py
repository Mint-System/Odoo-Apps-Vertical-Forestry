import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        res = []
        for rec in self:
            if rec.default_code == rec.name:
                res.append((rec.id, rec.default_code))
            else:
                res.append(
                    (
                        rec.id,
                        "%s%s"
                        % (
                            rec.default_code and "[%s] " % rec.default_code or "",
                            rec.name,
                        ),
                    )
                )
        return res
