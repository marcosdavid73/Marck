# Marck — Sistema de gestión (repositorio)

Resumen
Este repositorio contiene una aplicación de escritorio en Python/Tkinter para gestionar afiliados, usuarios, caja, alquileres y eventos.

Requisitos
- Python 3.9+ (Tkinter y sqlite3 incluidos en la mayoría de instalaciones).
- Opcional: PlantUML o herramienta online para regenerar PNG a partir de archivos .puml.

Instalación rápida (Linux/Mac/Windows WSL)
1. Crear un entorno virtual:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

2. Instalar dependencias:
   pip install -r requirements.txt

3. Preparar la base de datos (si no existe o si querés regenerarla):
   python db_setup_fixed.py

4. Ejecutar la aplicación:
   python main.py

Nota sobre la base de datos incluida
- El repositorio puede contener `jubilados.db` con datos de ejemplo. Verificá que no tenga datos sensibles antes de compartirlo.
- Si vas a usar la DB incluida, recomiendo ejecutar primero el script `scripts/migrate_usuarios.py` para normalizar columnas/roles.

Documentación entregada (añadida en esta rama)
- CASOS_DE_USO.md — texto con actores y flujos.
- use_cases.puml — diagrama de casos de uso.
- scripts/migrate_usuarios.py — script para añadir columnas faltantes y normalizar roles.
- run_demo.sh — script para levantar demo local (Linux/Mac).

Cómo incorporar los diagramas en tu informe
- he incluido use_cases.puml listo para convertir a PNG con PlantUML (local) o https://plantuml.com/online.

Qué corregí/propongo respecto al código
- Corregir creación de tabla `usuarios` para que incluya `dni` y `contrasena` (o ajustar código para no usarlas).
- Unificar nombres de rol entre UI y lógica (mapear etiquetas de UI a claves internas).
- Añadir requirements.txt y README (este archivo).

Qué haré después de tu OK
- Si autorizás, puedo ejecutar la migración sobre la DB y subir una copia sanitizada.
