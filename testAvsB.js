function testAvsB(x) {
	var finalA = x[0].join().replace(/GSM/g,'').split(",");
	var finalB = x[1].join().replace(/GSM/g,'').split(",");

	//---------------------------------
	// End sample/group assignments
	//---------------------------------
	var abform = document.AvsB;
	var selectedQ = abform.testKindAB.selectedIndex;
	var fold = document.AvsB.signifAB_2t;  // default 
	if (selectedQ == 1 || selectedQ == 2) 
		fold = document.AvsB.signifAB_1t; 
	else if (selectedQ == 3 || selectedQ == 4)
		fold = document.AvsB.signifAB_rv; 

	var foldText = fold.options[fold.selectedIndex].text;

	var code = "ttest";
	if(selectedQ == 3)
		code = "vdiff";  // value means
	else if(selectedQ == 4)
		code = "rdiff";  // rank means
	
	if(finalA.length < 2 || finalB.length < 2) {
		alert("Group size(s) too small.\nSelect at least 2 samples for each group.");
		return;
	}

	var operText = "";
	if(selectedQ == 0) {  // t-test two tailed
		operText = "eq";
		foldText = foldText.substr(0,5);
	}
	else if(selectedQ == 1) { // t-test A>B
		operText = "gt";
		foldText = foldText.substr(0,5);
	}
	else if(selectedQ == 2) { // t-test A<B
		operText = "lt";
		foldText = foldText.substr(0,5);
	}
	else {
		var oper = document.AvsB.sideAB;
		operText = oper.options[oper.selectedIndex].text;
		if(operText == 'lower') {
			operText = 'lt';
			foldText = foldText.charAt(0);
		}
		else if(operText == 'higher') {
			operText = 'gt';
			foldText = foldText.charAt(0);
		}
		else if(operText == 'either') {
			operText = 'gtlt';
			foldText = foldText.charAt(0);
		}
	}

	var selection = '';
	
	for (var i=0;i<sample_ids.length;i++){
		if (x[0].indexOf('GSM'+sample_ids[i])>=0){
			selection += '0';
		}
		else if (x[1].indexOf('GSM'+sample_ids[i])>=0){
			selection += '1';
		}
		else{
			selection += 'X';
		}
	}
	
	var url = "/geo/tools/gds_ab.cgi?acc=GDS"+gdsid+"&selection="+selection+"&method="+code+"&oper="+operText+"&pval="+foldText;

	window.open(url, "AvsB");
}

function optionsAB() {
	var abform = document.AvsB;
	var selectedQ = abform.testKindAB.selectedIndex;

	var twoside = selectedQ == 0 ? "": "none";
	var oneside = (selectedQ == 1 || selectedQ == 2) ? "": "none";
	var valrank = (selectedQ == 3 || selectedQ == 4) ? "": "none";
	document.getElementById("signifLabel1").style.display = valrank;
	document.getElementById("signifAB_2t").style.display = twoside;
	document.getElementById("signifAB_1t").style.display = oneside;
	document.getElementById("signifLabel0").style.display = valrank ? "" : "none";
}
