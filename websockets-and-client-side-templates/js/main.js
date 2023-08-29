let templates = ["notification-template"];
for (let template_name of templates) {
    let source = document.getElementById(template_name).innerHTML;
    let template = Handlebars.compile(source);
    Handlebars.registerPartial(template_name, template);
}

htmx.defineExtension("transform-response", {
    transformResponse : function(text, xhr, elt) {
        let data = JSON.parse(text);
        data["serial"] = `transformed ${data["serial"]}`;
        return JSON.stringify(data);
    }
});

//htmx.logAll()
