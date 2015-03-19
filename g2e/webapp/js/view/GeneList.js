App.View.GeneList = Backbone.View.extend({

    tagName: 'div',

    className: 'geneList',

    template: _.template('' +
        '<h4><%= direction %> gene list</h4>' +
        '<ul>' +
            '<li>' +
                '<a href="<%= text_file %>" target="_blank">Download text file</a>' +
            '</li>' +
            '<li>' +
                '<a href="<%= enrichr_link %>" target="_blank">View results on Enrichr</a>' +
            '</li>' +
        '</ul>'
    ),

    initialize: function(options) {
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
