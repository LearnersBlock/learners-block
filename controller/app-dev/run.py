from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager  #
from flask_cors import CORS  #
from resources.models import db
from resources.models import migrate
from resources.models import create_default_user
from resources.resources import portainer_start, portainer_stop, \
    portainer_status, system_info, wifi_connection_status, device, \
    health_check, host_config, journal_logs, update, uuid, \
    wifi_forget, wifi_forget_all, wifi_toggle, login, logout, \
    settings_ui, set_password, set_ui, verify_login, hostname  #


def create_app(config):
    # Initalise and configure Flask
    app = Flask(__name__)
    app.config.from_object(config)

    # Setup Flask-JWT-Extended
    cors = CORS(app, supports_credentials=True)
    jwt = JWTManager(app)

    # Import database and migration process
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
        create_default_user()
    api = Api(app)
    return app, api, cors, jwt


app, api, cors, jwt = create_app('config.Development')

# Configure API access points=
if __name__ == '__main__':
    print("Api-v1 - Starting API...")

    # Activate endpoints
    api.add_resource(wifi_connection_status, '/v1/wifi/connectionstatus')
    api.add_resource(device, '/v1/device')
    api.add_resource(health_check, '/')
    api.add_resource(host_config, '/v1/hostconfig/<hostname>')
    api.add_resource(hostname, '/v1/hostname')
    api.add_resource(login, '/v1/login')  #
    api.add_resource(set_password, '/v1/setpassword')  #
    api.add_resource(set_ui, '/v1/setui')  #
    api.add_resource(logout, '/v1/logout')  #
    api.add_resource(verify_login, '/v1/verifylogin')  #
    api.add_resource(settings_ui, '/v1/settingsui')  #
    api.add_resource(journal_logs, '/v1/journallogs')
    api.add_resource(portainer_status, '/v1/portainer/status')
    api.add_resource(portainer_start, '/v1/portainer/start')
    api.add_resource(portainer_stop, '/v1/portainer/stop')
    api.add_resource(update, '/v1/update')
    api.add_resource(uuid, '/v1/uuid')
    api.add_resource(system_info, '/v1/system/info')
    api.add_resource(wifi_forget, '/v1/wifi/forget')
    api.add_resource(wifi_forget_all, '/v1/wifi/forgetall')
    api.add_resource(wifi_toggle, '/v1/wifitoggle')

    # Run app
    app.run(port=9090, host='0.0.0.0', debug=True)
