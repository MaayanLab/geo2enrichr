
/* Checks which, if any, dataset page GEO2Enrichr is on.
 */
function Page() {

    var IS_DATASET_PAGE,
        IS_GDS_PAGE,
        path;

    (function findPage() {
        if (window.location.pathname !== '/') {
            path = window.location.pathname.split('/')[1];
            if (path === 'sites') {
                IS_DATASET_PAGE = true;
                IS_GDS_PAGE = true;
            } else if (path === 'geo') {
                IS_DATASET_PAGE = true;
                IS_GDS_PAGE = false;
            } else {
                IS_DATASET_PAGE = false;
            }
        }
    })();

    return {
        isDataset: function() {
            return IS_DATASET_PAGE;
        },
        isGds: function() {
            return IS_GDS_PAGE;
        }
    };
}