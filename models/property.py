from odoo import fields, models, api, _


class Property(models.Model):
    # This is a table name in DB will be set to estate_property
    _name = "estate.property"
    # Adding Mixin
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.published.mixin', 'website.seo.metadata']
    _description = "Estate Properties"

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')],
        default='new', string='Status', group_expand='_expand_state')
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Monetary(string="Expected Price", tracking=True)
    best_offer = fields.Monetary(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Monetary(string="Selling Price", readonly=True)
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation", default='north')
    # "estate.property.offer" --> Core model, "property_id" --> Inverse field
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    sales_id = fields.Many2one("res.users", string="Salesman")
    buyer_id = fields.Many2one("res.partner", string="Buyer", domain=[("is_company", "=", True)])
    # Related field
    phone = fields.Char(string="Phone", related="buyer_id.phone")
    currency_id = fields.Many2one("res.currency", string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id)

    # E.g. Depends
    # Note: Always prefer Computed fields, because it is triggered outside the context of the form view.
    # @api.depends('living_area', 'garden_area')
    # def _compute_total_are(self):
    #     for rec in self:
    #         rec.total_are = rec.living_area + rec.garden_area

    # # Can assign function to "compute" either as a string or as a func. reference.
    # total_are = fields.Integer(string="Total Area", compute=_compute_total_are)

    # E.g. Onchange
    # Note: Onchange is triggered within the form view.
    @api.onchange('living_area', 'garden_area')
    def _onchange_total_are(self):
        self.total_are = self.living_area + self.garden_area

    total_are = fields.Integer(string="Total Area")

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'canceled'

    offer_count = fields.Integer(string="Offer Count", compute="_compute_offer_count")

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',
        }

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            if rec.offer_ids:
                rec.offer_count = len(rec.offer_ids)
            else:
                rec.offer_count = 0

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    # def action_url_action(self):
    #     """
    #     URL Action
    #     """
    #     return {
    #         'type': 'ir.actions.act_url',
    #         'url': 'https://odoo.com',
    #         # When 'self' website opens on the same page.
    #         # 'target': 'self',
    #         'target': 'new',
    #     }

    def _get_report_base_filename(self):
        # To make sure just one record is obtained
        self.ensure_one()
        return 'Estate Property - %s' % self.name

    # def action_client_action(self):
    #     """For use in Client Action"""
    #     return {
    #         'type': 'ir.actions.client',
    #         # Tag 'reload' already has a widget. Accessing it out of the box.
    #         'tag': 'display_notification',
    #         'params': {
    #             'title': _('Testing Client Action notification.'),
    #             # success, warning, danger
    #             'type': 'success',
    #             'sticky': False,
    #         }
    #
    #         # 'tag': 'reload',
    #         #     'tag': 'apps'
    #     }

    def _compute_website_url(self):
        for rec in self:
            rec.website_url = "/properties/%s" % rec.id

    def action_send_email(self):
        mail_template = self.env.ref('real_estate_ads.mail_template')
        mail_template.send_mail(self.id, force_send=True)

    def _get_emails(self):
        # "self.offer_ids.mapped('partner_email')" returns list
        return ','.join(self.offer_ids.mapped('partner_email'))

    def _expand_state(self, states, domain, order):
        return [
            # Expanding selection field
            key for key, dummy in type(self).state.selection
        ]


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
