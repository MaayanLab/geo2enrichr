App.View.Page = Backbone.View.extend({

    el: '#page',

    events: {},

    initialize: function() {
        this.$el.append(
            '<ul>' +
            '   <li><a href="#">Index</a></li>' +
            '   <li><a href="#geo">GEO</a></li>' +
            '   <li><a href="#custom">Custom</a></li>' +
            '</ul>');
    },

    render: function() {
    }
});
