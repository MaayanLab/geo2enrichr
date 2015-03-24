App.View.ShareButton = Backbone.View.extend({

    tagName: 'table',

    template: _.template('' +
        '<caption class="top">Share</caption>' +
        '<tr>' +
            '<td>Permanent link to these results</td>' +
            '<td><%= link %></td>' +
        '</td>'
    ),

    initialize: function() {
        this.$el.append(this.template({
            link: window.location.href
        }));
    }
});
