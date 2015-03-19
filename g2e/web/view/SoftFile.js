App.View.SoftFile = Backbone.View.extend({

    tagName: 'table',

    template: _.template('' +
        '<caption>SOFT file</caption>' +
        '<tr>' +
            '<td>Name</td>' +
            '<td><%= name %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Platform</td>' +
            '<td><%= platform %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Cleaned text file</td>' +
            '<td>' +
                '<a href="<%= text_file %>" target="_blank">Download</a>' +
            '</td>' +
        '</tr>'
    ),

    initialize: function(data) {
        this.$el.append(this.template(data));
    }
});
