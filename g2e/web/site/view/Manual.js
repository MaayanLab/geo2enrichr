App.View.Manual = Backbone.View.extend({

    tagName: 'div',

    className: 'manual content',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('manual');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    },
});
