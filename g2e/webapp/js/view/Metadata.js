App.View.Metadata = Backbone.View.extend({

    tagName: 'table',

    className: 'metadata',

    template: _.template('' +
        '<caption>Metadata</caption>' +
        '<tr>' +
            '<td>Method</td>' +
            '<td><%= method %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Cutoff</td>' +
            '<td><%= cutoff %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Cell</td>' +
            '<td><%= cell %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Perturbation</td>' +
            '<td><%= perturbation %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Gene</td>' +
            '<td><%= gene %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Disease</td>' +
            '<td><%= disease %></td>' +
        '</tr>'
    ),

    initialize: function(data) {
        this.$el.append(this.template(data));
    }
});
