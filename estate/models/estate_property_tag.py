import random
from odoo import models, fields, api

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'Tag name has to be unique')]
    _order = "name"

    name = fields.Char(string='Name', required=True)
    color = fields.Integer()
