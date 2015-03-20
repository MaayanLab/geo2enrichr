App.View.Tutorial = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('tutorial');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    },
});
