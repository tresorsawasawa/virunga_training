import random
from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Tag name has to be unique')]
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()

# Feature to pick random color
    @api.model
    def create(self, vals):
        if 'color' not in vals:
            vals['color'] = random.randint(1, 11)
        return super(EstatePropertyTag, self).create(vals)
