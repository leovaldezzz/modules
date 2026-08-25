# Instalación

## Linux (Debian/Ubuntu)

### 1. Instalar Python y `venv`

Si no tienes instalado Python o el módulo `venv`, ejecuta:

```bash
sudo apt update
sudo apt install python3 python3-venv
```

### 2. Crear el entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

```bash
source venv/bin/activate
```

### 4. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 5. Instalar el proyecto

Instala el proyecto en modo editable:

```bash
python -m pip install -e .
```

---

## Windows

### 1. Crear el entorno virtual

Se recomienda utilizar el lanzador de Python:

```powershell
py -m venv venv
```

### 2. Activar el entorno virtual

En PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Instalar el proyecto

```powershell
python -m pip install -e .
```

> **Nota:** Si PowerShell no permite ejecutar `Activate.ps1`, puedes utilizar directamente `venv\Scripts\python.exe` sin activar el entorno virtual.

---

## Comprobar la instalación

Para comprobar que el entorno virtual está activo y que el proyecto se instaló correctamente:

### Linux

```bash
which python
python --version
```

### Windows

```powershell
where python
python --version
```