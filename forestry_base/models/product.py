def get_name(rec):
    return '%(default_code)s - %(supplier_name)s - %(location_name)s' % {
        'default_code': rec.default_code or '000',
        'supplier_name': rec.supplier_id.name,
        'location_name': rec.location_partner_id.name,
    }