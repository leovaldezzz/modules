## Modulo expected_data

`expected_data` valida payloads de tipo diccionario a partir de una declaracion de
campos. Ademas de indicar si el payload es valido, captura los valores aceptados
y devuelve errores estructurados.

### Uso basico

```python
from expected_data.expected_data import ExpectedData, Field


validator = ExpectedData({
    "name": Field(
        key="name",
        required=True,
        datatype=str,
        min_length=2,
        max_length=80,
    ),
    "age": Field(
        key="age",
        required=True,
        datatype=int,
    ),
    "role": Field(
        key="role",
        default="user",
        enum=["user", "admin"],
    ),
})

payload = {
    "name": "Ada Lovelace",
    "age": 36,
}

result = validator.validate(payload)

if result["valid"]:
    print(validator.data())
    # {'name': 'Ada Lovelace', 'age': 36, 'role': 'user'}
else:
    print(result["errors"])
```

Los campos que faltan pueden recibir un valor por defecto. Los campos marcados
como `required=True` deben aparecer en el payload. `datatype` acepta un tipo o
una tupla de tipos, por ejemplo `datatype=(int, float)`.

### Errores de validacion

`validate(...)` devuelve un diccionario con `valid` y `errors`. Cada error incluye
el campo, un codigo, un mensaje y los valores esperado y recibido:

```python
invalid_payload = {"name": "A", "age": "treinta", "role": "guest"}
result = validator.validate(invalid_payload)

print(result["valid"])
# False

for error in result["errors"]:
    print(error["field"], error["code"])
# name min_length
# age type
# role enum
```

Tambien puedes obtener el estado completo despues de validar:

```python
print(validator.result())
# {
#     "valid": False,
#     "data": {...},
#     "errors": [...],
# }
```

### Agregar campos despues

`add(...)` permite construir el esquema progresivamente y devuelve el mismo
objeto para encadenar llamadas:

```python
validator = (
    ExpectedData()
    .add(Field("email", required=True, datatype=str))
    .add(Field("newsletter", default=False, datatype=bool))
)
```

Agregar dos veces el mismo campo produce `ValueError`.

### Validacion personalizada

`scanner` puede ser una funcion que reciba el valor y devuelva `True` o `False`:

```python
def is_positive(value):
    return value > 0


validator = ExpectedData({
    "amount": Field(
        "amount",
        required=True,
        datatype=(int, float),
        scanner=is_positive,
    ),
})

result = validator.validate({"amount": 25})
print(result["valid"])
# True
```

Tambien se puede usar `PayloadValidator` como scanner para revisar el contenido
de un valor:

```python
from expected_data.payload_validator import PayloadValidator, SecurityLevel


security_scanner = PayloadValidator(SecurityLevel.SAFE_TEXT)
validator = ExpectedData({
    "comment": Field("comment", scanner=security_scanner),
})

result = validator.validate({"comment": "Texto normal"})
print(result["valid"])
```

### Metodos principales

- `validate(payload)`: valida y devuelve `valid` y `errors`.
- `scan(payload)`: valida y devuelve los datos capturados.
- `data()`: devuelve una copia de los datos capturados.
- `errors()`: devuelve los errores de la ultima validacion.
- `is_valid()`: indica si la ultima validacion no produjo errores.
- `result()`: combina validez, datos y errores.
- `add(field)`: agrega un `Field` al esquema.

La validacion no modifica el diccionario original recibido.
