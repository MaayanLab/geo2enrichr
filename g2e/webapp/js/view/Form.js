App.View.Form = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'change input': 'update',
    },

    initialize: function(options) {
        this.$el.hide();
        var template = App.renderTemplate('form', this.model.toJSON());
        options.parent.$el.find('#content').append(this.el);
        this.$el.append(template);
        this.model.on('change', this.render, this);
        App.EventAggregator.on('clear:form', this.clear, this);
    },
    
    render: function() {
        var jsonModel = this.model.toJSON();
    }
});
