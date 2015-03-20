App.View.GeneList = Backbone.View.extend({

    tagName: 'tr',

    className: 'geneList',

    template: _.template('' +
        '<td><%= direction %></td>' +
        '<td>' +
            '<a href="<%= text_file %>" target="_blank">Download</a>' +
        '</td>' +
        '<td>' +
            '<a href="<%= enrichr_link %>" target="_blank">Open link</a>' +
        '</td>'
    ),

    initialize: function(options) {
        debugger;
        options.direction = this.getDirection(options.direction);
        this.$el.append(this.template(options));
    },

    getDirection: function(direction) {
        if (direction === 1) {
            return 'Up';
        } else if (direction === -1) {
            return 'Down';
        // Else direction should be 0.
        } else {
            return 'Combined';
        }
    }
});
