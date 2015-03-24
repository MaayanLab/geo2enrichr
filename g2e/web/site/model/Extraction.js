App.Model.Extraction = Backbone.Model.extend({
    
    urlRoot: '/g2e/api/extract',

    url: function() {
        return this.urlRoot + '/' + this.id;
    },

    defaults: {
        genelists: [
            {
                direction: null,
                enrichr_link: null,
                name: null,
                text_file: null
            },
            {
                direction: null,
                enrichr_link: null,
                name: null,
                text_file: null
            },
            {
                direction: null,
                enrichr_link: null,
                name: null,
                text_file: null
            }
        ],
        metadata: {
            cutoff: null,
            method: null
        },
        softfile: {
            is_geo: null,
            name: null,
            platform: null,
            stats: null,
            text_file: null
        }
    }
});
