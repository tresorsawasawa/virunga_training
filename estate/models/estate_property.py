from odoo import models, fields
from datetime import timedelta, date

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: (date.today() + timedelta(days=90)),
        copy=False
        )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Number of Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades", default=1)
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [('N', 'North'),
         ('S', 'South'),
         ('E', 'East'),
         ('W', 'West')],
        string="Garden Orientation")
    state = fields.Selection(
        [('new', 'New'),
         ('offer_received', 'Offer Received'),
         ('offer_accepted', 'Offer Accepted'),
         ('sold', 'Sold'),
         ('canceled', 'Canceled')],
        string="Status",
        default='new',
        copy=False,
        required=True
        )

