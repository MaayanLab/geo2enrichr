
/* Embeds HTML into the page, depending on context.
 */
function UiEmbedder(events, page, screenScraper, templater) {

    function embed(platformNotSupported) {
        var $modalButtonParent = screenScraper.getModalButtonParent();
        if (page.isGds()) {
            embedInGdsPage($modalButtonParent, platformNotSupported);
        } else {
            var $metadataTableParent = screenScraper.getMetadataTableParent();
            embedInGsePage($modalButtonParent, $metadataTableParent, platformNotSupported);
        }
    }

    function abort() {
        embed(true);
    }

    function embedInGsePage($modalButtonParent, $metadataTableParent, platformNotSupported) {
        var $openModalButtonHtml;
        if (platformNotSupported) {
            $openModalButtonHtml = templater.get('platformNotSupported');
            $modalButtonParent.append($openModalButtonHtml);
            return;
        } else {
            $openModalButtonHtml = templater.get('openModalButton', 'gse');
            $modalButtonParent.append($openModalButtonHtml);
            $openModalButtonHtml.click(function() {
                events.fire('openModalBox');
            });
        }

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

    function embedInGdsPage($modalButtonParent, platformNotSupported) {
        var $openModalButtonHtml;
        if (platformNotSupported) {
            $openModalButtonHtml = templater.get('platformNotSupported');
            $modalButtonParent.children().last().after($openModalButtonHtml);
        } else {
            $openModalButtonHtml = templater.get('openModalButton', 'gds');
            $modalButtonParent.children().last().after($openModalButtonHtml);
            $openModalButtonHtml.click(function() {
                events.fire('openModalBox');
            });
        }
    }

    return {
        embed: embed,
        abort: abort
    };
}