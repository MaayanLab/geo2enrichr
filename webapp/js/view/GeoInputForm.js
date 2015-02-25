App.View.GeoInputForm = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click .submit-btn': 'submit'
    },

    initialize: function(options) {
        this.parent = options.parent;
        this.requiredTable = new App.View.RequiredTable({
            parent: this,
            collection: new Table([
                new Row({
                    id: 'diffexp',
                    name: 'Differential expression method',
                    options: ['Characteristic direction', 'T-test']
                }),
                new Row({
                    id: 'dataset',
                    name: 'Dataset',
                        value: 'GDS5077',
                        onEditPrompt: 'Please enter a valid dataset accession number:'
                    }),
                new Row({
                    id: 'platform',
                    name: 'Platform',
                    value: 'GPL10558',
                    onEditPrompt: 'Please enter a valid platform accession number:'
                }),
                new Row({
                    id: 'organism',
                    name: 'Organism',
                    onEditPrompt: 'Please enter a support species ("Homo Sapiens" or "Mus Musculus"):'
                }),
                new Row({
                    id: 'control',
                    name: 'Control samples',
                    value: 'GSM1071454, GSM1071455',
                    onEditPrompt: 'Please enter a comma-separated list of sample accession numbers:'
                }),
                new Row({
                    id: 'experimental',
                    name: 'Experimental samples',
                    value: 'GSM1071457, GSM1071456',
                    onEditPrompt: 'Please enter a comma-separated list of sample accession numbers:'
                })
            ])
        });

        this.metadataTable = new App.View.MetadataTable({
            parent: this,
            collection: new Table([
                new Row({
                    id: 'cell',
                    name: 'Cell type or tissue',
                    value: 'No data'
                }),
                new Row({
                    id: 'perturbation',
                    name: 'Perturbation',
                    value: 'No data'
                }),
                new Row({
                    id: 'gene',
                    name: 'Manipulated gene**',
                    value: 'No data'
                }),
                new Row({
                    id: 'disease',
                    name: 'Disease**',
                    value: 'No data'
                })
            ])
        });

        this.submissionPanel = new App.View.SubmissionPanel({
            SERVER: 'http://localhost:8083/g2e'
        });

        this.render();
    },

    render: function() {
        this.parent.$el.append(this.$el.hide());
        this.$el.append(this.requiredTable.$el);
        this.$el.append(this.metadataTable.$el);
        this.$el.append(this.submissionPanel.$el);
    },

    submit: function() {
        this.submissionPanel.submit({
            dataset: this.requiredTable.collection.get('dataset').get('value'),
            platform: this.requiredTable.collection.get('platform').get('value'),
            A_cols: this.requiredTable.collection.get('control').get('value').replace(/ /g,'').split(','),
            B_cols: this.requiredTable.collection.get('experimental').get('value').replace(/ /g,'').split(',')
        });
    }
});
