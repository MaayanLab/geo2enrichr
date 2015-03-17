App.View.Results = Backbone.View.extend({

    tagName: 'div',

    initialize: function(options) {
        this.parent = options.parent;
    },

    render: function() {
        _.each(this.model.get('genelists'), function(gl) {
            new App.View.GeneList({
                text_file: gl.text_file,
                enrichr_link: gl.enrichr_link,
                direction: gl.direction,
                parent: this.parent
            });
        }, this);
    }
});
