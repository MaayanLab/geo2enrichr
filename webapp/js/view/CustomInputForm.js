App.View.CustomInputForm = Backbone.View.extend({

    tagName: 'div',


    className: 'content',

    template: '' +
        '<h3>Please page a gene list</h3>' +
        '<textarea style="width:300px;height:400px;" name="list" placeholder="Please enter a gene list">' +
        '</textarea>',

    events: {
        'click .submit-btn': 'submit'
    },

    initialize: function(options) {
        this.parent = options.parent;
        this.submissionPanel = new App.View.SubmissionPanel({
            SERVER: 'http://localhost:8083/g2e'
        });
        this.render();
    },

    render: function() {
        this.parent.$el.append(this.$el);
        this.$el.append(this.template);
        this.$el.append(this.submissionPanel.$el);
    },

    submit: function() {
        var inputString = this.$el.find('textarea').val();
        this.submissionPanel.submitCustomSoftFile(inputString);
    },

    processTextarea: function(textarea) {
        var lines = textarea.split('\n'),
            names = lines[0].split('\t'),
            samples = lines[1].split('\t'),
            genes = [],
            values = [],
            A_indices = [],
            B_indices = [];

        // Remove unnecessary columns.
        names.shift();
        samples.shift();
        lines.shift()
        lines.shift();

        _.each(samples, function(val, i) {
            if (val === '0') {
                A_cols.push(i);
            } else if (val === '1') {
                B_cols.push(i);
            }
        });

        result = {
            genes: [],
            A: [],
            B: []
        };

         _.each(lines, function(line, i) {
             line = line.split('\t')
             genes.push(line[0])
             line.shift();
             values.push(line)
        });
   

        console.log(genes.length === values.length);

        return {
            genes: genes/*,
            values: values,
            A_cols: A_cols,
            B_cols: B_cols*/
        };
    }
});
