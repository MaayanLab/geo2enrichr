App.View.Row = Backbone.View.extend({

    tagName: 'tr',

    events: {
        'click td': 'edit'
    },

    template: _.template('' +
        '<td><%= name %></td>' +
        '<% if (typeof(options) !== "undefined") { %>' +
            '<td>' +
                '<select>' +
                    '<% _.each(options, function(opt) { %>' +
                        '<option><%= opt %></option>' +
                    '<% }); %>' + 
                '</select>' +
            '</td>' +
        '<% } else if (input) { %>' +
            '<td>' +
                '<input placeholder="<%= value %>">' +
            '</td>' +
        '<% } else { %>' +
            '<td><%= value %></td>' +
        '<% } %>'
    ),

    initialize: function(options) {
        this.model = options.model;
        this.model.on('change', this.update, this);
        this.render();
    },

    render: function() {
        if (!this.model.get('editable')) {
            this.$el.addClass('locked');
        }
    },

    update: function() {
        this.$el.find('td').eq(0).html(this.model.get('name'));
        this.$el.find('td').eq(1).html(this.model.get('value'));
        if (this.model.get('editable')) {
            this.$el.removeClass('locked');
        } else {
            this.$el.addClass('locked');
        }
    },

    edit: function() {
        if (this.model.get('editable') && this.model.get('prompt')) {
            var val = prompt(this.model.get('prompt'), this.model.get('value'));
            this.model.set('value', val || this.model.get('value'));
        }
    }
});
