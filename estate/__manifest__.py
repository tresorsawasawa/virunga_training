{
    "name": "Real Estate",
    "summary": "Test module",
    "version": "17.0.0.0",
    "license": "OEEL-1",
    "author": "Tresor Sawasawa",
    "category": "Test",
    "depends": ["base"],
    "data": [
        # Security
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        # Views
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        # Menus
    ],
    "demo": ["demo/demo.xml"],
    "views": ["estate_property_views.xml"],
    "application": True,
}

