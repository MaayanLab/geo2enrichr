App.View.Pipeline = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('pipeline');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    },
});
