#STINKY METHOD
from html import escape


def attrs(**kwargs):
    result = []

    for key, value in kwargs.items():
        if value is None or value is False:
            continue

        if value is True:
            result.append(key)
            continue

        # Python pasa a HTML
        key = {
            "class_name": "class",
            "html_for": "for",
            "max_length": "maxlength",
            "default_value": "value",
        }.get(key, key)

        result.append(f'{key}="{escape(str(value), quote=True)}"')

    return " ".join(result)


def field(field):
    name = field.get("name", "")
    label = field.get("label", "")
    widget = field.get("widget", "text")

    common = {
        "name": name,
        "id": name,
        "required": bool(field.get("required")),
    }

    default = field.get("default")

    if default is not None:
        common["value"] = default

    if widget == "text":
        input_attrs = {
            "type": "text",
            "max_length": field.get("max_length"),
            **common,
        }

        return (
            "<div>"
            f'<label for="{escape(name, quote=True)}">{escape(label)}</label>'
            f"<input {attrs(**input_attrs)}>"
            "<br>"
            "</div>"
        )

    elif widget == "date":
        return (
            "<div>"
            f'<label for="{escape(name, quote=True)}">{escape(label)}</label>'
            f'<input {attrs(type="date", **common)}>'
            "<br>"
            "</div>"
        )

    elif widget == "textarea":
        textarea_attrs = {
            **common,
        }

        value = "" if default is None else default

        return (
            "<div>"
            f'<label for="{escape(name, quote=True)}">{escape(label)}</label>'
            f"<textarea {attrs(**textarea_attrs)}>"
            f"{escape(str(value))}"
            "</textarea>"
            "<br>"
            "</div>"
        )

    elif widget == "select":
        options = []

        for index, opt in enumerate(field.get("options", [])):
            if isinstance(opt, dict):
                value = opt.get("value", "")
                option_label = opt.get("label", "")
            else:
                value = opt
                option_label = opt

            selected = (
                default is not None
                and str(value) == str(default)
            )

            option_attrs = {
                "value": value,
                "selected": selected,
            }

            options.append(
                f"<option {attrs(**option_attrs)}>"
                f"{escape(str(option_label))}"
                "</option>"
            )

        return (
            "<div>"
            f'<label for="{escape(name, quote=True)}">{escape(label)}</label>'
            f"<select {attrs(**common)}>"
            f"{''.join(options)}"
            "</select>"
            "<br>"
            "</div>"
        )

    else:
        return (
            "<div>"
            f'<label for="{escape(name, quote=True)}">{escape(label)}</label>'
            f'<input {attrs(type="text", **common)}>'
            "<br>"
            "</div>"
        )


def form(fields):
    rendered_fields = "".join(
        field(f)
        for f in fields
    )

    return (
        '<form id="myform">'
        f"{rendered_fields}"
        '<button id="post">Enviar</button>'
        "</form>"
    )


def render_page(schema, formname=None):
    fields = schema.get("fields", [])

    title = formname or "Formulario dinámico"

    return (
        "<!DOCTYPE html>"
        "<html>"
        "<head>"
        '<meta charset="utf-8">'
        "<title>Postgres Form Generator</title>"
        '<link rel="stylesheet" href="/static/myform.css">'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
        "</head>"
        "<body>"
        f"<h1>{escape(str(title))}</h1>"
        f"{form(fields)}"
        '<script src="/static/myform.js"></script>'
        "</body>"
        "</html>"
    )