{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "http://www.example.com",
    "author": "mm1544",
    "description": """
        Real estate module to show available properties.
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/property_view.xml",
        "views/property_type_view.xml",
        "views/property_tag_view.xml",
        "views/property_offer_view.xml",
        "views/menu_items.xml",

        # Data Files
        # 'data/property_type.xml'
        'data/estate.property.type.csv'
    ],
    "demo": [
        "demo/property_tag.xml"
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
