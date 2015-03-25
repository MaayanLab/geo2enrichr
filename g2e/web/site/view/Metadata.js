App.View.Metadata = Backbone.View.extend({

    tagName: 'table',

    className: 'metadata',

    template: _.template('' +
        '<caption>Metadata</caption>' +
        '<tr>' +
            '<td>Differential expression method</td>' +
            '<td><%= method %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Cutoff</td>' +
            '<td><%= cutoff %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Cell type or tissue</td>' +
            '<td><%= cell %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Perturbation</td>' +
            '<td><%= perturbation %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Manipulated gene</td>' +
            '<td><%= gene %></td>' +
        '</tr>' +
        '<tr>' +
            '<td>Relevant disease</td>' +
            '<td><%= disease %></td>' +
        '</tr>'
    ),

    initialize: function(data) {
        this.$el.append(this.template(data));
    }
});
