var App = {
    Collection: {},
    Model: {},
    View: {},
    EventAggregator: _.extend({}, Backbone.Events),
    BASE: 'http://localhost:8083',
    SERVER: 'http://localhost:8083/g2e'
};

/* Update Backbone's API for common functionality.
 */
Backbone.View.prototype.show = function() {
    this.$el.show();
    return this;
}
Backbone.View.prototype.hide = function() {
    this.$el.hide();
    return this;
}
Backbone.View.prototype.appendTo = function(parent) {
    var paren = this.parent || parent;
    var html;
    if (this.template && this.model) {
        html = this.$el.append(this.template(this.model.toJSON()));
    } else if (this.template) {
        html = this.$el.append(this.template());
    } else {
        html = this.el;
    }
    paren.$el.append(html);
    return this;
}
Backbone.View.prototype.after = function(elem) {
    var html;
    if (this.template && this.model) {
        html = this.$el.append(this.template(this.model.toJSON()));
    } else if (this.template) {
        html = this.$el.append(this.template());
    } else {
        html = this.el;
    }
    elem.$el.after(html);
    return this;
}

$(function() {

    /* Bootstraps the page to the DOM, creating the header, nav, and footer.
     */
    var page = new App.View.Page();

    /* contentViews are replaceable views in the SAP; other views are static. 
     */
    App.contentViews = {
        index: new App.View.Index({
            parent: page
        }),
        about: new App.View.About({
            parent: page
        }),
        documentation: new App.View.Documentation({
            parent: page
        })
    };

    /* Abstraction allowing for easy handling of an arbitrary number of content
     * views.
     */
    App.show = function(view) {
        _.each(App.contentViews, function(v) {
            v.hide();
        });
        view.show();
    };

    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'documentation': 'documentation',
            'about': 'about'
        },
        index: function() {
            App.show(App.contentViews.index);
        },
        documentation: function() {
            App.show(App.contentViews.documentation);
        },
        about: function() {
            App.show(App.contentViews.about);
        }
    });
    App.router = new App.Router();
    Backbone.history.start();
});
