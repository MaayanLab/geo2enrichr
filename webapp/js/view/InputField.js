App.View.Field = Backbone.View.extend({

    tagName: 'tr',

    events: {
        'change': 'edit'
    },

    initialize: function(options) {
        this.model = options.model;
        this.model.on('change', this.render, this);
        App.EventAggregator.on('clear:form', this.clear, this);
        App.EventAggregator.on('change:mode', this.secure, this);
        debugger;
        this.render();
        this.secure();
    },
    
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
    },

    secure: function(mode) {
        mode = mode || 'geo';
        if (mode === 'geo' && this.model.get('disabled')) {
            this.disable();
        } else {
            this.enable();
        }
    },

    enable: function() {
        this.$el.find('*').last().prop('disabled', false);
        this.$el.find('td').eq(1).removeClass('disabled');
    },

    disable: function() {
        this.$el.find('*').last().prop('disabled', true);
        this.$el.find('td').eq(1).addClass('disabled');
    }
});

App.View.Option = App.View.Field.extend({

    template: _.template('' +
        '<td><%= name %></td>' +
        '<td>' +
            '<select>' +
                '<% _.each(options, function(opt) { %>' +
                    '<option><%= opt %></option>' +
                '<% }); %>' + 
            '</select>' +
        '</td>'
    ),

    initialize: function(options) {
        App.View.Field.prototype.initialize.apply(this, [options]);
    }
});

App.View.TextArea = App.View.Field.extend({

    template: _.template('' +
        '<td><%= name %></td>' +
        '<td><textarea placeholder="<%= value %>"></td>'
    ),

    initialize: function(options) {
        App.View.Field.prototype.initialize.apply(this, [options]);
    }
});

App.View.Input = App.View.Field.extend({

    template: _.template('' +
        '<td><%= name %></td>' +
        '<td><input value="<%= value %>"></td>'
    ),

    initialize: function(options) {
        App.View.Field.prototype.initialize.apply(this, [options]);
    }/*,

    edit: function(evt) {
        var val = $(evt.currentTarget).find('td input').val();
        this.model.set('value', val);
    }*/
});
