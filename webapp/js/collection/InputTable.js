App.Collection.InputTable = Backbone.Collection.extend({
    model: App.Model.Row
});

App.Collection.inputTableFactory = function() {
    return new App.Collection.InputTable([
        {
            id: 'diffexp',
            name: 'Differential expression method',
            options: ['Characteristic direction', 'T-test'],
            required: true,
            editable: true
        },
        {
            id: 'dataset',
            name: 'Dataset',
            value: 'GDS5077',
            prompt: 'Please enter a valid dataset accession number:',
            required: true
        },
        {
            id: 'platform',
            name: 'Platform',
            value: 'GPL10558',
            prompt: 'Please enter a valid platform accession number:',
            required: true
        },
        {
            id: 'organism',
            name: 'Organism',
            prompt: 'Please enter a support species ("Homo Sapiens" or "Mus Musculus"):',
            required: true
        },
        {
            id: 'control',
            name: 'Control samples',
            value: 'GSM1071454, GSM1071455',
            prompt: 'Please enter a comma-separated list of sample accession numbers:',
        },
        {
            id: 'experimental',
            name: 'Experimental samples',
            value: 'GSM1071457, GSM1071456',
            prompt: 'Please enter a comma-separated list of sample accession numbers:',
        },
        {
            id: 'cell',
            name: 'Cell type or tissue',
            value: 'No data',
            editable: true,
            input: true
        },
        {
            id: 'perturbation',
            name: 'Perturbation',
            value: 'No data',
            editable: true,
            input: true
        },
        {
            id: 'gene',
            name: 'Manipulated gene**',
            value: 'No data',
            editable: true,
            input: true
        },
        {
            id: 'disease',
            name: 'Disease**',
            value: 'No data',
            editable: true,
            input: true
        }
    ]);
}
