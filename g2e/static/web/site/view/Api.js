App.View.Api = Backbone.View.extend({

    tagName: 'div',

    className: 'content api',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('api');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    },
});
