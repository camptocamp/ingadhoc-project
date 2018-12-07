# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################

from openerp.osv import fields, osv


class project_task_type(osv.osv):
    _name = 'project.task.phase'
    _description = 'Task Phase'
    _order = 'date_max, id'

    def get_min_max_date(self, cr, uid, ids, field_name, arg, context=None):
        """ Finds minimum and maximum dates.
        @return: Dictionary of values
        """
        res = {}
        for i in self.browse(cr, uid, ids):
            min_date = False
            max_date = False
            for t in i.task_ids:
                if (t.date_start and t.date_start < min_date) or not min_date:
                    min_date = t.date_start
                if (t.date_end and t.date_end > max_date) or not max_date:
                    max_date = t.date_end
            res[i.id] = {'date_min': min_date or False,
                         'date_max': max_date or False}
        if not ids:
            return res
        return res

    _columns = {
        'name': fields.char('Phase Name', required=True, size=64,
                            translate=True),
        'sequence': fields.integer('Sequence'),
        'project_id': fields.many2one('project.project', 'Project'),
        'task_ids': fields.one2many('project.task', 'phase_id', 'Tasks'),
        'date_min': fields.function(get_min_max_date, multi="min_max_date",
                                    type='datetime', string='Min. date',
                                    store=True),
        'date_max': fields.function(get_min_max_date, multi="min_max_date",
                                    type='datetime', string='Max. date'),
    }


class project_task(osv.osv):
    _inherit = 'project.task'

    _columns = {
        'phase_id': fields.many2one('project.task.phase', 'Phase', ),
        'master_id': fields.many2one('master.project', 'Master Project'),
    }

    def _read_group_phase_ids(self, cr, uid, ids, domain,
                              read_group_order=None, access_rights_uid=None,
                              context=None):
        if context is None:
            context = {}
        phase_obj = self.pool.get('project.task.phase')
        order = 'date_min'
        access_rights_uid = access_rights_uid or uid
        if 'default_project_id' in context:
            search_domain = [
                '|',
                ('project_id', '=', context['default_project_id']),
                ('id', 'in', ids),
            ]
        else:
            search_domain = [('id', 'in', ids)]
        phase_ids = phase_obj._search(cr, uid, search_domain, order=order,
                                      access_rights_uid=access_rights_uid,
                                      context=context)
        result = phase_obj.name_get(cr, access_rights_uid, phase_ids,
                                    context=context)
        # restore order of the search
        result.sort(
            lambda x, y: cmp(phase_ids.index(x[0]), phase_ids.index(y[0])))
        return result, None

    _group_by_full = {
        'phase_id': _read_group_phase_ids,
    }
