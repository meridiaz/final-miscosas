# final-miscosas
# Entrega practica

## Datos

* Nombre Meritxell Díaz Coque
* Titulación: Doble grado en GITT+IAA
* Despliegue: http://pichu.pythonanywhere.com/
* Video básico: https://www.youtube.com/watch?v=1afohjud6p4
* Video parte opcional: https://www.youtube.com/watch?v=adkx4QsUTYU
* Cuenta: mdiaz

## Cuenta Admin Site
* meri/miscosas001
##Cuentas usuarios
* maite/miscosas002
* julian/avernoso
##Resumen parte obligatoria
* La primera peculiaridad es que al visualizarse un recurso, este aparecerá iluminado en la barra
de navegación.
* También he incluido en un formulario conjunto la posibilidad de cambiar el tema y tamaño en la página
del usuario.
* Podemos añadir alimentadores a través del formulario de la página principal, o en el caso de que ya se
encuentren en la página web, actualizar sus datos. También se pueden actualizar en el botón elegir de
la página principal y del propio alimentador
* Si en la barra de direcciones pedimos: /?format=xml o /?format=json se visualizará esta página en ese formato
* Los usuarios que ya hayan votado un ítem no puede quitar su voto, tan solo cambiarlo. Por ejemplo,
si se había hecho like y se vuelve a dar like se ignorará el segundo voto, mientras que si se hace dislike se
actualizará dicho voto


##Lista de partes opcionales
* Nombre parte: Inclusión Favicon.ico
* Nombre parte: Registrar usuarios desde mi aplicación, solo hay introducir una vez la contraseña
* Nombre parte: Asociar usuarios logeados a alimentadores elegidos
* Nombre parte: Fotos en los comentarios de tipo ImageField
* Nombre parte: Posibilidad de ver la app en inglés, cambiando las preferencias del navegador
* Nombre parte: Uso de bootstrap, de manera que se puede ver la aplicación en cualquier tipo de pantalla, como por ejemplo desde un dispositivo móvil.
* Nombre parte: Implementación alimentador extra(LastFM) con token autenticación. IMPORTANTE: Se debe incluir
en la carpeta final-miscosas/proyecto/miscosas un fichero con el nombre apikeys.py que contenga una variable
llamada LASTFM_APIKEY, esta será la clave que se utilizará para descargar su documento XML.
* Nombre parte: Todos las páginas se pueden ver en XML y JSON.
* Nombre parte: Devolución de una página de error personalizada junto con un código 404.
