$(function() {

    function invertGeneListsTable() {
        var $el = $('.gene-lists'),
            newRows = [];
        $el.find('tr').each(function () {
            $(this).find('th,td').each(function (i, td) {
                if (_.isUndefined(newRows[i])) {
                    newRows[i] = $('<tr></tr>');
                }
                newRows[i].append(this);
            });
        });
        $el.find('tr').remove();
        _.each(newRows, function (tr) {
            $el.append(tr);
        });
    }

    invertGeneListsTable();
});