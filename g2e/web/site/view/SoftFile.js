App.View.SoftFile = Backbone.View.extend({

    tagName: 'table',

    template: _.template('' +
        '<caption>SOFT file</caption>' +
        '<tr>' +
            '<td><%= nameTitle %></td>' +
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
        if (data.is_geo) {
            data.nameTitle = 'GEO accession number';
        } else {
            data.nameTitle = 'Description';
        }
        this.$el.append(this.template(data));
    }
});
