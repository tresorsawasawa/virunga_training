from odoo import models, fields


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    _sql_constraints = [("unique_name", "UNIQUE(name)", "Type name has to be unique")]
    _order = "name"
    _order = "sequence"

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name", required=True)
