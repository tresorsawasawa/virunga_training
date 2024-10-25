from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Real Estate Property Type"
    _sql_constraints = [("unique_name", "UNIQUE(name)", "Type name has to be unique")]
    _order = "name"
    _order = "sequence"

    sequence = fields.Integer(default=1)
    name = fields.Char(string="Name", required=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string="Property Count", compute="_compute_offer_count")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    
    def action_open_property_ids(self):
        return  {
            "name" : "Offers",
            "type" : "ir.actions.act_window",
            "view_mode" : "tree,form",
            "res_model" : "estate.property.offer",
            "target" : "current",
            "domain" : [("property_type_id", "=", self.id)],
            "context" : {
                "default_property_type_id" : self.id
            }
        }
