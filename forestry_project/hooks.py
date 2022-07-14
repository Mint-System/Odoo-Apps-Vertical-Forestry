# Copyright 2016 Tecnativa <vicent.cubells@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID, api


def pre_init_hook(cr):
    """
    With this pre-init-hook we want to avoid error when creating the UNIQUE
    code constraint when the module is installed and before the post-init-hook
    is launched.
    """
    cr.execute("ALTER TABLE project_task ADD COLUMN code character varying;")
    cr.execute("UPDATE project_task SET code = id;")


def post_init_hook(cr, registry):
    """
    This post-init-hook will update all existing task assigning them the
    corresponding sequence code.
    """
    env = api.Environment(cr, SUPERUSER_ID, dict())
    sequence_obj = env["ir.sequence"]

    projects = env["project.project"].search([], order="id")
    for project_id in projects.ids:
        cr.execute(
            "UPDATE project_project SET code = %s WHERE id = %s;",
            (sequence_obj.next_by_code("project.project"), project_id,),
        )

    tasks = env["project.task"].search([], order="id")
    for task_id in tasks.ids:
        cr.execute(
            "UPDATE project_task SET code = %s WHERE id = %s;",
            (sequence_obj.next_by_code("project.project"), task_id,),
        )
