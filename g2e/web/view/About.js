App.View.About = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    initialize: function(options) {
        this.$el.hide();
        template = App.renderTemplate('about');
        this.$el.append(template);
        options.parent.$el.find('#content').append(this.el);
    }
});
