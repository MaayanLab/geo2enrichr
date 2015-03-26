var data = require("sdk/self").data;
var pageMod = require("sdk/page-mod");
var self = require("sdk/self");

pageMod.PageMod({
    include: "http://www.ncbi.nlm.nih.gov/*",
    contentScriptFile: [ self.data.url("jquery-1.11.1.min.js"), self.data.url("jquery-ui.min.js"), self.data.url("g2e.js") ],
    contentStyleFile:  [ self.data.url("main.css"), self.data.url("open-sans.css") ],
    contentScriptWhen: 'end',
    contentScriptOptions: {
        logoUrl: self.data.url("logo-50x50.png")
    }
});
