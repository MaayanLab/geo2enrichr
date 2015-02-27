App.View.Nav = Backbone.View.extend({

    tagName: 'nav',

    events: {
        'click a': 'navigate'
    },

    template: '' +
        '<h1><a data-src="">GEO2Enrichr</a></h1>' +
        '<ul>' +
        '   <li><a data-src="documentation">Documentation</a></li>' +
        '   <li><a data-src="about">About</a></li>' +
        '</ul>',

    initialize: function(options) {
        this.render();
    },

    render: function() {
        this.$el.append(this.template);
    },

    navigate: function(evt) {
        evt.preventDefault();
        var route = '#' + $(evt.currentTarget).attr('data-src');
        App.router.navigate(route, { trigger: true });
    }
});
