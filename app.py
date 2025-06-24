from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate

app = Flask(__name__)

# Instalar modelo EN→ES si no está instalado
def ensure_model_installed():
    installed_languages = argostranslate.translate.get_installed_languages()
    if not any(
        lang.code == "en" and any(t.code == "es" for t in lang.translations)
        for lang in installed_languages
    ):
        try:
            print("🔄 Descargando modelo EN → ES...")
            available_packages = argostranslate.package.get_available_packages()
            for package in available_packages:
                if package.from_code == "en" and package.to_code == "es":
                    path = argostranslate.package.download_package(package)
                    argostranslate.package.install_from_path(path)
                    print("✅ Modelo instalado")
                    break
        except Exception as e:
            print("❌ Error instalando modelo:", e)

@app.route("/")
def home():
    return "✅ Servidor activo y corriendo en Dokploy"

@app.route("/translate", methods=["POST"])
def translate():
    try:
        ensure_model_installed()
        data = request.get_json()

        from_code = data.get("source_language", "en")
        to_code = data.get("target_language", "es")
        text = data.get("text", "")

        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((l for l in installed_languages if l.code == from_code), None)
        to_lang = next((l for l in installed_languages if l.code == to_code), None)

        if not from_lang or not to_lang:
            return jsonify({"error": "Idiomas no soportados"}), 400

        translation = from_lang.get_translation(to_lang)
        translated_text = translation.translate(text)
        return jsonify({"translatedText": translated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
