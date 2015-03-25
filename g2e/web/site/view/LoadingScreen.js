App.View.LoadingScreen = Backbone.View.extend({

    tagName: 'div',

    className: 'loading',

    template: '<div class="loader"><div class="modal">Loading...</div></div>',

    initialize: function(options) {
        options.parent.$el.append(this.$el.html(this.template))
    },

    stop: function() {
        this.$el.hide();
        this.$el.remove();
    }
});
