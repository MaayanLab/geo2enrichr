App.View.Page = Backbone.View.extend({

    id: 'wrapper',

    tagName: 'div',

    initialize: function() {
        var template = App.renderTemplate('page');
        var footer = App.renderTemplate('footer');
        this.$el.append(template);
        $('body').append(this.el);
        this.$el.after(footer);
    }
});
