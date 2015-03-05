App.View.Index = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click button': 'example'
    },

    template: _.template('' +
        '<nav>' +
        '   <a href="#soft/geo">GEO</a>' +
        '   <a href="#soft/upload">Upload</a>' +
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
        this.geoForm = new App.View.GeoForm({
            model: new App.Model.SoftFile()
        });
        this.uploadForm = new App.View.UploadForm({
            model: new App.Model.SoftFile()
        });

        /*this.submissionPanel = new App.View.SubmissionPanel({
            parent: this.inputForm
        });*/
       // this.resultsPanel = new App.View.ResultsPanel();

        this.$el.html(this.template());

        options.parent.$el.append(this.el);
        this.$el.find('#input-form').append(this.geoForm.el);
        this.$el.find('#input-form').append(this.uploadForm.el);
    
        //this.uploadForm.hide();

        //this.resultsPanel.appendTo(this);
        //this.submissionPanel.appendTo(this.inputForm);
    },

    rerender: function(mode, qs) {
        if (mode === 'upload') {
            this.uploadForm.set(qs);
            this.uploadForm.render();
            this.geoForm.$el.hide();
        } else {
            this.uploadForm.$el.hide();
            this.geoForm.set(qs);
            this.geoForm.render();
        }
    },
});
