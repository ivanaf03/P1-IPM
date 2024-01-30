```mermaid
sequenceDiagram
    participant User
    participant View
    participant Controller
    participant Model

    User ->> View: Interactúa con la interfaz de usuario
    User ->> View: Realiza acciones como hacer clic en botones, ingresar texto, etc.

    alt Realizar búsqueda de cóctel
        User ->> View: Ingresa el nombre del cóctel
        User ->> View: Hace clic en el botón de búsqueda
        View ->>Controller: Llama a on_search_button_coc_clicked(button, search_coc)

        opt Proceso en segundo plano (Hilo/Proceso)
            Controller ->>+ Model: Llama a getCocktailData(nombre_coctel)
            Model ->> Model: Realiza la solicitud a la API de cócteles
            Model -->> Controller: Devuelve datos del cóctel
            Controller ->> View: Llama a set_data(data)
        end
        View ->> View: Actualiza la interfaz de usuario con los datos del cóctel
    else Realizar búsqueda de ingredientes
        User ->> View: Ingresa el nombre del ingrediente
        User ->> View: Hace clic en el botón de búsqueda
        View ->> Controller: Llama a on_search_button_ing_clicked(button, search_ing)

        opt Proceso en segundo plano (Hilo/Proceso)
            Controller ->>+ Model: Llama a getIngredientData(nombre_ingrediente)
            Model ->> Model: Realiza la solicitud a la API de ingredientes
            Model -->> Controller: Devuelve datos del ingrediente
            Controller ->> View: Llama a set_data(data)
        end
        View ->> View: Actualiza la interfaz de usuario con los datos del ingrediente
    end

    alt Acción: Botón "Home" presionado
        Controller ->> View: Llama a on_home_button_clicked()
        View ->> Controller: Notifica la acción "Home" presionado
        Controller ->> View: Llama a update(0)
        View ->> Controller: Notifica la acción "update(0)"
    else Ver lista de cócteles alcohólicos
        User ->> View: Hace clic en el botón "Cócteles Alcohólicos"
        View ->> Controller: Llama a on_alcohol_button_clicked(widget)

        opt Proceso en segundo plano (Hilo/Proceso)
            Controller ->>+ Model: Llama a getAlcoholList()
            Model ->> Model: Realiza la solicitud a la API para obtener la lista de cócteles alcohólicos
            Model -->> Controller: Devuelve la lista de cócteles alcohólicos
            Controller ->> View: Llama a set_data(data)
        end
        View ->> View: Actualiza la interfaz de usuario con la lista de cócteles alcohólicos
    end

    User ->> View: Realiza más interacciones con la interfaz de usuario
    User ->> View: Finaliza la aplicación
    User ->> View: Cierra la ventana o finaliza la aplicación
    View ->> Controller: Llama a on_activate(app) para la finalización
    Controller ->> Model: Realiza tareas de limpieza o finalización
    Model -->> Controller: Confirma la finalización

