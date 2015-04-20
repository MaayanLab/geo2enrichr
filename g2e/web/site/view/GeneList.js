App.View.GeneList = Backbone.View.extend({

    tagName: 'tr',

    className: 'geneList',

    template: _.template('' +
        '<td><%= direction %></td>' +
        '<td title="Text file containing a gene list resulting from differential expression analysis.">' +
            '<a href="<%= text_file %>" target="_blank">Download</a>' +
        '</td>' +
        '<td title="Perform enrichment analysis against over 70 gene set libraries with Enrichr, a popular gene set enrichment analysis tool.">' +
            '<a href="<%= enrichr_link %>" target="_blank">Open Enrichr link</a>' +
        '</td>' +
        '<% if (l1000cds2_link !== "") { %>' +
            '<td title="Identify drugs that can potentially reverse expression using expression signatures from the LINCS L1000 small-molecule transcriptomics datasets processed with the Characteristic Direction method.">' +
                '<a href="<%= l1000cds2_link %>" target="_blank">Open L1000CD2 link</a>' +
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
