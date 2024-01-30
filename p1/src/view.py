import os
import urllib
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import gettext
import locale

lengua, encoding = locale.getdefaultlocale()
try:
    idioma = gettext.translation('mainapp', localedir='locale', languages=[lengua])
except FileNotFoundError as e:
    idioma = gettext.NullTranslations()
_ = idioma.gettext


def run(application_id, on_activate):
    app = Gtk.Application(application_id=None, flags=0)
    app.connect('activate', on_activate)
    app.run(None)


class View:
    def __init__(self):
        self.handler = None
        self.data = {}
        self.l = []

        self.pagina_anterior = "Home"
        self.cocktail_actual = None

    def set_handler(self, handler):
        self.handler = handler

    def on_activate(self, app):
        self.build(app)

    def set_data(self, data):
        self.data = data

    def build(self, app):

        self.window = win = Gtk.ApplicationWindow(application=app)
        win.set_title(_("COCKTAIL APP"))
        win.connect("destroy", Gtk.main_quit)
        win.set_default_size(720, 100)
        # Hacer ventana elástica
        win.set_resizable(True)

        self.notebook = Gtk.Notebook()
        self.notebook.set_show_tabs(False)
        win.add(self.notebook)

        # HOME view
        home_page = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.notebook.append_page(home_page, Gtk.Label(_("Home")))
        home_page.set_margin_top(20)
        home_page.set_margin_start(20)
        home_page.set_margin_end(20)
        home_page.set_margin_bottom(20)

        background_color = Gdk.RGBA(9/255, 10/255, 3/255, 1)
        #win.override_background_color(Gtk.StateFlags.NORMAL, background_color)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        home_page.pack_start(left_box, True, True, 0)

        # AspectFrame para redimensionar la imagen automáticamente

        aspect_frame = Gtk.AspectFrame(xalign=0, yalign=0.5, ratio=0.2, obey_child=True)
        left_box.pack_start(aspect_frame, True, True, 0)

        image = Gtk.Image.new_from_file(os.path.dirname(__file__) + "/Images/home.png")
        aspect_frame.add(image)

        css_provider = Gtk.CssProvider()

        css_data = """
            .resizable-image {
                background-color: white; /* Fondo blanco */
                border: 2px solid white; /* Borde blanco de 2 píxeles */
                border-radius: 10px; /* Borde redondeado de 10 píxeles */
            }
        """
        css_provider.load_from_data(css_data.encode())

        context = Gtk.StyleContext()
        screen = Gdk.Screen.get_default()
        context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        image.get_style_context().add_class("resizable-image")


        titulo = _("WELCOME!")
        hello_label = Gtk.Label()
        hello_label.set_markup(('<span size="xx-large" weight="bold"><big><big><big>' + titulo + '</big></big></big></span>'))
        left_box.pack_start(hello_label, True, True, 0)
        hello_label.set_alignment(0, 1)

        autores = _("Authors")

        authors_label = Gtk.Label()
        authors_label.set_markup(('<span size="xx-large">' + autores +':</span><span size="x-large"><i> Iván-Ivanna-Fernando</i></span>'))
        left_box.pack_start(authors_label, True, True, 0)
        authors_label.set_alignment(0, 1)

        space = Gtk.Label()
        space.set_vexpand(True)
        left_box.pack_start(space, True, True, 0)
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)


        #Color Botones
        css_providerB = Gtk.CssProvider()
        css_dataB = """
                   .colored-button {
                       background-color: #A68A56;
                       color: white;
                    border: none;
                   }
               """
        css_providerB.load_from_data(css_dataB.encode())

        #Color Entradas
        css_providerE = Gtk.CssProvider()
        css_dataE = """
                   .colored-entry {
                       background-color: #654321;
                       color: black;
                   }
               """
        css_providerE.load_from_data(css_dataE.encode())

        home_page.pack_start(right_box, True, True, 0)


        alcohol_button = Gtk.Button()
        label = Gtk.Label()
        label.set_markup(_("<b><big>Alcoholic</big></b>"))
        alcohol_button.add(label)
        context = alcohol_button.get_style_context()
        context.add_provider(css_providerB, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        alcohol_button.get_style_context().add_class("colored-button")
        alcohol_button.connect("clicked", self.handler.on_alcohol_button_clicked)
        right_box.pack_start(alcohol_button, True, True, 0)


        no_alcohol_button = Gtk.Button()
        label = Gtk.Label()
        label.set_markup(_("<b><big>Non-alcoholic</big></b>"))
        no_alcohol_button.add(label)
        context = no_alcohol_button.get_style_context()
        context.add_provider(css_providerB, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        no_alcohol_button.get_style_context().add_class("colored-button")
        no_alcohol_button.connect("clicked", self.handler.on_no_alcohol_button_clicked)
        right_box.pack_start(no_alcohol_button, True, True, 0)

        space = Gtk.Label()
        space.set_vexpand(True)
        right_box.pack_start(space, True, True, 0)
        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        right_box.pack_start(search_box, False, False, 0)
        space = Gtk.Label()
        space.set_vexpand(True)
        search_box.pack_start(space, True, True, 0)
        self.search_coc = Gtk.Entry()
        self.search_coc.set_placeholder_text(_("Search cocktails..."))
        context = self.search_coc.get_style_context()
        context.add_provider(css_providerE, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.search_coc.get_style_context().add_class("colored-entry")

        search_box.pack_start(self.search_coc, False, False, 0)

        search_coc_button = Gtk.Button(label=_("SEARCH"))
        context = search_coc_button.get_style_context()
        context.add_provider(css_providerB, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        search_coc_button.get_style_context().add_class("colored-button")
        search_coc_button.set_valign(Gtk.Align.CENTER)
        search_box.pack_start(search_coc_button, False, False, 0)
        search_coc_button.connect("clicked", self.handler.on_search_button_coc_clicked, self.search_coc)

        self.search_ing = Gtk.Entry()
        self.search_ing.set_placeholder_text(_("Search ingredients..."))
        context = self.search_ing.get_style_context()
        context.add_provider(css_providerE, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.search_ing.get_style_context().add_class("colored-entry")

        search_box.pack_start(self.search_ing, False, False, 0)
        search_ing_button = Gtk.Button(label=_("SEARCH"))
        search_ing_button.set_valign(Gtk.Align.CENTER)
        context = search_ing_button.get_style_context()
        context.add_provider(css_providerB, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        search_ing_button.get_style_context().add_class("colored-button")
        search_box.pack_start(search_ing_button, False, False, 0)
        search_ing_button.connect("clicked", self.handler.on_search_button_ing_clicked, self.search_ing)

        space = Gtk.Label()
        space.set_vexpand(True)
        search_box.pack_start(space, True, True, 0)
        space = Gtk.Label()
        space.set_vexpand(True)
        right_box.pack_start(space, True, True, 0)

        # Error view not connection
        error_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.notebook.append_page(error_page, Gtk.Label(_("Error")))

        error_image = Gtk.Image()
        error_image.set_from_file(os.path.dirname(__file__) + "/Images/x.jpg")
        image_frame = Gtk.AspectFrame(xalign=0.5, yalign=0.5, ratio=1.0, obey_child=False)
        image_frame.add(error_image)
        error_page.pack_start(image_frame, True, True, 0)

        error_label = Gtk.Label()
        error_label.set_markup("<big><b>" + _("ERROR") + "</b></big>")
        error_page.pack_start(error_label, True, True, 0)

        mensaje_error = Gtk.Label()
        mensaje_error.set_text(_("Please try checking your connection. :("))
        error_page.pack_start(mensaje_error, True, True, 0)

        error_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        error_page.pack_start(error_box2, True, True, 0)

        space = Gtk.Label()
        error_box2.pack_start(space, True, True, 0)

        home_button = Gtk.Button(label=_("HOME"))
        home_button.connect("clicked", self.handler.on_home_button_clicked)
        error_box2.pack_start(home_button, True, True, 0)

        space = Gtk.Label()
        error_box2.pack_start(space, True, True, 0)

        # Cocktail detail view
        cocktail_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.notebook.append_page(cocktail_page, Gtk.Label(_("Cocktail")))
        self.pagina_anterior = "Cocktail"
        self.cocktail_name_label = Gtk.Label()
        cocktail_page.pack_start(self.cocktail_name_label, False, False, 10)

        # ventana redimensionable
        self.scrolled_window_recipe = Gtk.ScrolledWindow()
        self.scrolled_window_recipe.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        cocktail_page.pack_start(self.scrolled_window_recipe, True, True, 10)

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        cocktail_page.pack_start(horizontal_box, True, True, 0)

        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        horizontal_box.pack_start(left_box, False, False, 10)
        self.right_boxi = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        horizontal_box.pack_start(self.right_boxi, False, False, 10)
        self.pixbuf = None
        self.image = Gtk.Image.new_from_pixbuf(self.pixbuf)
        left_box.pack_start(self.image, False, False, 10)
        self.recipe_label = Gtk.Label()
        self.recipe_label.set_line_wrap(True)
        self.scrolled_window_recipe.add(self.recipe_label)
        # Botones resizable
        self.ingredient_buttons = []
        for i in range(1, 16):
            self.ibutton = Gtk.Button(".")
            self.ingredient_buttons.append(self.ibutton)
            # expansión horizontal y vertical de los botones
            self.ibutton.set_hexpand(True)
            self.ibutton.set_vexpand(True)
            self.ibutton.set_valign(Gtk.Align.START)  # espacio entre botones
            self.right_boxi.pack_start(self.ibutton, False, False, 2)
            i + 1
        home_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        left_box.pack_start(home_box, False, False, 10)
        space = Gtk.Label()
        home_box.pack_start(space, True, True, 0)
        home_button = Gtk.Button(label=_("HOME"))
        home_button.connect("clicked", self.handler.on_home_button_clicked)
        home_button.set_size_request(80, 30)
        home_box.pack_start(home_button, True, True, 0)
        space = Gtk.Label()
        home_box.pack_start(space, True, True, 0)

        # Ingredient detail view
        ingredient_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.notebook.append_page(ingredient_page, Gtk.Label(_("Ingredient")))
        self.ing_name_label = Gtk.Label()

        # ventana redimensionable
        self.scrolled_window_ingredient = Gtk.ScrolledWindow()
        self.scrolled_window_ingredient.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        ingredient_page.pack_start(self.scrolled_window_ingredient, True, True, 10)

        ingredient_page.pack_start(self.ing_name_label, False, False, 10)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        ingredient_page.pack_start(self.scrolled_window, True, True, 10)
        self.description_label = Gtk.Label()
        self.scrolled_window.add(self.description_label)

        under_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        ingredient_page.pack_start(under_box, False, False, 10)
        space = Gtk.Label()
        under_box.pack_start(space, True, True, 0)

        home_button = Gtk.Button(label=_("HOME"))
        home_button.connect("clicked", self.handler.on_home_button_clicked)
        home_button.set_size_request(80, 30)
        under_box.pack_start(home_button, True, True, 0)
        space = Gtk.Label()
        under_box.pack_start(space, True, True, 0)
        self.ingredient_back_button = Gtk.Button(label="<=")
        under_box.pack_start(self.ingredient_back_button, True, True, 0)
        self.ingredient_back_button.connect("clicked", self.handler.on_back_button_clicked)
        space = Gtk.Label()
        under_box.pack_start(space, True, True, 0)

        # Alcoholic list view
        alcohol_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.notebook.append_page(alcohol_page, Gtk.Label(_("Alcoholic")))

        # ventana redimensionable
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        alcohol_page.pack_start(self.scrolled_window, True, True, 10)

        self.list = Gtk.ListBox()
        self.scrolled_window.add(self.list)
        self.coc_buttons = []

        for i in range(100):
            self.coc_button = Gtk.Button()
            self.coc_button.set_relief(Gtk.ReliefStyle.NONE)
            self.list.add(self.coc_button)
            self.coc_buttons.append(self.coc_button)
            i + 1

        under_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        alcohol_page.pack_start(under_box, False, False, 10)
        space = Gtk.Label()
        under_box.pack_start(space, True, True, 0)
        home_button = Gtk.Button(label=_("HOME"))
        home_button.connect("clicked", self.handler.on_home_button_clicked)
        home_button.set_size_request(80, 30)
        under_box.pack_start(home_button, True, True, 0)
        space = Gtk.Label()
        under_box.pack_start(space, True, True, 0)

        # Error view not search
        error_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.notebook.append_page(error_page, Gtk.Label(_("Error")))

        # Ventana redimensionable
        error_image = Gtk.Image()
        error_image.set_from_file(os.path.dirname(__file__) + "/Images/x.jpg")
        error_page.pack_start(error_image, True, True, 0)
        error_label = Gtk.Label()
        error_label.set_markup("<big><b>" + _("ERROR") + "</b></big>")
        error_page.pack_start(error_label, True, True, 0)
        mensaje_error = Gtk.Label()
        mensaje_error.set_text(_("Sorry, your search isn't in our database. :("))
        error_page.pack_start(mensaje_error, True, True, 0)

        error_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        error_page.pack_start(error_box2, True, True, 0)
        space = Gtk.Label()
        error_box2.pack_start(space, True, True, 0)
        home_button = Gtk.Button(label=_("HOME"))
        home_button.connect("clicked", self.handler.on_home_button_clicked)
        error_box2.pack_start(home_button, True, True, 0)
        space = Gtk.Label()
        error_box2.pack_start(space, True, True, 0)

        win.show_all()

    def update(self, num):
        if num == "ERROR":
            Gtk.main_iteration_do(False)
            self.pagina_anterior = "Home"
            self.notebook.set_current_page(1)
        elif num == "COC":
            Gdk.threads_enter()
            self.cocktail_actual = self.data
            self.pagina_anterior = "Home"
            self.cocktail_name_label.set_markup(f"<big><b>{self.data['strDrink']}</b></big>")
            imagen_url = self.data.get("strDrinkThumb")
            if imagen_url:
                response = urllib.request.urlopen(imagen_url)
                data = response.read()
                loader = GdkPixbuf.PixbufLoader.new_with_type('jpeg')
                loader.write(data)
                loader.close()
                self.pixbuf = loader.get_pixbuf()
                self.image.set_from_pixbuf(self.pixbuf)

                css_provider = Gtk.CssProvider()

                css_data = """
                            .resizable-image {
                                box-shadow: 0px 0px 0px 2px white; /* Crea una sombra como borde blanco de 2 píxeles */
                                border-radius: 10px; /* Borde redondeado de 10 píxeles */
                            }
                        """
                css_provider.load_from_data(css_data.encode())

                context = Gtk.StyleContext()
                screen = Gdk.Screen.get_default()
                context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

                self.image.get_style_context().add_class("resizable-image")

            if lengua == 'de_DE':
                recipe = self.data.get("strInstructionsDE")
            elif lengua == 'it_IT':
                recipe = self.data.get("strInstructionsIT")
            else:
                recipe = self.data.get("strInstructions")

            if recipe:
                self.scrolled_window_recipe.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
                self.recipe_label.set_text(recipe)
            ingredients = [self.data.get(f'strIngredient{i}') for i in range(1, 16)]
            for i, self.ibutton in enumerate(self.ingredient_buttons):
                ingredient = ingredients[i]
                if ingredient:
                    self.ibutton.connect("clicked", self.handler.on_search_button_ing_clicked, ingredient)
                    self.ibutton.set_label(ingredient)
                    self.ibutton.show()
                else:
                    self.ibutton.hide()
            Gdk.threads_leave()
            self.notebook.set_current_page(2)
        elif num == "ING":
            Gdk.threads_enter()
            self.pagina_anterior = "Cocktail"
            self.ing_name_label.set_markup(f"<big><b>{self.data['strIngredient']}</b></big>")
            if lengua == 'de_DE':
                description = self.data.get("strDescriptionDE")
            elif lengua == 'it_IT':
                description = self.data.get("strDescriptionIT")
            else:
                description = self.data.get("strDescription")
            if description:
                self.description_label.set_text(description)
                self.description_label.set_line_wrap(True)
            else:
                self.description_label.set_text("")
                self.description_label.set_line_wrap(True)
            Gdk.threads_leave()
            self.notebook.set_current_page(3)
        elif num == "ALC":
            Gdk.threads_enter()
            self.pagina_anterior = "Home"
            for i, cocktail in enumerate(self.l):
                self.coc_buttons[i].set_label(cocktail)
                self.coc_buttons[i].connect("clicked", self.handler.on_search_button_coc_clicked, cocktail)
            Gdk.threads_leave()
            self.notebook.set_current_page(4)
        elif num == "ERROR2":
            Gtk.main_iteration_do(False)
            self.pagina_anterior = "Home"
            self.notebook.set_current_page(5)
        else:
            Gdk.threads_enter()
            self.pagina_anterior = "Home"
            self.notebook.set_current_page(0)
            Gdk.threads_leave()
