{
    "name": "Forestry Project",
    "summary": """
        Extend project app for forestry.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.1.2.0",
    "license": "OPL-1",
    "depends": [
        "forestry_base",
        "hr_fleet",
        "project_enterprise",
        "project_task_default_stage",
        "project_task_code",
        "project_template",
    ],
    "data": ["views/project_task.xml", "views/project.xml"],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
}
