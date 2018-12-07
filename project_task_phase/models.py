# -*- coding: utf-8 -*-

from openerp import models, fields


class ProjectForecast(models.Model):
    _inherit = 'project.forecast'

    phase_id = fields.Many2one("project.task.phase",
                               related='task_id.phase_id', string='Phase',
                               readonly=True, store=True)
