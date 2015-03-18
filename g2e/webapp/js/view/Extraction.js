App.View.Extraction = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.parent = options.parent;
        this.parent.$el.append(this.el);
    },

    render: function() {
        _.each(this.model.get('genelists'), function(gl) {
            new App.View.GeneList({
                text_file: gl.text_file,
                enrichr_link: gl.enrichr_link,
                direction: gl.direction,
                parent: this
            });
        }, this);
    }
});
