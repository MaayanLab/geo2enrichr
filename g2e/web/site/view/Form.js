App.View.Form = Backbone.View.extend({

    tagName: 'div',

    className: 'content',

    events: {
        'click button': 'submit',
    },

    initialize: function(options) {
        this.$el.hide();
        var template = App.renderTemplate('form', this.model.toJSON());
        options.parent.$el.find('#content').append(this.el);
        this.$el.append(template);
        this.model.on('change', this.render, this);
        App.EventAggregator.on('clear:form', this.clear, this);
    },

    submit: function() {
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
            type: 'PUT',
            data: formData,
            // Tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false,
            success: function(data) {
                debugger;
                loader.stop();
                App.router.navigate(
                    'results/' + data.extraction_id,
                    { trigger: true }
                );
            },
            error: function(data) {
                debugger;
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
