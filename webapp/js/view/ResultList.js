App.View.ResultList = Backbone.View.extend({

    tagName: 'table',

    events: {
        'click tr td a': 'download'
    },

    template: _.template('' +
        '<% _.each(genes, function(value, gene) { %>' +
            '<tr>' +
                '<td><%= gene %></td><td><%= value %></td>' +
            '</tr>' +
        '<% }); %>'
    ),

    initialize: function(options) {
        this.model = options.model;
        this.model.on('change', this.render, this);
    },

    render: function() {
        var html = this.template({
            genes: this.model.get('genes')
        });
        this.$el.html(html);
    }
});
