### Semana 1
El trabajo de la primera semana es a base de nuestra aplicación. Primero el archivo "diagrama_iu.pf" nos permite ver las bases de la app con un prototipo muy simple. En base a ello hemos creado dos documentos UML, un diagrama estático y otra dinámico ("diseño_sw_static.md" y "diseño_sw_dynamic.md"). Los diagramas nos permiten ver el flujo entre clases y los elementos que tienen cada una. La lógica de nuestra app se basa en el patrón MVP. En base a los diagramas hemos construído la app en python+gtk. 

##### Funcionamiento de la app (primera semana)
Por el momento disponemos de una app monothread y en fase alpha, con algunos errores como falta de control de accesos concurrentes y falta de control de caídas de conexión . Se arreglarán a lo largod e las próximas semanas. Disponemos de una interfaz prinipal que permite "Buscar cóctel", "Buscar ingrediente", "Ver cócteles con alcohol" y "Ver cócteles sin alcohol". Estos 2 últimos nos llevan a una ventana con una lista de las resspectivas bebidas que maneja la API. "Buscar cóctel" nos lleva a una ventana "Ver cóctel" con una foto del cóctel, su receta y los ingredientes. Ahí también podemos seleccionar un ingrediente y pasamos a la pantalla de "Ver ingrediente". Parte de ellos tiene información y curiosidades acerca del ingrediente. En caso de que la búsqueda no sea efectiva, salta un aviso de error.

### Semana 2 

Esta semana seguimos trabajando en mejorar el codigo, ampliar nuestro concimiento de la libreria GTK asi como implementar las excepciones correspondientes y convertir nuestra aplicacion a multithread (o intentarlo).

Tambien nos hemos adelantado algo de trabajo de la semana que viene informandonos sobre como traducir nuestra app de forma semiautomatica y asi poder implementar varios idiomas.

##### Funcionamiento de la app (segunda semana)


Hemos implementado errores mas variados a la aplicacion (antes teniamos uno generico para todo) : 

- `NotInternetException`
- `NoResultsException`

Estos se pueden encontrar en un nuevo archivo [exceptions.py](/src/exceptions.py), donde guardaremos todas nuetras excepciones.
Tambien hemos solucionado aquellos errores que no permitian un uso correcto de la app, como que la lista de los cocktails no era interactuable.
Por ultimo hemos hecho nuestra aplicacion multithread, lo que ha solucionado los problemas de carga en la aplicacion, asi de paso restructurando el codigo general de la app en una manera mas correcta.

### Semana 3

Esta semana nuestra app puede llegar a más clientes gracias a la internacionalización de ella. Ahora tenemos traducciones hechas en alemán, inglés e italiano, los idiomas de la API. Además hemos hecho las ventanas resizable y añadido una nueva comodidad para el cliente, tal como es el botón de back en los ingredientes, de forma que pueden volver al cóctel en el que se encontraban si acceden al ingrediente desde un cóctel. 

##### Funcionamiento de la app (tercera semana)

Se han implementado los ficheros .po y se compilaron en .mo, de forma que se traducen las palabras que se encuentran en esas líneas al idioma del sistema operativo del cliente, de forma que queda al app por completo pasada a otro idioma.
Se han añadido las líneas necesarias para hacer unas ventanas elásticas, resizables (win.set_resizable(True), self.scrolled_window_recipe = Gtk.ScrolledWindow()...).
Hemos añadido como condiciones cocktail_actual y pagina_anterior para así poder gestionar el botón de back, de forma que pueda volver al cóctel en el que se encontraba si venía de una página anterior de cóctel, sino se volverá a la página principal.
