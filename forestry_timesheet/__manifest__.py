{
    "name": "Forestry Timesheet",
    "summary": """
        Extend timesheet app for forestry.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["forestry_base"],
    "data": ["views/view_task_form2_inherited.xml", "views/hr_timesheet_line_tree.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
