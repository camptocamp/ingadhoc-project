Project Task Phase
==================

Upstream repository: https://github.com/ingadhoc-project
Camptocamp fork: https://github.com/camptocamp/ingadhoc-project

Notes
-----

This module has been modified by the previous integrator, that's why we have
put it in the specific branch `9.0-custom`.

The main differences are:

* On `project.task.phase` model, the local one has the following fields:
** `project_id` (M2O)
** `task_ids` (O2M)
** `date_min` and `date_max` (computed fields)
* On `project.task`, the local module has added these fields:
** `phase_id` (M2O)
** `master_id` (M2O related to `master.project` , a data model added by the `sale_update` module)
* due to the above M2O dependency, the local module has a new dependency against `sale_update`.
* the local module was developed with the old API

Make a diff between the branches `9.0` and `9.0-custom` to know precisely
the differences.
