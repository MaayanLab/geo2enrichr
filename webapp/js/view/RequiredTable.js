var RequiredTable = Backbone.View.extend({

    el: $('#requiredData'),

    events: {
        'click .editable': 'edit'
    },

    template: _.template('' +
        '<tr id="<%= id %>">' +
            '<td><%= name %></td>' +
            '<% if (typeof(options) !== "undefined") { %>' +
                '<td>' +
                    '<select>' +
                        '<% _.each(options, function(opt) { %>' +
                            '<option><%= opt %></option>' +
                        '<% }); %>' + 
                    '</select>' +
                '</td>' +
            '<% } else { %>' +
                '<td class="value editable"><%= value %></td>' +
            '<% } %>' +
        '</tr>'
    ),

    initialize: function() {
        this.listenTo(this.collection, 'change', this.update);
        this.render();
    },

    render: function() {
        var self = this;
        self.collection.each(function(row) {
            self.$el.append(self.template(row.attributes));
        });
    },

    update: function(row) {
        var newVal = row.get('value');
        this.$el.find('#' + row.id + ' .editable').html(newVal);
    },

    edit: function(evt) {
        var id = $(evt.currentTarget).parent().attr('id'),
            cell = this.collection.get(id),
            existingVal = cell.get('value'),
            msg = cell.get('onEditPrompt'),
            newVal = prompt(msg, existingVal);
        cell.set('value', newVal);
	}
});
