App.View.Tutorial = Backbone.View.extend({

    tagName: 'div',

    className: 'tutorial content',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('tutorial');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    },
});
