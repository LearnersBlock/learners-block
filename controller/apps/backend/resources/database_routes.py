from common.docker import docker_py
from common.models import User
from common.models import App_Store
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import abort
from flask_restful import Resource
from pkg_resources import packaging
from resources.errors import print_error
import json
import os
import requests


class app_store_set(Resource):
    @jwt_required()
    def get(self):
        try:
            app_list = requests.get(
                                "https://raw.githubusercontent.com/"
                                "LearnersBlock/app-store/main/"
                                "database.json",
                                timeout=8).json()

        except Exception as ex:
            print_error('app_store_set', 'Failed loading app list', ex)
            abort(408, status=408, message='error', error=str(ex))

        for i in App_Store.query.all():
            # Check all entries are present to avoid exception
            try:
                if i.name not in app_list:
                    pass
            except Exception as ex:
                print_error('app_store_set', 'Failed finding app', ex)
                continue

            # Process list
            if i.name not in app_list:
                print('An entry in the local database has been deleted '
                      'online. Removing local entry...')

                App_Store.query.filter_by(name=i.name).delete()

                try:
                    docker_py.remove(name=i.name,
                                     image=i.image)
                except Exception as ex:
                    print_error('app_store_set',
                                'failed docker remove', ex)

                if i.logo and os.path.exists(os.path.realpath('.') +
                                             i.logo):
                    try:
                        os.remove(os.path.realpath('.') + i.logo)
                    except FileNotFoundError as ex:
                        print_error('app_store_set',
                                    'failed deleting image', ex)

                continue

            if i.status.lower() == "installed" and \
                packaging.version.parse(i.version) < \
                packaging.version.parse(app_list
                                        [i.name]['version']):
                print('Update available for ' + str(i.name))

                lb_database = App_Store.query.filter_by(
                            name=i.name).first()
                lb_database.status = 'update_available'
                lb_database.save_to_db()

        for i in app_list:
            lb_database = App_Store.query.filter_by(name=i).first()

            if lb_database is None:
                lb_database = App_Store(name=i,
                                        long_name=app_list[i]
                                        ['long_name'],
                                        image=app_list[i]
                                        ['image'],
                                        ports=json.dumps(app_list
                                                         [i]['ports']),
                                        volumes=json.dumps(app_list[i]
                                                           ['volumes']),
                                        version=app_list[i]
                                        ['version'],
                                        author_site=app_list[i]
                                        ['author_site'],
                                        logo='')

                # Check all entries are present to avoid exception
                try:
                    if app_list[i]['logo']:
                        pass
                except Exception as ex:
                    print_error('app_store_set',
                                'Failed getting logo path', ex)
                    continue

                if app_list[i]['logo']:
                    lb_database.logo = '/lb_share/assets/' + \
                                        lb_database.name + \
                                        '/' + app_list[i]['logo'] \
                                        .split('/')[-1]

                    try:
                        r = requests.get(app_list[i]['logo'],
                                         stream=True,
                                         timeout=5)

                        if r.status_code == 200:
                            try:
                                os.mkdir('./lb_share/assets/' +
                                         lb_database.name)
                            except Exception as ex:
                                print_error('app_store_set',
                                            'failed making required directory',
                                            ex)

                            with open('.' + lb_database.logo, 'wb') as f:
                                for chunk in r:
                                    f.write(chunk)
                        else:
                            print_error('app_store_set',
                                        'failed saving image')
                    except Exception as ex:
                        print_error('app_store_set',
                                    'failed saving image', ex)
            else:
                lb_database.name = i
                lb_database.long_name = app_list[i]['long_name']
                lb_database.image = app_list[i]['image']
                lb_database.ports = json.dumps(app_list
                                               [i]['ports'])
                lb_database.volumes = json.dumps(app_list[i]
                                                 ['volumes'])
                lb_database.version = app_list[i]['version']
                lb_database.author_site = \
                    app_list[i]['author_site']

            lb_database.save_to_db()

        return {'message': 'done'}, 200


class app_store_status(Resource):
    def get(self):
        database_entries = []
        entry = {}

        all_entires = App_Store.query.all()

        for i in all_entires:
            entry = {
                        'name': i.name,
                        'long_name': i.long_name,
                        'image': i.image,
                        "ports": json.loads(i.ports),
                        "volumes": json.loads(i.volumes),
                        "version": i.version,
                        "author_site": i.author_site,
                        "logo": i.logo,
                        'status': i.status
                    }

            database_entries.append(entry)

        return database_entries, 200


class set_ui(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        lb_database = User.query.filter_by(username='lb').first()

        if "files" in content:
            if content["files"].lower() == "true":
                lb_database.files = True
            else:
                lb_database.files = False
        if "library" in content:
            if content["library"].lower() == "true":
                lb_database.library = True
            else:
                lb_database.library = False
        if "website" in content:
            if content["website"].lower() == "true":
                lb_database.website = True
            else:
                lb_database.website = False
        if "start_page" in content:
            lb_database.start_page = content["start_page"]

        lb_database.save_to_db()

        return {'message': 'done'}, 200


class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()

        verified_password = User.verify_password(' ',
                                                 lb_database.password)

        # Check if there is a wifi password set and return boolean
        if lb_database.wifi_password:
            wifi_password = True
        else:
            wifi_password = False

        return {'files': lb_database.files,
                'library': lb_database.library,
                'website': lb_database.website,
                'start_page': lb_database.start_page,
                'default_login_password_set': verified_password,
                'wifi_password_set': wifi_password}, 200


class set_wifi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        lb_database = User.query.filter_by(username='lb').first()
        lb_database.wifi_password = content["wifi_password"]
        lb_database.save_to_db()

        # If in production environment
        if os.environ['FLASK_ENV'].lower() == "production":
            from common.wifi import wifi
            from common.wifi import wifi_connect
            # If connected, restart Wi-Fi-Connect
            connected = wifi().check_connection()

            if not connected:
                try:
                    # Restart wifi-connect
                    wifi_connect().stop()
                    wifi_connect().start(wait=2)
                except Exception as ex:
                    print_error('set_wifi', 'Failed starting wifi-connect', ex)
                    abort(500, status=500,
                          message='Wifi-connect failed to launch',
                          error=str(ex))

        return {'message': 'success'}, 200
