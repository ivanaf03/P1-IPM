 Diseño software
<!-- ## Notas para el desarrollo de este documento
En este fichero debeis documentar el diseño software de la práctica.
> :warning: El diseño en un elemento "vivo". No olvideis actualizarlo
> a medida que cambia durante la realización de la práctica.
> :warning: Recordad que el diseño debe separar _vista_ y
> _estado/modelo_.
	 
El lenguaje de modelado es UML y debeis usar Mermaid para incluir los
diagramas dentro de este documento. Por ejemplo:
-->
```mermaid
classDiagram
    class Model {
        +getCocktailData(nombre_coctel: string): object
        +getIngredientData(nombre_ingrediente: string): object
        +getListByTag(letra: string): List<string>
    }

    class Controller {
        -model: Model
        -view: View
        -cocktail_searched: bool

        +on_alcohol_button_clicked(widget: Widget)
        +handle_alcohol_results(future: Future)
        +on_no_alcohol_button_clicked(widget: Widget)
        +handle_no_alcohol_results(future: Future)
        +on_search_button_coc_clicked(button: Button, search_coc: Entry)
        +handle_cocktail_data_results(future: Future)
        +on_search_button_ing_clicked(button: Button, search_ing: Entry)
        +handle_ingredient_data_results(future: Future)
        +on_home_button_clicked(button: Button)
        +on_back_button_clicked(button: Button)
        +getCocktailDataP(name: string): object
        +getIngredientDataP(name: string): object
        +getAlcoholList(): List<string>
        +getNoAlcoholList(): List<string>
    }

    class View {
        -gtkObjects: Any  //Atributo genérico para objetos GTK
        -handler: Controller
        -data: object
        -l: List<string>
        -pagina_anterior: string
        -cocktail_actual: object

        +set_handler(handler: Controller)
        +on_activate(app: Gtk.Application)
        +set_data(data: object)
        +build(app: Gtk.Application)
        +update(num: int)
    }

    class NotInternetException {
    }

    class NoResultsException {
    }

    Controller --> Model
    Controller --> View
    View ..> Controller
    Model ..> NotInternetException
    Controller ..> NotInternetException
    Model ..> NoResultsException
    Controller ..> NoResultsException
```

