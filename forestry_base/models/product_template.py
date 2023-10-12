from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    name = fields.Char(compute="_compute_name", store=True, readonly=False)
    supplier_id = fields.Many2one("res.partner", check_company=True)
    supplier_code = fields.Char("Supplier Reference")
    location_partner_id = fields.Many2one("res.partner", check_company=True)
    location_link = fields.Char(
        related="location_partner_id.location_link", readonly=False
    )

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

    @api.onchange("location_partner_id")
    def _onchange_location_partner_id(self):
        for product in self:
            if not product.location_link:
                product.location_link = product.location_partner_id.location_link

    @api.depends("default_code")
    def _compute_name(self):
        for rec in self:
            rec.name = rec.default_code or _("New")
