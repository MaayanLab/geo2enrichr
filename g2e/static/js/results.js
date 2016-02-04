$(function() {

    function invertGeneListsTable() {
        var $el = $('.gene-lists'),
            newRows = [];
        $el.find('tr').each(function () {
            $(this).find('th,td').each(function (i, td) {
                if (typeof newRows[i] === 'undefined') {
                    newRows[i] = $('<tr></tr>');
                }
                newRows[i].append(this);
            });
        });
        $el.find('tr').remove();
        $.each(newRows, function (i, tr) {
            $el.append(tr);
        });
    }

    function setupAdminControlsIfNecessary() {
        var $adminControls = $('#admin-controls');
        if (!$adminControls.length) {
            return;
        }
        $adminControls.find('#tags').tagit({
            singleField: true
        });
        $adminControls.find('#edit-gene-signature').click(submitEdit);

        function submitEdit(evt) {
            evt.preventDefault();

            var extractionId = $adminControls.find('input[name="extraction_id"]').val(),
                $forms = $adminControls.find('form'),
                formData = new FormData($forms[0]);

            $.ajax({
                url: '/g2e/results/' + extractionId + '/edit',
                type: 'POST',
                data: formData,
                // Tell jQuery not to process data or worry about content-type.
                cache: false,
                contentType: false,
                processData: false,
                success: function () {
                    window.location.reload();
                },
                error: function () {
                    alert('Unknown error updating signature.');
                }
            });
        }
    }

    invertGeneListsTable();
    setupAdminControlsIfNecessary();
});