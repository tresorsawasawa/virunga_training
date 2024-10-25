from odoo import models, fields, api
from datetime import timedelta, date
from odoo.exceptions import UserError, ValidationError


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
        copy=False,
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
        [("N", "North"), ("S", "South"), ("E", "East"), ("W", "West")],
        string="Garden Orientation",
    )
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        default="new",
        copy=False,
        required=True,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    best_price = fields.Float(
        string="Best Offer Price",
        compute="_compute_best_price",
        store=True,
        readonly=True,
    )
    total_area = fields.Float(
        string="Total Area", compute="_compute_total_area", store=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(
                    property.offer_ids.mapped("price"), default=0.0
                )
            else:
                property.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        for estate in self:
            if not estate.garden:
                estate.garden_area = 0
                estate.garden_orientation = ""

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        if self.date_availability and self.date_availability < date.today():
            return {
                "warning": {
                    "title": "Invalid Date",
                    "message": "The availability date cannot be in the past.",
                }
            }

    def action_set_sold(self):
        for property in self:
            if property.state == "canceled":
                raise UserError("A canceled property cannot be sold.")
            property.state = "sold"

    def action_set_cancel(self):
        for property in self:
            if property.state == "sold":
                raise UserError("A sold property cannot be canceled.")
            property.state = "canceled"

    # Constrains

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price <= 0:
                raise ValidationError("The selling price must be positive")

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for record in self:
            if record.expected_price <= 0:
                raise ValidationError("The expected price must be positive")

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price_and_expected_price(self):
        for record in self:
            if record.selling_price < record.expected_price:
                raise ValidationError(
                    "The selling price cannot be less than the expected price"
                )
