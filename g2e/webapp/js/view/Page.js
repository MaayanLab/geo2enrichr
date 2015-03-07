App.View.Page = Backbone.View.extend({

    el: '#page',

    initialize: function() {
        this.nav = new App.View.Nav();
        this.render();
    },

    render: function() {
        this.$el.append(this.nav.$el);
    }
});
