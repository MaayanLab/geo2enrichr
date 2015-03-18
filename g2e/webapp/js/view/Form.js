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
    },

    set: function(qs) {
        _.each(qs, function(value, field) {
            this.model.set(field, value);
        }, this);
    },

    clear: function() {
        _.each(this.model.attributes, function(val, key) {
            this.model.set(key, '');
        }, this);
    },

    submit: function(evt) {
        evt.preventDefault();
        this.model.save().then(function() {
            debugger;
        });
    },

    update: function(evt) {
        debugger;
        var $changedEl = $(evt.currentTarget),
            value = $changedEl.val(),
            id = $changedEl.attr('name');

        console.log('setting model ' + id + ' with value ' + value);
        if (value.indexOf(',') > 0) {
            this.model.set(id, value.split(','));
        } else if (value.indexOf('+') > 0) {
            this.model.set(id, value.replace('+', ' '));
        } else {
            this.model.set(id, value);
        }
    }
});
