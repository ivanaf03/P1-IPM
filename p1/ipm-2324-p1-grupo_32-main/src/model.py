import requests
import threading
import exceptions

class Model:
    @staticmethod
    def getCocktailData(nombre_coctel):
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={nombre_coctel}"
        
        def get_data():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data['drinks']:
                        return data['drinks'][0]
                    else:
                        return None
                else:
                    print(f"Error al obtener datos. Código de estado: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error de red: {str(e)}")
                raise exceptions.NotInternetException

        result = []

        def thread_func():
            data = get_data()
            result.append(data)
        
        thread = threading.Thread(target=thread_func)
        thread.start()
        thread.join()
        
        if not result:
            raise exceptions.NotInternetException

        return result[0]

    @staticmethod
    def getIngredientData(nombre_ingrediente):
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?i={nombre_ingrediente}"
        
        def get_data():
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data['ingredients']:
                        return data['ingredients'][0]
                    else:
                        return None
                else:
                    print(f"Error al obtener datos. Código de estado: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error de red: {str(e)}")
                raise exceptions.NotInternetException

        result = []

        def thread_func():
            data = get_data()
            result.append(data)
        
        thread = threading.Thread(target=thread_func)
        thread.start()
        thread.join()
        
        if not result:
            raise exceptions.NotInternetException

        return result[0]

    @staticmethod
    def getListByTag(letra):
        urls = {
            'n': 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic',
            'a': 'https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic'
        }
        
        if letra in urls:
            url = urls[letra]
            
            def get_data():
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    data = response.json()
                    if 'drinks' in data:
                        if letra == "n":
                            return [item['strDrink'] for item in data['drinks']]
                        if letra == "a":
                            return [item['strDrink'] for item in data['drinks']]
                except requests.exceptions.RequestException as e:
                    print(f"Error de red: {str(e)}")
                    raise exceptions.NotInternetException

            result = []

            def thread_func():
                data = get_data()
                result.append(data)

            thread = threading.Thread(target=thread_func)
            thread.start()
            thread.join()

            if not result:
                raise exceptions.NotInternetException

            return result[0]
        else:
            print(f"Error: Letra no válida '{letra}'.")
            return None
