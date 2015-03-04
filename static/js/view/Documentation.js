App.View.Documentation = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    template: _.template('<h3>Documentation</h3>'),

    initialize: function(options) {
        this.appendTo(options.parent);
    },
});
