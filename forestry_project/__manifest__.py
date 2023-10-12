{
    "name": "Forestry Project",
    "summary": """
        Extend project app for forestry.
    """,
    "author": "Mint System GmbH, Odoo Community Association (OCA)",
    "website": "https://www.mint-system.ch",
    "category": "Administration",
    "version": "15.0.4.0.0",
    "license": "OPL-1",
    "depends": [
        "forestry_base",
        "hr_fleet",
        "project_enterprise",
        "project_task_default_stage",
    ],
    "data": [
        "data/project_sequence.xml",
        "views/project_task.xml",
        "views/project.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "images": ["images/screen.png"],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
