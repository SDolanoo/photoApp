import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])


def ai_prompt(self):
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
        system_instruction="przeczytaj zdjęcie paragonu i uzyskaj z niego nastepujące informacje w formacie json: data zakupu, wymień wszystkie produkty i ich ceny, suma PTU, SUMA PLN",
    )

    # TODO Make these files available on the local file system
    # You may need to update the file paths
    files = [
        upload_to_gemini("image.png", mime_type="image/png"),
    ]

    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    files[ 0 ],
                ],
            },
            {
                "role": "model",
                "parts": [
                    "```json\n{\n  \"data_zakupu\": \"2024-11-09\",\n  \"produkty\": [\n    { \"nazwa\": \"FILET Z KURCZAKA\", \"cena\": 13.82 },\n    { \"nazwa\": \"SEREK TWOJ SMAK\", \"cena\": 3.99 },\n    { \"nazwa\": \"SEREK BIELUCH SMI\", \"cena\": 3.35 },\n    { \"nazwa\": \"SEREK BIELUCH SMI\", \"cena\": 3.35 },\n    { \"nazwa\": \"AWOKADO ZIELONE\", \"cena\": 6.49 },\n    { \"nazwa\": \"ARCHEW LUZ\", \"cena\": 1.71 },\n    { \"nazwa\": \"BANANY LUZ\", \"cena\": 5.68 },\n    { \"nazwa\": \"MUS JABLKOWY DAWT\", \"cena\": 7.99 },\n    { \"nazwa\": \"CUKIER DIAMANT\", \"cena\": 7.29 },\n    { \"nazwa\": \"MIX ORZECHÓW PRAŽ\", \"cena\": 11.39 },\n    { \"nazwa\": \"MAKA MLYNOMAG\", \"cena\": 3.55 },\n    { \"nazwa\": \"MASLO EKSTRA LACI\", \"cena\": 8.75 },\n    { \"nazwa\": \"MASLO EKSTRA LACI\", \"cena\": 8.75 },\n    { \"nazwa\": \"MANGO SZTUKA\", \"cena\": 6.99 },\n    { \"nazwa\": \"SWEETIE LUZ\", \"cena\": 0.76 },\n    { \"nazwa\": \"JAJA AUGUSTYNIAK\", \"cena\": 9.95 },\n    { \"nazwa\": \"OGÓREK DŁUGI SZTU\", \"cena\": 3.49 },\n    { \"nazwa\": \"GALKA MUSZKATOL.\", \"cena\": 1.65 },\n    { \"nazwa\": \"PASTA DR.OETKER\", \"cena\": 7.95 },\n    { \"nazwa\": \"SODA DR OETKER\", \"cena\": 1.25 },\n    { \"nazwa\": \"CYNAMON KAM\", \"cena\": 2.29 },\n    { \"nazwa\": \"ANYZ KAMIS\", \"cena\": 5.19 },\n    { \"nazwa\": \"PROSZEK DR.OET.\", \"cena\": 0.95 },\n    { \"nazwa\": \"NAPÓJ ENERG MONST\", \"cena\": 6.19 },\n    { \"nazwa\": \"NAPÓJ ENERG MONST\", \"cena\": 6.19 }\n  ],\n  \"suma_ptu\": 10.19,\n  \"suma_pln\": 138.96\n}\n```",
                ],
            },
        ]
    )

    response = chat_session.send_message("INSERT_INPUT_HERE")
    chat_session.histor
    print(response.text)