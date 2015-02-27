App.View.InputForm = Backbone.View.extend({

    tagName: 'table',

    initialize: function(options) {
        this.collection = options.collection;
        this.render();
        App.EventAggregator.on('clear', function() {
            this.clear();
        }, this);
    },

    render: function() {
        this.collection.each(function(row) {
            var rowView = new App.View.Row({ model: row });
            rowView.appendTo(this);
        }, this);
    },
    
    changeMode: function(mode) {
        var datasetModel = this.collection.where({ id: 'dataset' })[0],
            platformModel = this.collection.where({ id: 'platform' })[0],
            organismModel = this.collection.where({ id: 'organism' })[0],
            controlModel = this.collection.where({ id: 'control' })[0],
            experimentalModel = this.collection.where({ id: 'experimental' })[0];
        if (mode === 'custom') {
            datasetModel.set({ name: 'Name', editable: true });
            platformModel.set({ editable: true });
            organismModel.set({ editable: true });
            controlModel.set({ editable: true });
            experimentalModel.set({ editable: true });
        } else {
            datasetModel.set({ name: 'Dataset', editable: false });
            platformModel.set({ editable: false });
            organismModel.set({ editable: false });
            controlModel.set({ editable: false });
            experimentalModel.set({ editable: false });
        }
    },

    clear: function() {
        this.collection.each(function(row) {
            row.set('value', '');
        });
    }
});
