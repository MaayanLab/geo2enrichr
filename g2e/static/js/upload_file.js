/* Handles the file upload form.
 */

$(function() {

    var ENDPOINT = 'upload_soft_file',
        $fileInput = $('#file-input td'),
        $useExampleButton = $('#example-file button'),
        $descriptionInput = $('#description-input input'),
        $chdir = $('.chdir'),
        $ttest = $('.ttest');

    $('button#upload-button').click(submit);
    $('select.diffexp_method').change(methodChange);
    $useExampleButton.click(showExample);
    setupTagFunctionality();

    $ttest.hide();

    function submit(evt) {
        evt.preventDefault();

        // There are other forms on the page.
        var $forms = $('#upload-form form'),
            formData = new FormData($forms[0]),
            loader = Loader();
        
        loader.start();

        $.each($forms.find('select'), function(i, select) {
            var $select = $(select),
                key = $select.attr('name'),
                val = $select.val();
            formData.append(key, val);
        });

        formData.append('normalize', 'False');

        $.ajax({
            url: '/g2e/api/extract/' + ENDPOINT,
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
                var jsonResponse = JSON.parse(data.responseText);
                if (jsonResponse.error) {
                    alert(jsonResponse.error);
                } else {
                    alert('Unknown error uploading data. Please contact the Ma\'ayan lab if this persists.');
                }
            },
            complete: function() {
                loader.stop();
            }
        });
    }

    function showExample() {
        ENDPOINT = 'example';
        $fileInput.html('Example File Selected');
        $('#example-file').hide();
        $descriptionInput.attr('value', 'example_input');
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
        $("#tags").tagit({
            singleField: true
        });
    }
});