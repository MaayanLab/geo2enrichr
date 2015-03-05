App.View.About = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    template: _.template('<h3>About</h3>'),

    initialize: function(options) {
        options.parent.$el.append(this.el);
    }
});
