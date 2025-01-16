import os
import json
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

class Ai:

    def __init__(self, **args):
        self.image_path = None
        self.last_response = ""
        self.history = None

    def ai_recipe_prompt(self) -> list:
        def upload_to_gemini(path, mime_type=None):
            """Uploads the given file to Gemini.

            See https://ai.google.dev/gemini-api/docs/prompting_with_media
            """
            file = genai.upload_file(path, mime_type=mime_type)
            print(f"Uploaded file '{file.display_name}' as: {file.uri}")
            return file

        def format_prompt(text) -> list:
            jo = json.loads(text)
            date = jo["data_zakupu"]
            nazwa_sklepu = jo["nazwa_sklepu"]
            kwota_calkowita = jo["kwota_calkowita"]
            produkty = jo["produkty"]
            text = (f'data_zakupu: {str(jo["data_zakupu"])}\n,\
                            nazwa_sklepu: {jo["nazwa_sklepu"]}\n,\
                            kwota_calkowita: {jo["kwota_calkowita"]},\
                            produkty:\n')
            for p in jo["produkty"]:
                if jo["produkty"].index(p) == len(jo["produkty"]) - 1:
                    text = text + f"{p['nazwa_produktu']}: {p['cena_suma']}"
                else:
                    text = text + f"{p['nazwa_produktu']}: {p['cena_suma']}\n"
            return [text, date, nazwa_sklepu, kwota_calkowita, produkty]

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="przeczytaj zdjęcie paragonu i uzyskaj z niego nastepujące informacje. Całość napisz w "
                               "podanym formacie json zmieniając tylko value, key muszą zostać nie zmienione. Napisz "
                               "tylko json w podanym niżej formacie. "
                               "Jeśli jest informacja w nawiasie, zastosuj się do tej informacji, nie wstawiając jej w odpowiedź. "
                               "Jeśli nie udało się znaleźć informacji, "
                               "napisz 'null'. Dane MUSZĄ mieć następujące nazwy:\n{\n  \"data_zakupu\": "
                               "\"data_zakupu\",\n  \"nazwa_sklepu\": \"nazwa_sklepu\",\n  \"kwota_calkowita\": "
                               "\"kwota_calkowita\",\n  \"produkty\": [\n    {\n      \"nazwa_produktu\": "
                               "\"nazwa_produktu\",\n      \"cena_suma\": \"cena_jednostkowa\",\n      \"ilosc\": "
                               "\"ilosc\"(jeśli ilość nie jest integerem napisz tylko float np. 0.55)\n    }\n  ]\n}",
        )

        # TODO Make these files available on the local file system
        # You may need to update the file paths
        files = [
            upload_to_gemini(self.image_path, mime_type="image/jpeg"),
        ]

        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        files[0],
                    ],
                },
            ]
        )

        response = chat_session.send_message("INSERT_INPUT_HERE")
        self.last_response = response.text
        self.history = chat_session.history
        print(response.text)
        return format_prompt(response.text)
    # RESPONSE.TEXT LOOKS LIKE THIS SHIT
    # {
    #     "data_zakupu": "data_zakupu",
    #     "nazwa_sklepu": "nazwa_sklepu",
    #     "kwota_calkowita": "kwota_calkowita",
    #     "produkty": [
    #         {
    #             "nazwa_produktu": "nazwa_produktu",
    #             "cena_suma": "cena_jednostkowa",
    #             "ilosc": "ilosc"
    #         }
    #     ]
    # }