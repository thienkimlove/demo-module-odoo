import logging


from odoo import api, fields, _, models
from odoo.exceptions import UserError
_logger = logging.getLogger(__name__)


class ProjectTaskType(models.Model):
        _inherit = 'project.task.type'
        is_lock_for_user_drag = fields.Boolean('Is Lock For User Drag?')


class Task(models.Model):
        _inherit = "project.task"

        def write(self, vals):
            _logger.info('QuanDM debug : %s.', vals.get('stage_id'))
            _logger.info('QuanDM debug sef : %s.', self.stage_id)

            if 'stage_id' in vals:
                stage_id_move_to = vals.get('stage_id')
                stage_id_current = self.stage_id
                _logger.info('QuanDM is lock : %s.', stage_id_current.is_lock_for_user_drag)
                _logger.info('QuanDM stage_id_move_to : %s.', stage_id_move_to)
                _logger.info('QuanDM stage_id_current : %s.', stage_id_current.id)
                _logger.info('QuanDM current user : %s.', self.env.user)

                if stage_id_move_to != stage_id_current.id \
                        and stage_id_current.is_lock_for_user_drag \
                        and not self.env.user.has_group('project.group_project_manager'):
                    raise UserError(_("You don't have the right to do this. Please contact an Administrator."))

            return super(Task, self).write(vals)
