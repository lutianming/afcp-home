

var isChrome = navigator.userAgent.indexOf('Chrome') != -1;
var isIE = window.ActiveXObject != undefined;

// Add an event, compatible with IE < 9
function addEvent(el, event, func) {
	// Si notre élément possède la méthode addEventListener() (compatibilité
	// avec IE version<9 oblige)
	if (el.addEventListener) {
		el.addEventListener(event, func, false);
	} else { // Si notre élément ne possède pas la méthode addEventListener()
		el.attachEvent('on' + event, func);
	}
}

function hasClass(ele,cls) {
	//if (!ele) return false;
	return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
}
function addClass(ele,cls) {
	//if (ele && !hasClass(ele,cls)) {
		ele.className += " "+cls;
	//}
}
function removeClass(ele,cls) {
	//if (hasClass(ele,cls)) {
		var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
		ele.className=ele.className.replace(reg,' ');
	//}
}
function replaceClass(ele, cls, cls2) {
	var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
	ele.className=ele.className.replace(reg,'$1'+cls2+'$2');
}

var hidden, shown;
//if (isIE) {
//	hidden = "hidden";
//	shown = "";
//	var unwrapped = document.querySelectorAll(".unwrapped");
//	alert(unwrapped.length);
//	for (var i=0; i<unwrapped.length; i++) {
//		//replaceClass(unwrapped[i], "unwrapped", hidden);
//		//removeClass(unwrapped[i], "unwrapped");
//	}
//} else {
	hidden = "wrapped";
	shown = "unwrapped";
//}
function transition(elt, bt) {
	//if (elt.className == "hidden") {
	//alert(elt);
	if (hasClass(elt, hidden)) {
		show(elt, bt);
		//removeClass(elt, hidden);
		//replaceClass(elt, hidden, shown);
	} else {
		hide(elt, bt);
		//addClass(elt, hidden);
		//replaceClass(elt, shown, hidden);
	}
	return false;
}
function show(elt, bt) {
	//elt.className = "";
	//removeClass(elt, hidden);
	if (!isIE) {
//		removeClass(elt, hidden);
//	} else {
		var child, child2;
		var parent = elt;
		while (parent && parent != document) {
			if (parent == elt || hasClass(parent, "unwrapped")) {
				calculateAndSetHeight(parent);
			}
			parent = parent.parentNode;
		}
	}
	replaceClass(elt, hidden, shown);
	//alert(elt.style.height);
//	if (bt)
//		bt.childNodes[0].nodeValue = "Masquer";
}
function getStyle(elt, styleProp)
{
	var y;
	if (window.getComputedStyle) {
		y = document.defaultView.getComputedStyle(elt,null).getPropertyValue(styleProp);
		//alert(elt + " ; " + styleProp + " : " + y);
	} else if (elt.currentStyle) {
		y = elt.currentStyle[styleProp];
	}
	return parseFloat(y);
}
function myNextSibling(elt) {
	while (elt && elt.nodeType != 1 && elt.nextSibling != null) {
		elt = elt.nextSibling;
	}
	return elt;
}
function myPreviousSibling(elt) {
	while (elt && elt.nodeType != 1 && elt.previousSibling != null) {
		elt = elt.previousSibling;
	}
	return elt;
}
function calculateAndSetHeight(elt) {
	// Calcule la taille de l'élément pour l'attribuer explicitement.
	// Nécessite un unique enfant (par exemple un div) englobant tous
	// les autres sous-enfants.
	var child, child2;
	child = myNextSibling(elt.firstChild);
	height = getStyle(child, "height"); //child.offsetHeight;
	child2 = myNextSibling(child.firstChild);
	if (child2) {
		height += getStyle(child2, "margin-top");
//		alert(height);
	}
	child2 = myPreviousSibling(child.lastChild);
	if (child2) {
		height += getStyle(child2, "margin-bottom");
		//alert(child2 + " / " + getStyle(child2, "margin-bottom"));
	}
	elt.style.height = (height)+'px';
}
function hide(elt, bt) {
	replaceClass(elt, shown, hidden);
	if (!isIE) {
//		addClass(elt, hidden);
//	} else {
		var parent = elt.parentNode;
		elt.style.height = "";
		while (parent && parent != document) {
			if (hasClass(parent, "unwrapped")) {
				calculateAndSetHeight(parent);
			}
			parent = parent.parentNode;
		}
	}
}

function getNext (obj) {
	if (!obj || !obj.nextSibling) return obj;
	var next=obj.nextSibling;
	while (next.nodeType!=1 && next.nextSibling != null)
		next=next.nextSibling;
	return next;
}

addEvent(window, 'load', function(e) {
	//var buttons = document.querySelectorAll(".apply-button");
	var buttons = $('.apply-button');
	for (var i=0; i<buttons.length; i++){
		addEvent(buttons[i], 'click', function(e) { 
			e = e || window.event; 
			target = e.srcElement || e.target; 
			while (!hasClass(target, "apply-button") && target.parentNode) {
				target = target.parentNode;
			}
			transition(getNext(target), target); 
		});
		//hide(getNext(elts[i]), elts[i]);
	}
});


// Fichier javascript en bas du fichier html
// Initialisation :

//var elts = document.querySelectorAll(".apply-button");
var elts = $('.apply-button');
for (var i=0; i<elts.length; i++){
	hide(getNext(elts[i]), elts[i]);
}
