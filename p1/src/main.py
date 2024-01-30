from model import Model

from view import View
from controller import Controller

if __name__ == "__main__":
    view=View()
    model=Model()
    controller = Controller(model, view)
    controller.run(application_id="CocktailApp")