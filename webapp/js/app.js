var App = {
    Collection: {},
    Model: {},
    View: {}
};

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
        geo: new App.View.GeoInputForm({
            parent: page
        }),
        custom: new App.View.CustomInputForm({
            parent: page
        })
    };

    /* Abstraction allowing for easy handling of an arbitrary number of content
     * views.
     */
    App.show = function(view) {
        if (App.contentViews.current) {
            $(App.contentViews.current.el).hide();
        }
        App.contentViews.current = view;
        $(App.contentViews.current.el).show();
    };

    App.Router = Backbone.Router.extend({
        routes: {
            '': 'index',
            'geo': 'geo',
            'custom': 'custom'
        },
        index: function() {
            App.show(App.contentViews.index);
        },
        geo: function() {
            App.show(App.contentViews.geo);
        },
        custom: function() {
            App.show(App.contentViews.custom);
        }
    });
    new App.Router();
    Backbone.history.start();
});
