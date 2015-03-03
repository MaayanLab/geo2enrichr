App.View.InputForm = Backbone.View.extend({

    tagName: 'form',
    
    mode: 'geo',

    mockUsed: false,
    
    initialize: function(options) {
        this.render();
        App.EventAggregator.on('clear:form', this.clear, this);
        App.EventAggregator.on('change:mode', this.change, this);
        App.EventAggregator.on('mock:input', this.mock, this);
    },

    render: function() {
        var $table = $('<table></table>');
        this.$el.append($table);
        this.collection.each(function(f) {
            var field;
            if (f instanceof App.Model.Input) {
                field = new App.View.Input({ model: f });
            } else if (f instanceof App.Model.Option) {
                field = new App.View.Option({ model: f });
            } else if (f instanceof App.Model.TextArea) {
                field = new App.View.TextArea({ model: f });
            } else if (f instanceof App.Model.File) {
                field = new App.View.File({ model: f });
            }
            $table.append(field.el);
        }, this);
        this.secure();
    },
   
    secure: function() {
        this.collection.each(function(model) {
            var triFlag = model.get(this.mode);
            if (triFlag === 1) {
                model.set('hide', false);
                model.set('disabled', false);
            } else if (triFlag === -1) {
                model.set('hide', true);
            } else {
                model.set('hide', false);
                model.set('disabled', true);
            }
        }, this);
    },

    change: function(mode) {
        this.mode = mode;
        var datasetModel = this.collection.where({ id: 'dataset' })[0];
        if (this.mode === 'upload') {
            datasetModel.set({ name: 'Name' });
        } else {
            datasetModel.set({ name: 'Dataset' });
        }
        this.secure();
        if (this.mockUsed) {
            this.mock();
        }
    },

    clear: function() {
        this.mockUsed = false;
        this.collection.each(function(model) {
            if (model.get('options')) {
                model.set('value', model.get('value'));
            } else {
                model.set('value', '');
            }
        });
    },

    mock: function() {
        this.mockUsed = true;
        this.collection.each(function(model) {
            var prop = model.get(this.mode + 'Mock');
            if (_.isUndefined(prop)) {
                model.set('value', '');
            } else {
                model.set('value', prop);
            }
        }, this);
    }
});
