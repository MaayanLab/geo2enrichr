App.View.TextArea = Backbone.View.extend({

    tagName: 'textarea',

    events: {
        'change': 'change'
    },

    initialize: function() {
        App.EventAggregator.on('mode:change', this.update, this);
    },

    change: function() {
        this.model.set('value', $(arguments[0].currentTarget).val());
    },

    update: function(mode) {
        if (mode === 'custom') {
            this.show();
        } else {
            this.hide();
        }
    }
});
