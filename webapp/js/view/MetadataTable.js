var MetadataTable = Backbone.View.extend({

    el: $('#metadataTable'),

    events: {
        'change input': 'edit'
    },

    template: _.template('' +
         '<tr id="<%= id %>">' +
            '<td class="title">' +
                '<label><%= name %></label>' +
            '</td>' +
            '<td class="value">' +
                '<input placeholder="<%= value %>">' +
            '</td>' +
        '</tr>'
    ),

    initialize: function() {
        this.render();
    },

    render: function() {
        var self = this;
        self.collection.each(function(row) {
            self.$el.append(self.template(row.attributes));
        });
    },

    edit: function(evt) {
        var id = $(evt.currentTarget).parents().eq(1).attr('id'),
            cell = this.collection.get(id),
            newVal = $(evt.currentTarget).val();
        cell.set('value', newVal);
    }
});
