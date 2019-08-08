
/* This module creates an invisible div that it useful for verifying that
 * GEO2Enrichr is installed.
 */
var Extension = function () {
    var div = document.createElement('div');
    div.setAttribute('id', 'geo2enrichr-extension-installed-div');
    document.getElementsByTagName('body')[0].appendChild(div);
};
