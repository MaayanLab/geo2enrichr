App.Collection.InputTable = Backbone.Collection.extend({
    model: App.Model.Field
});

App.Collection.inputTableFactory = function() {

    /* The properties "geo" and "upload" refer to which mode on which the input
     * field is activated. 1 indicates hide; -1 indicates show; 0 indicates show
     * but disable.
     */
    return new App.Collection.InputTable([
        new App.Model.Option({
            id: 'diffexp',
            name: 'Differential expression method',
            options: ['Characteristic direction', 'T-test'],
            backend: ['chdir', 'ttest'],
            value: 'Characteristic direction',
            geo: 1,
            upload: 1
        }),
        new App.Model.Option({
            id: 'cutoff',
            name: 'Gene list cutoff',
            options: ['500', '400', '300', '200', 'None'],
            value: '500',
            geo: 1,
            upload: 1
        }),
        new App.Model.Option({
            id: 'norm',
            name: 'Normalize data if necessary',
            options: ['Yes', 'No'],
            backend: ['True', 'False'],
            value: 'Yes',
            geo: 1,
            upload: 1
        }),
        new App.Model.File({
            id: 'file',
            name: 'SOFT file',
            value: '',
            hide: true,
            geo: -1,
            upload: 1,
            uploadMock: 'ExampleFile'
        }),
        new App.Model.Input({
            id: 'dataset',
            name: 'Dataset',
            value: '',
            geo: 0,
            geoMock: 'GDS5077',
            upload: -1
        }),
        new App.Model.Input({
            id: 'platform',
            name: 'Platform',
            value: '',
            geo: 0,
            geoMock: 'GPL10558',
            upload: 1
        }),
        new App.Model.Input({
            id: 'organism',
            name: 'Organism',
            value: '',
            geo: 0,
            geoMock: 'Homo Sapiens',
            upload: 1,
            uploadMock: 'Homo Sapiens'
        }),
        new App.Model.Input({
            id: 'control',
            name: 'Control samples',
            value: [],
            geo: 0,
            geoMock: ['GSM1071454', 'GSM1071455'],
            upload: -1,
        }),
        new App.Model.Input({
            id: 'experimental',
            name: 'Experimental samples',
            value: [],
            geo: 0,
            geoMock: ['GSM1071457', 'GSM1071456'],
            upload: -1
        }),
        new App.Model.Input({
            id: 'cell',
            name: 'Cell type or tissue',
            value: '',
            geo: 1,
            geoMock: 'RUES2 stem cells',
            upload: 1
        }),
        new App.Model.Input({
            id: 'perturbation',
            name: 'Perturbation',
            value: '',
            geo: 1,
            geoMock: 'Depleted for transmembrane protein 88',
            upload: 1
        }),
        new App.Model.Input({
            id: 'gene',
            name: 'Manipulated gene**',
            value: '',
            geo: 1,
            geoMock: 'TMEM 88',
            upload: 1
        }),
        new App.Model.Input({
            id: 'disease',
            name: 'Disease**',
            value: '',
            geo: 1,
            upload: 1,
        })
    ]);
}
