from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'
    _sql_constrains = [('unique_name', 'UNIQUE(name)', 'Tag name has to be unique')]

    name = fields.Char(string='Name', required=True)
