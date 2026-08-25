## Modulo cheap_render

`cheap_render` convierte un esquema sencillo de formulario en HTML. Genera
campos, etiquetas, valores por defecto y opciones, y escapa los valores antes de
insertarlos en el HTML.

### Ejemplo basico

```python
from cheap_render.cheap_render import render_page


schema = {
    "fields": [
        {
            "name": "name",
            "label": "Nombre",
            "widget": "text",
            "required": True,
            "max_length": 80,
        },
        {
            "name": "birth_date",
            "label": "Fecha de nacimiento",
            "widget": "date",
        },
        {
            "name": "bio",
            "label": "Descripcion",
            "widget": "textarea",
            "default": "",
        },
        {
            "name": "role",
            "label": "Rol",
            "widget": "select",
            "options": [
                {"value": "user", "label": "Usuario"},
                {"value": "admin", "label": "Administrador"},
            ],
            "default": "user",
        },
    ]
}

html = render_page(schema, formname="Alta de usuario")
print(html)
```

`render_page(...)` devuelve un documento HTML completo con el titulo, el
formulario y referencias a `/static/myform.css` y `/static/myform.js`.

### Esquema de un campo

Los atributos mas habituales son:

- `name`: nombre e identificador HTML del campo.
- `label`: texto de la etiqueta.
- `widget`: `text`, `date`, `textarea` o `select`.
- `required`: agrega el atributo HTML `required` cuando es verdadero.
- `default`: valor inicial del campo.
- `max_length`: agrega el atributo HTML `maxlength` para campos de texto.
- `options`: opciones disponibles para un campo `select`.

Las opciones de `select` pueden ser simples:

```python
{
    "name": "status",
    "label": "Estado",
    "widget": "select",
    "options": ["pending", "approved", "rejected"],
    "default": "pending",
}
```

O pueden separar el valor enviado y el texto visible:

```python
{
    "value": "approved",
    "label": "Aprobado",
}
```

### Funciones disponibles

Tambien puedes generar partes del formulario directamente:

```python
from cheap_render.cheap_render import attrs, field, form


print(attrs(class_name="control", required=True, value="Ada"))
# class="control" required value="Ada"

html_field = field({
    "name": "email",
    "label": "Correo",
    "widget": "text",
    "required": True,
})

html_form = form([{
    "name": "email",
    "label": "Correo",
    "widget": "text",
}])
```

`attrs(...)` convierte nombres Python habituales como `class_name`, `html_for`,
`max_length` y `default_value` en sus equivalentes HTML. Los valores se escapan
con `html.escape`, por lo que no deben interpolarse manualmente en el resultado.

Si se indica un `widget` desconocido, se genera un `<input type="text">` como
alternativa.
