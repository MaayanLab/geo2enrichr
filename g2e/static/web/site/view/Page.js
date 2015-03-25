App.View.Page = Backbone.View.extend({

    id: 'wrapper',

    tagName: 'div',

    events: {
        'click nav a': 'click'
    },

    initialize: function(options) {
        var template = App.renderTemplate('page'),
            footer = App.renderTemplate('footer');
        this.$el.append(template);
        $('body').append(this.el);
        this.$el.after(footer);
        this.$nav = this.$el.find('nav');
    },

    click: function(evt) {
        this.setNav(evt.target.className);
    },

    setNav: function(route) {
        var $elem;
        if (route === 'results') {
            this.$nav.hide();
        } else {
            this.$nav.show();
        }
        this.$el.find('nav a').removeClass('selected');
        $elem = this.$el.find('.' + route);
        if ($elem.length) {
            $elem.addClass('selected');
        }
    }
});
