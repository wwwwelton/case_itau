import os
from flasgger import Swagger


def get_stage_name():
    return os.getenv("STAGE_NAME")


def get_apispec_path(stage_name):
    if stage_name:
        return f"/{stage_name}/apispec/apispec_1.json"
    else:
        return "/apispec/apispec_1.json"


def get_redirect_path(path):
    stage_name = get_stage_name()
    if stage_name:
        return f"/{stage_name}/{path}/"
    else:
        return path


def make_swagger_config():
    stage_name = get_stage_name()

    swagger_config = Swagger.DEFAULT_CONFIG.copy()
    swagger_config.update(
        {
            "swagger": "2.0",
            "info": {
                "title": "API de busca de livros",
                "description": "Este projeto é uma API que retorna uma lista de livros com base em autores e/ou gêneros de livros.",
                "version": "1.0.0",
                "contact": {
                    "linkedin": "https://www.linkedin.com/in/welton-leite-b3492985/"
                },
                "license": {
                    "name": "GNU General Public License v3.0",
                    "url": "https://www.gnu.org/licenses/gpl-3.0.html",
                },
            },
            "swagger_ui_bundle_js": "//unpkg.com/swagger-ui-dist@3.28.0/swagger-ui-bundle.js",
            "swagger_ui_standalone_preset_js": "//unpkg.com/swagger-ui-dist@3.28.0/swagger-ui-standalone-preset.js",
            "jquery_js": "//unpkg.com/jquery@2.2.4/dist/jquery.min.js",
            "swagger_ui_css": "//unpkg.com/swagger-ui-dist@3.28.0/swagger-ui.css",
            "favicon": "//unpkg.com/swagger-ui-dist@3.28.0/favicon-32x32.png",
        }
    )

    swagger_config["specs"][0]["route"] = get_apispec_path(stage_name)
    if stage_name:
        swagger_config["basePath"] = f"/{stage_name}"

    return swagger_config
