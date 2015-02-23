$(function() {
    var table = new Table([
        new Row({
            id: 'diffexp',
            name: 'Differential expression method',
            options: ['Characteristic direction', 'T-test']
        }),
        new Row({
            id: 'dataset',
            name: 'Dataset',
            onEditPrompt: 'Please enter a valid dataset accession number:'
        }),
        new Row({
            id: 'platform',
            name: 'Platform',
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
            onEditPrompt: 'Please enter a comma-separated list of sample accession numbers:'
        }),
        new Row({
            id: 'experimental',
            name: 'Experimental samples',
            onEditPrompt: 'Please enter a comma-separated list of sample accession numbers:'
        })
    ]);

    new RequiredTable({
        collection: table
    });
});
