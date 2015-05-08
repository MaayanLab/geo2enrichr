App.View.GeneList = Backbone.View.extend({

    tagName: 'tr',

    className: 'geneList',

    template: _.template('' +
        '<td><%= direction %></td>' +
        '<td>' +
            '<a href="<%= text_file %>" target="_blank">' +
                '<img src="web/site/image/download.png">' +            
            '</a>' +
        '</td>' +
        '<td>' +
            '<a href="<%= enrichr_link %>" target="_blank">' +
                '<img src="web/site/image/targetapp/enrichr.png">' +
            '</a>' +
        '</td>' +
        '<% if (l1000cds2_link !== "") { %>' +
            '<td>' +
                '<a href="<%= l1000cds2_link %>" target="_blank">' +
                    '<img src="web/site/image/targetapp/l1000cds2.png">' +
                '</a>' +
            '</td>' +
        '<% } else { %>' +
            '<td></td>' +
        '<% } %>' + 
        '<% if (paea_link !== "") { %>' +
            '<td>' +
                '<a href="<%= paea_link %>" target="_blank">' +
                    '<img src="web/site/image/targetapp/paea.png">' +
                '</a>' +
            '</td>' +
        '<% } else { %>' +
            '<td></td>' +
        '<% } %>'
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
