// Creating widget
odoo.define('real_estate_ads.CustomAction', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var CustomAction = AbstractAction.extend({
        template: "CustomActions",
        start: function() {
            console.log("Test Action 1.")
        }
    })

    // 'custom_client_action' is a Tag name
    core.action_registry.add("custom_client_action", CustomAction);
});