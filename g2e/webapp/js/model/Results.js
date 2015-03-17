App.Model.Results = Backbone.Model.extend({
    
    urlRoot: '/g2e/extract?id=',

    url: function() {
        return this.urlRoot + this.id;
    },

    defaults: {
        cutoff: null,
        enrichr_link_up: null,
        enrichr_link_down: null
    }
});
