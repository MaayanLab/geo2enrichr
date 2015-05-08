App.View.GeneLists = Backbone.View.extend({

    tagName: 'table',

    id: 'geneLists',

    template: '' +
        '<caption>External Links and Downloads</caption>' +
        '<thead>' +
            '<tr>' +
                '<td></td>' +
                '<td title="Text file containing a gene list resulting from differential expression analysis.">Gene lists</td>' +
                '<td title="Perform enrichment analysis against over 70 gene set libraries with Enrichr, a popular gene set enrichment analysis tool.">Links to Enrichr</td>' +
                '<td title="Identify drugs that can potentially reverse expression using expression signatures from the LINCS L1000 small-molecule transcriptomics datasets processed with the Characteristic Direction method.">Link to L1000CDS2</td>' +
                '<td title="Perform principle angle enrichment analysis against over 70 gene set libraries.">Link to PAEA</td>' +
            '</tr>' +
        '</thead>',

    initialize: function(genelists) {
        this.$el.append(this.template);
        _.each(genelists, function(gl) {
            var gl = new App.View.GeneList({
                text_file: gl.text_file,
                enrichr_link: gl.enrichr_link,
                l1000cds2_link: gl.l1000cds2_link,
                paea_link: gl.paea_link,
                direction: gl.direction
            });
            this.$el.append(gl.el);
        }, this);
        this.invertTable();
    },

    invertTable: function() {
        var newRows = [];
        this.$el.find('tr').each(function(){
            $(this).find('th,td').each(function(i, td){
                if (_.isUndefined(newRows[i])) {
                    newRows[i] = $('<tr></tr>');
                }
                newRows[i].append(this);
            });
        });
        this.$el.find('tr').remove();
        _.each(newRows, function(tr) {
            this.$el.append(tr);
        }, this);
    }
});
