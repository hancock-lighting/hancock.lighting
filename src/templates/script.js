;(function() {
	var query = decodeURIComponent(document.location.search.slice(1));
	var bodyClasses = document.body.className;
	if (bodyClasses != "") {
		bodyClasses += " ";
	}
	if (query === "") {
		bodyClasses += "{{ classes|join(" ") }}";
	} else {
		bodyClasses += query;
	}
	document.body.className = bodyClasses;
})()