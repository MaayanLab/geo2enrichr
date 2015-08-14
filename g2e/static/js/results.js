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

    invertGeneListsTable();
});