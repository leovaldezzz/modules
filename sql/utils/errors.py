class PgFrameworkError(Exception):
    description = "Unknown framework error"
    def __str__(self):
        return self.description

class MissingConditionError(PgFrameworkError):
    description = "Missing WHERE condition"

class ValueCountMismatchError(PgFrameworkError):
    description = "El número de valores proporcionados no coincide con la cantidad de columnas editables esperadas"

class MissingFieldsError(PgFrameworkError):
    description = "At least one field required"

class MissingWritableFieldsError(PgFrameworkError):
    description = "At least one writable field required"

class MissingValuesError(PgFrameworkError):
    description = "Query values missing"

class MissingRequiredFieldsError(PgFrameworkError):
    description = "Hay columnas no automáticas y no nulas; debe proporcionar valores para insertarlas."
