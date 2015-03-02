App.Model.Field = Backbone.Model.extend({
    defaults: {
        id: '',
        name: '',
        value: '',
        required: false,
        editable: false
    }
});

App.Model.Input = App.Model.Field.extend({
    defaults: {}
});

App.Model.Option = App.Model.Field.extend({
    defaults: {
        options: []
    }
});

App.Model.TextArea = App.Model.Field.extend({
    defaults: {}
});

App.Model.File = App.Model.Field.extend({
    defaults: {}
});
