App.View.InputForm = Backbone.View.extend({

    tagName: 'table',

    events: {
        'change input': 'update',
    },

    commonTemplate: _.template('' +
        '<tr class="table-break">' +
        '   <td>Platform</td>' +
        '   <td>' +
        '       <input name="platform" value="<%= platform %>">' +
        '   </td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Organism</td>' +
        '   <td>' +
        '       <input name="organism" value="<%= organism %>">' +
        '   </td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Cell</td>' +
        '   <td><%= cell %></td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Perturbation</td>' +
        '   <td><%= perturbation %></td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Gene</td>' +
        '   <td><%= gene %></td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Disease</td>' +
        '   <td><%= disease %></td>' +
        '</tr>' +
        '<tr class="table-break">' +
        '   <td>Method</td>' +
        '   <td>' +
        '       <select>' +
        '           <option>Characteristic direction</option>' +
        '       </select>' +
        '   </td>' +
        '</tr>'
    ),

    initialize: function(options) {
        this.model.on('change', this.render, this);
        this.render();
        App.EventAggregator.on('clear:form', this.clear, this);
    },
    
    render: function() {
        var jsonModel = this.model.toJSON();
        this.$el.html(this.template(jsonModel) + this.commonTemplate(jsonModel));
        this.$el.show();
    },

    set: function(qs) {
        _.each(qs, function(value, field) {
            this.model.set(field, value);
        }, this);
    },

    clear: function() {
        _.each(this.model.attributes, function(val, key) {
            this.model.set(key, '');
        }, this);
    },

    submit: function(evt) {
        evt.preventDefault();
        this.model.save().then(function() {
            debugger;
        });
    },

    update: function(evt) {
        debugger;
        var $changedEl = $(evt.currentTarget),
            value = $changedEl.val(),
            id = $changedEl.attr('name');

        console.log('setting model ' + id + ' with value ' + value);
        if (value.indexOf(',') > 0) {
            this.model.set(id, value.split(','));
        } else if (value.indexOf('+') > 0) {
            this.model.set(id, value.replace('+', ' '));
        } else {
            this.model.set(id, value);
        }
    }
});


App.View.GeoForm = App.View.InputForm.extend({

    template: _.template('' +
        '<tr id="dataset">' +
        '   <td>Dataset</td>' +
        '   <td>' +
        '       <input name="dataset" value="<%= dataset %>">' +
        '   </td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Examples</td>' +
        '   <td>' +
        '       <input name="A_cols" value="<%= A_cols %>">' +
        '   </td>' +
        '</tr>' +
        '<tr>' +
        '   <td>Controls</td>' +
        '   <td>' +
        '       <input name="B_cols" value="<%= A_cols %>"' +
        '   </td>' +
        '</tr>'
    ),

    example: function() {
        console.log('building example');
        var qs = {
            'dataset': 'GDS5077',
            'platform': 'GPL10558',
            'organism': 'Homo sapiens',
            'A_cols': 'GSM1071454,GSM1071455',
            'B_cols': 'GSM1071457,GSM1071456'
        }
        App.router.navigate($.param(qs), { trigger: true, replace: true });
    }
});


App.View.UploadForm = App.View.InputForm.extend({

    template: _.template('' +
        '<tr>' +
        '   <td>File</td>' +
        '   <td>Filename' +
        '   </td>' +
        '</tr>'
    )
});
