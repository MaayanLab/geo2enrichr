var ResultList = Backbone.View.extend({

    tagName: 'table',

    events: {
        'click tr td a': 'download'
    },

    template: _.template('' +
        "<%_.forEach(up.genes, function (u) {%>"
        + "<%=u%>, "
        + "<%})%>"
    ),

    initialize: function(options) {
        console.log(options);
        debugger;
        var html = $(this.el).append(this.template(options.results));
        options.parent.$el.append(html);
    },

    download: function(evt) {
        debugger;
    }
});
