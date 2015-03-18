App.View.GeneList = Backbone.View.extend({

    tagName: 'div',

    className: 'geneList',

    template: _.template('' +
        '<h3><%= direction %> gene list</h3>' +
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
        options.direction = this.capitalize( options.direction );
        this.$el.append(this.template(options));
    },

    capitalize: function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
});
