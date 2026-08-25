## Uso del modulo SQL

Este modulo permite conectarse a PostgreSQL y construir consultas con objetos
Python. El flujo habitual es:

1. Crear un objeto `Sql`, que administra un pool de conexiones.
2. Crear un `Table` asociado a ese objeto.
3. Obtener las columnas mediante `table.column["nombre"]`.
4. Construir una operacion, agregar condiciones y ejecutarla.
5. Cerrar el pool al terminar.

### Instalacion y conexion

Instala la dependencia desde la raiz del proyecto:

```bash
pip install -r requirements.txt
```

Configura la conexion de PostgreSQL mediante variables de entorno:

```bash
export DB_NAME=mi_base
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

Tambien puedes proporcionar valores directamente a `Sql(...)`:

```python
db = Sql(
	dbname="base_de_prueba",
	user="postgres",
	password="contrasena_ficticia",
	host="localhost",
	port=5432,
)
```

### Ejemplo paso a paso

El siguiente ejemplo supone que existe una tabla `users` con las columnas
`id`, `name`, `email` y `active`:

```python
from sql.sql_objects.table import Table
from sql.utils.sql import Sql


db = Sql()
users = Table(db, "users")

try:
	# Las columnas se obtienen del esquema real de PostgreSQL.
	name = users.column["name"]
	email = users.column["email"]
	active = users.column["active"]

	# SELECT con filtro, orden y limite.
	rows = (
		users.select(name, email)
		.where(active == True)
		.order_by(name.asc())
		.limit(10)
		.execute(fetchall=True)
	)
	print(rows)

	# INSERT con un diccionario. Los valores se validan contra el esquema.
	users.insert().values({
		"name": "Ada Lovelace",
		"email": "ada@example.com",
	}).execute()

	# UPDATE: siempre debe incluir una condicion WHERE.
	(
		users.update(active)
		.values(False)
		.where(email == "ada@example.com")
		.execute()
	)

	# DELETE: tambien requiere una condicion WHERE.
	users.delete().where(email == "ada@example.com").execute()
finally:
	db.close()
```

El modulo usa consultas parametrizadas. Por ejemplo, la consulta anterior se
puede inspeccionar antes de ejecutarla:

```python
query = users.select(name, email).where(email == "ada@example.com")

print(query.sql())
# SELECT name, email FROM users WHERE email = %s

print(query.params())
# ("ada@example.com",)
```

### Crear una tabla

Si la tabla aun no existe, puedes crearla con `Table.create(...)`:

```python
users.create(
	columns={
		"id": "BIGSERIAL PRIMARY KEY",
		"name": "VARCHAR(100) NOT NULL",
		"email": "VARCHAR(255) NOT NULL UNIQUE",
		"active": "BOOLEAN NOT NULL DEFAULT TRUE",
	},
	if_not_exists=True,
)
```

Despues de crearla, `Table` puede consultar su esquema y resolver sus columnas.
Para borrar la tabla mediante el objeto `Sql`:

```python

```

### Consultas directas

Para casos que no necesitan el constructor de consultas, `Sql` tambien ofrece
metodos directos. Usa `%s` como placeholder y pasa los valores por separado:

```python
row = db.fetchone(
	"SELECT id, name FROM users WHERE email = %s",
	("ada@example.com",),
)

total = db.scalar("SELECT COUNT(*) AS total FROM users")
print(row, total)
```

Los metodos disponibles son `fetchone`, `fetchall`, `scalar`, `exists` y
`execute`. Las operaciones de escritura hacen commit automaticamente. Para
agrupar varias operaciones en una transaccion:

```python
with db.transaction() as connection:
	with connection.cursor() as cursor:
		cursor.execute(
			"UPDATE users SET active = %s WHERE email = %s",
			(False, "ada@example.com"),
		)
```
