{
    "name": "Forestry Timesheet",
    "summary": """
        Extend timesheet app for forestry.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.3.2.0",
    "license": "OEEL-1",
    "depends": ["forestry_project", "stock", "timesheet_grid"],
    "data": [
        "views/project_task.xml",
        "views/project_task_create_timesheet.xml",
        "views/hr_timesheet.xml",
        "report/report_deliveryslip.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
