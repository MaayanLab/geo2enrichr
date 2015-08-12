/* The original release of GEO2Enrichr was a single-page application using
 * Backbone. Since then, it has been converted to a static site. In order to
 * not break permanent links to result pages, this script redirects the user
 * appropriately.
 */

if (window.location.hash.indexOf('#results') === 0) {
    var resultsId = window.location.hash.split('/')[1];
    resultsId = typeof resultsId === 'undefined' ? '' : resultsId;
    window.location.replace("/g2e/results/" + resultsId);
}