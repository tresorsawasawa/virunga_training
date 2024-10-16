from odoo import models, fields

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=1)
    living_area = fields.Float(string="Living Area (sqm)")