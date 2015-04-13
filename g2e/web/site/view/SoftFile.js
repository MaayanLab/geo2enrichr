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
            '<td>Normalized</td>' +
            '<td><%= normalize %></td>' +
        '</tr>' +
        '<tr title="Parsed and cleaned SOFT file, with GEO metadata removed and only the control and samples listed.">' +
            '<td>Parsed SOFT file</td>' +
            '<td>' +
                '<a href="<%= text_file %>" target="_blank">Download</a>' +
            '</td>' +
        '</tr>'
    ),

    initialize: function(data) {
        if (data.normalize === 'true') {
            data.normalize = 'True';
        } else {
            data.normalize = 'False';
        }
        if (data.is_geo) {
            data.nameTitle = 'GEO accession number';
        } else {
            data.nameTitle = 'Description';
        }
        this.$el.append(this.template(data));
    }
});
