App.View.SoftFile = Backbone.View.extend({

    tagName: 'div',

    className: 'softFile',

    template: _.template('' +
        '<h2>SOFT file</h2>' +
        '<ul>' +
            '<li><%= name %></li>' +
            '<li><%= platform %></li>' +
            '<li>' +
                '<a href="<%= text_file %>" target="_blank">Download cleaned SOFT file</a>' +
            '</li>' +
        '</ul>'
    ),

    initialize: function(options) {
        this.$el.append(this.template(options.softfile));
    }
});
