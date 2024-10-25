from odoo import models, fields, api
from datetime import timedelta, datetime
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True, string="Property Type"
    )
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            elif offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept(self):  
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped('status'):
            raise UserError("This property has already an offer")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
    
    def action_refuse(self):
        self.ensure_one()
        if self.property_id.selling_price == self.price :
            self.property_id.selling_price = 0.00
        self.status = "refused"

    @api.constrains("price")
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("The price must be strictly positive")
    
    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        property = self.env["estate.property"].browse(property_id)

        property.state = "offer_received"

        existing_offers = self.search([("property_id", "=", property_id)])
        for offer in existing_offers:
            if vals.get("price") < offer.price:
                raise UserError("Cannot create an offer lower than an existing offer.")
            
        return super(EstatePropertyOffer, self).create(vals)
