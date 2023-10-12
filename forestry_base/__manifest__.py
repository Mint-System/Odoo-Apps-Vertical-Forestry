{
    "name": "Forestry Base",
    "summary": """
        Base module of the forestry vertical integration apps.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Forestry",
    "version": "15.0.4.0.0",
    "license": "OPL-1",
    "depends": ["contacts", "product"],
    "data": [
        "views/product_template.xml",
        "views/res_partner.xml",
        "views/product_product.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
