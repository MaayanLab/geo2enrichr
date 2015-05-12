App.View.Footer = Backbone.View.extend({

    el: 'footer',
    
    template: _.template('' +
        '<a class="company" href="<%= link %>" target="_blank">' +
            '<img src="<%= image %>">' +
        '</a>'
    ),

    initialize: function(genelists) {
        var $div = $('<div id="share" class="wrapper"></div>');
        _.each(this.model.toJSON(), function(obj, i) {
            $div.append(this.template(obj));
        }, this);
        this.$el.append($div);
    },
});
