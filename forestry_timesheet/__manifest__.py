{
    "name": "Forestry Timesheet",
    "summary": """
        Extend timesheet app for forestry.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.2.0.1",
    "license": "OEEL-1",
    "depends": ["forestry_project", "stock", "timesheet_grid"],
    "data": ["views/project_task.xml", "views/hr_timesheet.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
