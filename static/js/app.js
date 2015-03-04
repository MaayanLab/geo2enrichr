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
    (this.parent || parent).$el.append(this.el);
    return this;
}
Backbone.View.prototype.after = function(elem) {
    elem.$el.after(this.el);
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

    App.objectFromQueryString = function(queryString) {
        if (_.isNull(queryString) || _.isUndefined(queryString))
            return '';
        var result = {},
            queryString = queryString.split('&');
        _.each(queryString, function(frag) {
            f = frag.split('=');
            result[f[0]] = f[1];
        });
        return result;
    };

    App.Router = Backbone.Router.extend({
        routes: {
            '(?*queryString)': 'index',
            'geo(?*queryString)': 'geo',
            'upload(?*queryString)': 'upload',
            'documentation': 'documentation',
            'about': 'about'
        },
        index: function() {
            App.contentViews.index.hide();
            //App.show(App.contentViews.index);
        },
        geo: function(queryString) {
            console.log('index page being rebuilt with:');
            console.log(arguments);
            App.contentViews.index.inputForm.render({
                path: 'geo',
                queryString: App.objectFromQueryString(queryString)
            });
            App.show(App.contentViews.index);
        },
        upload: function(queryString) {
            console.log('index page being rebuilt with:');
            console.log(arguments);
            App.contentViews.index.inputForm.render({
                path: 'upload',
                queryString: App.objectFromQueryString(queryString)
            });
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
    Backbone.history.start({
        root: '/g2e'
    });
});
