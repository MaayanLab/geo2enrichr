
/* Embeds HTML into the page, depending on context.
 */
function UiEmbedder(events, page, screenScraper, templater) {

    (function embed() {
        var $modalButtonParent = screenScraper.getModalButtonParent();
        if (page.isGds()) {
            embedInGdsPage($modalButtonParent);
        } else {
            var $metadataTableParent = screenScraper.getMetadataTable();
            embedInGsePage($modalButtonParent, $metadataTableParent);
        }
    })();

    function embedInGsePage($modalButtonParent, $metadataTableParent) {
        var $openModalButtonHtml = templater.get('openModalButton', 'gse');
        $modalButtonParent.append($openModalButtonHtml);
        $openModalButtonHtml.click(function() {
            events.fire('openModalBox');
        });

        $metadataTableParent.find('tr').each(function(i, tr) {
            if ($(tr)
                .find('td')
                .first()
                .text()
                .toLowerCase()
                .indexOf('samples') === 0)
            {
                $samples_table = $(tr);
                return false;
            }
        });

        $samples_table
            .find('tr')
            .each(function(i, tr) {
                $(tr).append(templater.get('checkboxes', 'gse'));
            })
            .end()
            .find('table')
            .first()
            .find('tr')
            .first()
            .before(templater.get('thead', 'gse'));
    }

    function embedInGdsPage($modalButtonParent) {
        var $openModalButtonHtml = templater.get('openModalButton', 'gds');
        $modalButtonParent.children().last().after($openModalButtonHtml);
        $openModalButtonHtml.click(function() {
            events.fire('openModalBox');
        });
    }
}