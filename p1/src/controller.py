import view
import exceptions
import concurrent.futures

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.cocktail_searched = False
        self.current_page = "Home" 

    # Runner
    def run(self, application_id):
        self.view.set_handler(self)
        view.run(application_id=application_id, on_activate=self.view.on_activate)

    # Handler methods
    def on_alcohol_button_clicked(self, widget):
        self.current_page = "Home" 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.getAlcoholList)
            future.add_done_callback(self.handle_alcohol_results)

    def handle_alcohol_results(self, future):
        try:
            data = future.result()
            self.view.l = data
            self.view.update("ALC")
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def on_no_alcohol_button_clicked(self, widget):
        self.current_page = "Home" 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.getNoAlcoholList)
            future.add_done_callback(self.handle_no_alcohol_results)

    def handle_no_alcohol_results(self, future):
        try:
            data = future.result()
            self.view.l = data
            self.view.update("ALC")
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def on_search_button_coc_clicked(self, button, search_coc):
        try:
            if not isinstance(search_coc, str):
                search_text = search_coc.get_text()
            else:
                search_text = str(search_coc)
            if len(search_text) > 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.getCocktailDataP, search_text)
                    future.add_done_callback(self.handle_cocktail_data_results)
                self.current_page = "Cocktail"
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def handle_cocktail_data_results(self, future):
        try:
            data = future.result()
            self.view.set_data(data)
            self.view.update("COC")
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def on_search_button_ing_clicked(self, button, search_ing):
        self.cocktail_searched = True
        try:
            if not isinstance(search_ing, str):
                search_text = search_ing.get_text()
            else:
                search_text = str(search_ing)
            if len(search_text) > 0:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(self.getIngredientDataP, search_text)
                    future.add_done_callback(self.handle_ingredient_data_results)
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def handle_ingredient_data_results(self, future):
        try:
            data = future.result()
            self.view.set_data(data)
            self.view.update("ING")
        except exceptions.NotInternetException:
            self.view.update("ERROR")
        except exceptions.NoResultsException:
            self.view.update("ERROR2")

    def on_home_button_clicked(self, button):
        self.current_page = "Home" 
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.home_button_action)

    def on_back_button_clicked(self, button):
        if self.current_page == "Cocktail":
            cocktail_name = self.view.cocktail_actual['strDrink']
            self.on_search_button_coc_clicked(button, cocktail_name)
        else:
            self.home_button_action()

    def home_button_action(self):
        self.view.update("HOME")

    # Model abstraction
    def getCocktailDataP(self, name):
        lista = self.model.getCocktailData(name)
        if lista is None:
            raise exceptions.NoResultsException
        return lista

    def getIngredientDataP(self, name):
        lista = self.model.getIngredientData(name)
        if lista is None:
            raise exceptions.NoResultsException
        return lista

    def getAlcoholList(self):
        lista = self.model.getListByTag("a")
        if lista is None:
            raise exceptions.NoResultsException
        return lista

    def getNoAlcoholList(self):
        lista = self.model.getListByTag("n")
        if lista is None:
            raise exceptions.NoResultsException
        return lista
