App.View.Form = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click button': 'submit',
        'change select#diffexp_method': 'methodChange',
        'change select#correction_method' : 'correctionChange'
    },

    initialize: function(options) {
        // This view's visibility is handled in app.js.
        this.$el.hide();

        this.$form = $('<form></form>');
        this.$el.append(this.$form);

        var templateData = this.model.toJSON();
        this.$form.append( App.renderTemplate('form-required', templateData) );
        this.$options = $('<div id="options"></div>');
        this.$options.append( App.renderTemplate('form-options-chdir', templateData) );
        this.$form.append( this.$options );
        this.$form.append( App.renderTemplate('form-metadata', templateData) );
        this.$form.append('<button>Extract gene lists</button>');

        options.parent.$el.find('#content').append(this.el);
        this.model.on('change', this.render, this);
        App.EventAggregator.on('clear:form', this.clear, this);
    },

    methodChange: function(evt) {
        var diffexp_method = $(evt.target).val(),
            template = this.model.toJSON();
        this.$options.empty();
        if (diffexp_method === 'ttest') {
            this.$options.append( App.renderTemplate('form-options-ttest', template) );
        } else {
            this.$options.append( App.renderTemplate('form-options-chdir', template) );
        }
    },

    correctionChange: function(evt) {
        var correction_method = $(evt.target).val();
        if (correction_method === 'none') {
            $('#threshold_row').hide();
        } else {
            $('#threshold_row').show();
        }
    },

    submit: function(evt) {
        evt.preventDefault();
        var loader = new App.View.LoadingScreen({
                parent: this
            }),
            $forms = $('form'),
            formData = new FormData($forms[0]);

        _.each($forms.find('select'), function(select) {
            var $select = $(select),
                key = $select.attr('name'),
                val = $select.val();
            formData.append(key, val);
        });

        $.ajax({
            url: '/g2e/api/extract/upload',
            type: 'POST',
            data: formData,
            // Tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false,
            success: function(data) {
                loader.stop();
                App.router.navigate(
                    'results/' + data.extraction_id,
                    { trigger: true }
                );
                return false
            },
            error: function(data) {
                loader.stop();
                console.log(data);
                alert('Unknown error uploading data. Please contact the Ma\'ayan lab if this persists.');
            }
        });
    },

    loadExample: function() {
        App.router.navigate(
            'results/1',
            { trigger: true }
        );
    }
});
