App.View.Field = Backbone.View.extend({

    tagName: 'tr',

    events: {
        'change': 'edit'
    },

    initialize: function(options) {
        this.model = options.model;
        this.model.on('change', this.render, this);
        this.render();
    },
    
    render: function() {
        console.log(this.model.get('id'));
        if (this.model.get('hide')) {
            this.hide();
        } else {
            this.show();
        }

        this.$el.html(this.template(this.model.toJSON()));
        if (this.model.get('disabled')) {
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
        '<td>' +
            '<textarea placeholder="<%= value %>"></textarea>' +
        '</td>'
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
    }
});
