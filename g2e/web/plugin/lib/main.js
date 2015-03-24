var data = require("sdk/self").data;
var pageMod = require("sdk/page-mod");

pageMod.PageMod({
    include: "http://www.ncbi.nlm.nih.gov/*",
    contentScriptFile: [data.url("jquery-1.11.1.min.js"), data.url("jquery-ui.min.js"), data.url("g2e.js"), data.url("main.css")],
    contentScriptWhen: 'start'
});
