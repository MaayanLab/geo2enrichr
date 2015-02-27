App.Model.Row = Backbone.Model.extend({
    defaults: {
        id: '',
        name: '',
        value: '',
        prompt: undefined,
        options: undefined,
        required: false,
        editable: false,
        input: false
    }
});
