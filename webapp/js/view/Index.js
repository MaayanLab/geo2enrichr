App.View.Index = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.parent = options.parent;
        this.render();
    },

    render: function() {
        this.parent.$el.append(this.$el);
        this.$el.append(
            '<h1>GEO2Enrichr</h1>'
        );
    }
});
