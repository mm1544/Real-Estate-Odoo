from odoo import http
from odoo.http import request

# Example of importing controller. Need to inherit imported controller and extend it.
from odoo.addons.real_estate_ads.controllers.main import PropertyController


class PropertyController(http.Controller):

    # @http.route(['/properties'], type='http', website=True, auth="public",
    # method="POST", cors="*", csrf=True)
    @http.route(['/properties'], type='http', website=True, auth="public")
    def show_properties(self):
        # Can't use 'self.env'. Need to use 'request.env'
        # For trainiing purposes not authenticating this endpoint, but using sudo()
        # proprty_ids = request.env['estate.property'].search([]).sudo().search([])
        proprty_ids = request.env['estate.property'].search([]).search([])
        print(proprty_ids)
        # "property_list" is template ID. "{"property_ids": proprty_ids}" -> passing data to template
        return request.render("real_estate_ads.property_list", {"property_ids": proprty_ids})
