App.View.Index = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click button': 'click'
    },

    mode: 'geo',

    template: _.template('' +
        '<button data-command="geo">GEO</button>' +
        '<button data-command="custom">Custom</button>' +
        '<button data-command="clear">Clear</button>'
    ),

    initialize: function(options) {
        this.parent = options.parent;
        

        this.collection = App.Collection.inputTableFactory();
        this.inputForm = new App.View.InputForm({
            collection: this.collection
        });
        this.textArea = new App.View.TextArea();
        this.submissionPanel = new App.View.SubmissionPanel({
            collection: this.collection,
            parent: this
        });
        
        this.resultsPanel = new App.View.ResultsPanel();
        this.render();
    },

    render: function() {
        this.appendTo();
        this.inputForm.appendTo(this);
        this.textArea.hide().appendTo(this.inputForm);
        this.submissionPanel.appendTo(this.inputForm);
        this.resultsPanel.appendTo(this);
    },

    click: function(evt) {
        var command = $(evt.currentTarget).attr('data-command');
        if (command === 'clear') {
            App.EventAggregator.trigger('clear');
            return;
        }
        
        if (command === 'custom') {
            this.textArea.show();
        } else if (command === 'geo') {
            this.textArea.hide();
        }
        this.inputForm.changeMode(command);
    }
});
