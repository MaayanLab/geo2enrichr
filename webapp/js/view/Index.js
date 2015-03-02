App.View.Index = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click button': 'click'
    },

    template: _.template('' +
        '<nav>' +
        '   <button data-command="geo">GEO</button>' +
        '   <button data-command="custom">Custom</button>' +
        '   <button data-command="clear">Clear</button>' +
        '   <button data-command="mock">Mock</button>' +
        '</nav>' +
        '<div id="input-form"></div>'
    ),

    commands: {
        'clear': function() {
            App.EventAggregator.trigger('clear:form');
        },
        'mock': function() {
            App.EventAggregator.trigger('mock:input');
        }
    },

    initialize: function(options) {
        this.parent = options.parent;
        

        this.collection = App.Collection.inputTableFactory();
        this.inputForm = new App.View.InputForm({
            collection: this.collection
        });

        this.submissionPanel = new App.View.SubmissionPanel({
            collection: this.collection,
            parent: this.inputForm//,
            //textArea: this.textArea
        });
        
        this.resultsPanel = new App.View.ResultsPanel();
        this.render();
    },

    render: function() {
        this.$el.html(this.template());
        this.appendTo();
        this.$el.find('#input-form').append(this.inputForm.el);
        this.resultsPanel.appendTo(this);
        this.submissionPanel.appendTo(this.inputForm);
    },

    click: function(evt) {
        var cmd = $(evt.currentTarget).attr('data-command');
        if (this.commands[cmd]) {
            this.commands[cmd]();
            return;
        }
        App.EventAggregator.trigger('change:mode', cmd);
    }
});
