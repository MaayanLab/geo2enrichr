App.Collection.InputTable = Backbone.Collection.extend({
    model: App.Model.Field
});

App.Collection.inputTableFactory = function() {
    return new App.Collection.InputTable([
        new App.Model.Option({
            id: 'diffexp',
            name: 'Differential expression method',
            options: ['Characteristic direction', 'T-test']
            // This option is required but the user can't unselect it so we're fine.
        }),
        new App.Model.Input({
            id: 'dataset',
            name: 'Dataset',
            value: '',
            required: true,
            disabled: true
        }),
        new App.Model.Input({
            id: 'platform',
            name: 'Platform',
            value: '',
            required: true,
            disabled: true
        }),
        new App.Model.Input({
            id: 'organism',
            name: 'Organism',
            value: '',
            required: true,
            disabled: true
        }),
        new App.Model.Input({
            id: 'control',
            name: 'Control samples',
            value: '',
            required: true,
            disabled: true
        }),
        new App.Model.Input({
            id: 'experimental',
            name: 'Experimental samples',
            value: '',
            required: true,
            disabled: true
        }),
        new App.Model.Input({
            id: 'cell',
            name: 'Cell type or tissue',
            value: ''
        }),
        new App.Model.Input({
            id: 'perturbation',
            name: 'Perturbation',
            value: ''
        }),
        new App.Model.Input({
            id: 'gene',
            name: 'Manipulated gene**',
            value: ''
        }),
        new App.Model.Input({
            id: 'disease',
            name: 'Disease**',
            value: ''
        }),
        new App.Model.TextArea({
            id: 'textArea',
            name: 'Gene list',
            value: '',
            hide: true
        })
    ]);
}
