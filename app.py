from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

app = Flask(__name__)

# Descargar modelo EN→ES si no está instalado
def ensure_model():
    installed = argostranslate.translate.get_installed_languages()
    if not any(l.code == "en" and any(t.code == "es" for t in l.translations) for l in installed):
        packages = argostranslate.package.get_available_packages()
        for pkg in packages:
            if pkg.from_code == "en" and pkg.to_code == "es":
                path = argostranslate.package.download_package(pkg)
                argostranslate.package.install_from_path(path)
                print("Modelo EN→ES instalado")
                break

try:
    ensure_model()
except Exception as e:
    print("Error descargando modelo:", e)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    from_code = data.get("source_language", "en")
    to_code = data.get("target_language", "es")
    text = data.get("text", "")

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed_languages if l.code == from_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_code), None)

    if not from_lang or not to_lang:
        return jsonify({"error": "Language not supported"}), 400

    translation = from_lang.get_translation(to_lang)
    translated_text = translation.translate(text)
    return jsonify({"translatedText": translated_text})
