import os
import google.generativeai as genai

class Ai:

    def __init__(self, **args):
        self.image_path = None
        self.last_response = ""
        self.history = None


    def ai_first_prompt(self):
        def upload_to_gemini(path, mime_type=None):
            """Uploads the given file to Gemini.

            See https://ai.google.dev/gemini-api/docs/prompting_with_media
            """
            file = genai.upload_file(path, mime_type=mime_type)
            print(f"Uploaded file '{file.display_name}' as: {file.uri}")
            return file

        # Create the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="przeczytaj zdjęcie paragonu i uzyskaj z niego nastepujące informacje w formacie json."
                               "Dane MUSZĄ mieć następujące nazwy: 'data_zakupu', 'produkty' i do każdego produktu jego 'nazwa' i 'cena', 'suma_ptu', 'suma_pln'",
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
                        files[ 0 ],
                    ],
                },
            ]
        )

        response = chat_session.send_message("INSERT_INPUT_HERE")
        self.last_response = response.text
        self.history = chat_session.history
        print(response.text)
        return response.text


    # def correction_prompt(self, image_path: str):
    #
    #     def upload_to_gemini(path, mime_type=None):
    #         """Uploads the given file to Gemini.
    #
    #         See https://ai.google.dev/gemini-api/docs/prompting_with_media
    #         """
    #         file = genai.upload_file(path, mime_type=mime_type)
    #         print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    #         return file
    #
    #     # Create the model
    #     generation_config = {
    #         "temperature": 1,
    #         "top_p": 0.95,
    #         "top_k": 40,
    #         "max_output_tokens": 8192,
    #         "response_mime_type": "application/json",
    #     }
    #
    #     model = genai.GenerativeModel(
    #         model_name="gemini-1.5-pro",
    #         generation_config=generation_config,
    #         system_instruction="przeczytaj zdjęcie paragonu i uzyskaj z niego nastepujące informacje w formacie json: data zakupu, wymień wszystkie produkty i ich ceny, suma PTU, SUMA PLN",
    #     )
    #
    #     # TODO Make these files available on the local file system
    #     # You may need to update the file paths
    #     files = [
    #         upload_to_gemini(image_path, mime_type="image/jpeg"),
    #     ]
    #
    #     chat_session = model.start_chat(
    #         history=[
    #             {
    #                 "role": "user",
    #                 "parts": [
    #                     files[ 0 ],
    #                 ],
    #             },
    #             {
    #                 "role": "model",
    #                 "parts": [
    #                     self.last_response
    #                     ],
    #             },
    #         ]
    #     )
    #
    #     response = chat_session.send_message(
    #         "Nie ma wszystkich żądanych informacji z paragonu ze zdjęcia wcześniej. Wygeneruj jeszcze raz cały json.Wygeneruj tylko json.")
    #     self.last_response = response.text
    #
    #     return response.text