/* Handles the file upload form.
 */

$(function() {

    $('button').click(submit);
    $('select.diffexp_method').change(methodChange);
    setupTagFunctionality();

    var $chdir = $('.chdir'),
        $ttest = $('.ttest');

    $ttest.hide();

    function submit(evt) {
        evt.preventDefault();
        var $forms = $('form'),
            formData = new FormData($forms[0]),
            loader = Loader(),
            $tags = $('#tags'),
            tagValues = [];

        _.each($forms.find('select'), function(select) {
            var $select = $(select),
                key = $select.attr('name'),
                val = $select.val();
            formData.append(key, val);
        });

        _.each($tags.find('li'), function(tag) {
            var value = $(tag).find('.tagit-label').html();
            if (typeof value !== 'undefined') {
                tagValues.push(value);
            }
        });

        formData.append('tags', tagValues);
        formData.append('normalize', 'False');

        $.ajax({
            url: '/g2e/api/extract/upload',
            type: 'POST',
            data: formData,
            // Tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false,
            success: function(data) {
                window.location.replace('/g2e/results/' + data.extraction_id);
            },
            error: function(data) {
                alert('Unknown error uploading data. Please contact the Ma\'ayan lab if this persists.');
            },
            complete: function() {
                loader.stop();
            }
        });
    }

    function methodChange(evt) {
        var diffexp_method = $(evt.target).val();
        if (diffexp_method === 'ttest') {
            $chdir.hide();
            $ttest.show();
        } else {
            $chdir.show();
            $ttest.hide();
        }
    }

    function setupTagFunctionality() {
        $("#tags").tagit();
    }

    function Loader() {
        var $el = $('<div class="loading"><div class="loader"><div class="modal">Loading...</div></div></div>');
        $('body').append($el);
        return {
            stop: function() {
                $el.remove();
            }
        }
    }

});