App.View.InputForm = Backbone.View.extend({

    tagName: 'table',

    events: {
        'change input': 'update',
        'click button': 'example',
        'click a': 'submit'
    },

    template: _.template('' +
        '<tr>' +
        '   <td>Method</td>' +
        '   <td>' +
        '       <select>' +
        '           <option>Characteristic direction</option>' +
        '       </select>' +
        '   </td>' +
        '</tr>' +
        '<tr id="dataset">' +
        '   <td>Dataset</td>' +
        '   <td>' +
        '       <input name="dataset" value="<%= dataset %>">' +
        '   </td>' +
        '</tr>' +
        '<tr>' +
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
        '</tr>' +
        '<tr><td>Cell</td><td><%= cell %></td></tr>' +
        '<tr><td>Perturbation</td><td><%= perturbation %></td></tr>' +
        '<tr><td>Gene</td><td><%= gene %></td></tr>' +
        '<tr><td>Disease</td><td><%= disease %></td></tr>' +
        '<tr>' +
        '   <td><button>Example</button></td>' +
        '</tr>' +
        '<tr>' +
        '   <td><a href="">Submit</a></td>' +
        '</tr>' +
    ''),
    
    initialize: function(options) {
        this.$el.append(this.template(this.model.toJSON()));
        this.model.on('change', this.rerender, this);
        App.EventAggregator.on('clear:form', this.clear, this);
    },

    rerender: function() {
        this.$el.html(this.template(this.model.toJSON()));
    },

    clear: function() {
        _.each(this.model.attributes, function(val, key) {
            this.model.set(key, '');
        }, this);
    },

    render: function(url) {
        var mode = Backbone.history.location.href.split('#')[1];
        console.log('rerendering form on mode ' + mode);

        _.each(url.queryString, function(val, key) {
            this.model.set(key, val);
        }, this);

        if (mode === 'upload') {
            var ds = this.$el.find('#dataset');
            ds.find('td').first().html('File name');
            ds.find('tr').html('<div>Hi</div>');
            //this.$el.find('dataset').attr('disable');
            //this.$el.find('dataset').hide();
        }

        /* Certain options are only visible and/or editable on each mode.
         * Check that the correct options are selected.
         */
        //hash = Backbone.history.location.hash.split('?');
        //mode = hash.length ? hash[0].slice(1) : 'geo';
        //console.log('securing under mode ' + mode);
        /*this.collection.each(function(model) {
            var triFlag = model.get(mode);
            if (triFlag === 1) {
                model.set('hide', false);
                model.set('disabled', false);
            } else if (triFlag === -1) {
                model.set('hide', true);
            } else {
                model.set('hide', false);
                model.set('disabled', true);
            }
        }, this);*/

    },

    submit: function(evt) {
        evt.preventDefault();
        this.model.save().then(function() {
            debugger;
        });
    },

    update: function(evt) {
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
    },

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
