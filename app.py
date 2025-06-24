from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

# Inicializar Flask
app = Flask(__name__)

# Descargar e instalar modelo EN → ES si no está
def ensure_model():
    installed = argostranslate.translate.get_installed_languages()
    if not any(lang.code == "en" for lang in installed):
        packages = argostranslate.package.get_available_packages()
        for pkg in packages:
            if pkg.from_code == "en" and pkg.to_code == "es":
                path = argostranslate.package.download_package(pkg)
                argostranslate.package.install_from_path(path)

# Descargar modelos al iniciar
ensure_model()

# Endpoint de traducción
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    from_lang_code = data.get("source_language")
    to_lang_code = data.get("target_language")
    text = data.get("text")

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed_languages if l.code == from_lang_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_lang_code), None)

    if not from_lang or not to_lang:
        return jsonify({"error": "Idioma no soportado"}), 400

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(text)
    return jsonify({"translatedText": translated_text})
