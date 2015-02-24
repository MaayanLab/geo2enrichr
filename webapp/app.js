$(function() {
    
    var requiredTable = new RequiredTable({
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

    var metadataTable = new MetadataTable({
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

    new SubmissionForm({
        SERVER: 'http://localhost:8083/g2e',
        requiredData: requiredTable.collection,
        metadata: metadataTable.collection
    });
});
