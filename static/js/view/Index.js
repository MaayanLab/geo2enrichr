App.View.Index = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click a': 'click',
        'click button': 'example'
    },

    template: _.template('' +
        '<nav>' +
        '   <a href="#geo">GEO</a>' +
        '   <a href="#upload">Upload</a>' +
        '   <button>Example</button>' +
        '</nav>' +
        '<div id="input-form"></div>'
    ),

    commands: {
        'example': function() {
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
            parent: this.inputForm
        });
        this.resultsPanel = new App.View.ResultsPanel();

        this.$el.html(this.template());
        this.appendTo();
        this.$el.find('#input-form').append(this.inputForm.el);
        this.resultsPanel.appendTo(this);
        this.submissionPanel.appendTo(this.inputForm);
    },

    click: function(evt) {
        /* Get which link was just clicked. This is not in
         * Backbone.history.fragment.
         */
        var href = $(evt.currentTarget).attr('href').slice(1),
            mode = href === 'upload' ? 'upload' : 'geo';
       // App.EventAggregator.trigger('change:mode', mode);
    },

    getMode: function() {
        if (Backbone.history.fragment === '')
            return '';
        if (Backbone.history.fragment.indexOf('?') < 0)
            return Backbone.history.fragment;
        return Backbone.history.fragment.split('?')[0];
    },

    example: function() {
        console.log('Getting example with ' + this.getMode() + ' as mode');
        this.mode = this.getMode();
        this.queryString = {};
        this.collection.each(function(model) {
            var modelId = model.get('id'),
                prop = model.get(this.mode + 'Mock'),
                triFlag = model.get(this.mode);
            if (!_.isUndefined(prop)) {
                if (_.isArray(prop)) {
                    prop = prop.join(',');
                }
                this.queryString[modelId] = prop;
            }
        }, this);
        App.router.navigate(this.mode + '?' + $.param(this.queryString), { trigger: true, replace: true });
    }
});
