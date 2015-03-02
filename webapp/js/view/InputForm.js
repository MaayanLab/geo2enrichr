App.View.InputForm = Backbone.View.extend({

    tagName: 'table',
    
    mode: 'geo',
    
    initialize: function(options) {
        this.collection = options.collection;
        this.render();
        App.EventAggregator.on('clear:form', this.clear, this);
        App.EventAggregator.on('change:mode', this.change, this);
        App.EventAggregator.on('mock:input', this.mock, this);
    },

    render: function() {
        this.collection.each(function(f) {
            var field;
            if (f instanceof App.Model.Input) {
                field = new App.View.Input({
                    model: f,
                    parent: this
                });
                field.appendTo(this);
            } else if (f instanceof App.Model.Option) {
                field = new App.View.Option({
                    model: f,
                    parent: this
                });
                field.appendTo(this);
            } else if (f instanceof App.Model.TextArea) {
                field = new App.View.TextArea({
                    model: f,
                    parent: this
                });
                field.appendTo(this);
            }
        }, this);
    },
    
    change: function(mode) {
        var datasetModel = this.collection.where({ id: 'dataset' })[0];
        if (mode === 'custom') {
            datasetModel.set({ name: 'Name' });
        } else {
            datasetModel.set({ name: 'Dataset' });
        }
        this.mode = mode;
    },

    clear: function() {
        this.collection.each(function(row) {
            row.set('value', '');
        });
    },

    mock: function() {
        if (this.mode === 'custom') {
            this.collection.where({'id':'dataset'})[0].set('value', 'My experimental data');
            this.collection.where({'id':'platform'})[0].set('value', 'NA');
            this.collection.where({'id':'organism'})[0].set('value', 'Homo Sapiens');
            this.collection.where({'id':'control'})[0].set('value', 'A, B, C, D');
            this.collection.where({'id':'experimental'})[0].set('value', 'E, F');
        } else {
            this.collection.where({'id':'dataset'})[0].set('value', 'GDS5077');
            this.collection.where({'id':'platform'})[0].set('value', 'GPL10558');
            this.collection.where({'id':'organism'})[0].set('value', 'Homo Sapiens');
            this.collection.where({'id':'control'})[0].set('value', 'GSM1071454, GSM1071455');
            this.collection.where({'id':'experimental'})[0].set('value', 'GSM1071457, GSM1071456');
            this.collection.where({'id':'cell'})[0].set('value', 'RUES2 stem cells');
            this.collection.where({'id':'perturbation'})[0].set('value', 'Depleted for transmembrane protein 88');
            this.collection.where({'id':'gene'})[0].set('value', 'TMEM 88');
        }
    }
});
