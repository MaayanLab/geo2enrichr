
var GdsScraper = function($metadataTableParent, $modalButtonParent) {

    return {

        getDataset: function() {
            var record_caption = $metadataTableParent.find('.caption').text(),
                re = new RegExp(/(?:GDS|GSE)[0-9]*/);
            return re.exec(record_caption)[0];
        },

        getOrganism: function() {
            return this.getByName('organism');
        },

        getPlatform: function() {
            return this.getByName('platform');
        },

        getSamples: function() {
            var $groupRow = $($modalButtonParent.children().find('tbody td')[0]),
                bkp_not_found = true,
                samplesStr = this.textFromHtml($groupRow),
                samplesArr = samplesStr.split(' '),
                samplesBkpIdx, A_cols, B_cols;

            $.each(samplesArr, function(i, val) {
                if (bkp_not_found && val.substr(val.length-1) !== ',') {
                    samplesBkpIdx = i+1;
                    bkp_not_found = false;
                } else {
                    // WARNING: we're mutating the list while iterating over it. 
                    // This should be okay since we're just trimming the comma.
                    samplesArr[i] = val.replace(',', '');
                }
            });

            return {
                A_cols: samplesArr.slice(0, samplesBkpIdx),
                B_cols: samplesArr.slice(samplesBkpIdx, samplesArr.length)
            };
        },

        getByName: function(name) {
            // 1. Grab the text from the appropriate row
            // 2. Strip out all the whitespace (newlines, tabs, etc.)
            // 3. Split on the semicolon (notice there are two) and return just the code.
            var idx = this.getRowIdxFromName(name);
            var text = $($metadataTableParent.find('tr')[idx]).text();
            // Remove any preceding whitespace.
            return text.split(':')[1].replace(/\s*/, '');
        },

        getRowIdxFromName: function(attrName) {
            var self = this,
                result;
            $metadataTableParent.find('tr').each(function(i, tr) {
                var titleEl = $(tr).find('th')[0],
                    titleText = self.normalizeText($(titleEl).text()),
                    titleName = titleText.split(':')[0];
                if (titleName === attrName) {
                    result = i;
                    return false;
                }
            });
            return result;
        }
    };
};
