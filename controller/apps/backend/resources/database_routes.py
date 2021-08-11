from common.docker import docker_py
from common.models import User
from common.models import App_Store
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import abort
from flask_restful import Resource
from pkg_resources import packaging
from resources.errors import print_message
import json
import os
import requests


class app_store_set(Resource):
    @jwt_required()
    def get(self):
        # Fetch list of available apps from app-store repo
        try:
            app_list = requests.get(
                                "https://raw.githubusercontent.com/"
                                "LearnersBlock/app-store/main/"
                                "database.json",
                                timeout=8).json()

        except Exception as ex:
            print_message('app_store_set', 'Failed loading app list', ex)
            abort(408, status=408, message='error', error=str(ex))

        # For all the current apps in database
        for db_entry in App_Store.query.all():
            # If the database entry is not in the list in app-store repo
            if db_entry.name not in app_list:
                print('An entry in the local database has been deleted '
                      'online. Removing local entry...')

                # Remove any container dependecies
                if db_entry.dependencies:
                    # Fetch dependecies and convert to JSON
                    json_dep = json.loads(db_entry.dependencies)

                    # Remove the dependency containers and images
                    for dependency in json_dep:
                        # Stop and remove the dependency containers
                        deps = docker_py.remove(name=dependency)

                        # Remove related dependency images
                        try:
                            deps = docker_py.prune(image=json_dep
                                                   [dependency]
                                                   ["image"],
                                                   network=db_entry.name)
                        except Exception as ex:
                            print_message('app_store_set',
                                          'Dependency image may already '
                                          'have been pruned',
                                          ex)

                        print_message('app_store_set', deps["response"])

                # Remove the main container and image
                docker_py.remove(name=db_entry.name)
                try:
                    docker_py.prune(image=db_entry.image,
                                    network=db_entry.name)
                except Exception as ex:
                    print_message('app_store_set',
                                  'Image may already have been '
                                  'pruned',
                                  ex)

                # If a logo was downloaded then remove it
                if db_entry.logo and os.path.exists(os.path.realpath('.') +
                                                    db_entry.logo):
                    try:
                        os.remove(os.path.realpath('.') + db_entry.logo)
                    except FileNotFoundError as ex:
                        print_message('app_store_set',
                                      'failed deleting image', ex)

                # Remove the application entry from local database
                App_Store.query.filter_by(name=db_entry.name).delete()
                App_Store.commit()

                # Continue to next entry in loop as remaining steps
                # are not needed
                continue

            # If the application is installed and there is an update available
            if db_entry.status.lower() == "installed" and \
                packaging.version.parse(db_entry.version) < \
                packaging.version.parse(app_list
                                        [db_entry.name]['version']):
                print('Update available for ' + str(db_entry.name))

                # Change the database entry to update_available
                lb_database = App_Store.query.filter_by(
                            name=db_entry.name).first()
                lb_database.status = 'update_available'
                lb_database.save_to_db()

        # For each app in the online in the app-store repo
        for app in app_list:
            # Get the app entry from the database
            lb_database = App_Store.query.filter_by(name=app).first()

            # If it doesn't exist in the database yet, create it
            if lb_database is None:
                lb_database = App_Store(name=app,
                                        long_name=app_list[app]
                                        ['long_name'],
                                        env_vars=json.dumps(app_list[app]
                                                            ['env_vars']),
                                        image=app_list[app]
                                        ['image'],
                                        ports=json.dumps(app_list
                                                         [app]['ports']),
                                        volumes=json.dumps(app_list[app]
                                                           ['volumes']),
                                        dependencies=json.dumps(
                                                        app_list[app]
                                                        ['dependencies']),
                                        version=app_list[app]
                                        ['version'],
                                        author_site=app_list[app]
                                        ['author_site'],
                                        logo='')

                # Check all entries are present to avoid exception
                try:
                    if app_list[app]['logo']:
                        pass
                except Exception as ex:
                    print_message('app_store_set',
                                  'Failed getting logo path', ex)
                    continue

                # Save the logo
                if app_list[app]['logo']:
                    lb_database.logo = '/lb_share/assets/' + \
                                        lb_database.name + \
                                        '/' + app_list[app]['logo'] \
                                        .split('/')[-1]

                    try:
                        r = requests.get(app_list[app]['logo'],
                                         stream=True,
                                         timeout=5)

                        if r.status_code == 200:
                            try:
                                os.makedirs('./lb_share/assets/' +
                                            lb_database.name)
                            except Exception as ex:
                                print_message('app_store_set',
                                              'Could not make required '
                                              'directory',
                                              ex)

                            with open('.' + lb_database.logo, 'wb') as f:
                                for chunk in r:
                                    f.write(chunk)
                        else:
                            print_message('app_store_set',
                                          'failed saving image')
                    except Exception as ex:
                        print_message('app_store_set',
                                      'failed saving image', ex)

            # If it already exists in the database, update the details
            else:
                lb_database.name = app
                lb_database.long_name = app_list[app]['long_name']
                lb_database.env_vars = json.dumps(app_list[app]
                                                  ['env_vars'])
                lb_database.image = app_list[app]['image']
                lb_database.ports = json.dumps(app_list
                                               [app]['ports'])
                lb_database.volumes = json.dumps(app_list[app]
                                                 ['volumes'])
                lb_database.dependencies = json.dumps(
                                                app_list[app]
                                                ['dependencies'])
                lb_database.version = app_list[app]['version']
                lb_database.author_site = \
                    app_list[app]['author_site']

            # Save any changes to the DB
            lb_database.save_to_db()

        return {'message': 'done'}, 200


class app_store_status(Resource):
    def get(self):
        # Set vars
        database_entries = []
        entry = {}

        # Fetch all DB entries
        all_entires = App_Store.query.all()

        # For each entry in the DB
        for db_entry in all_entires:
            # Add all the DB fields to entry var
            entry = {
                        'name': db_entry.name,
                        'long_name': db_entry.long_name,
                        'env_vars': json.loads(db_entry.env_vars),
                        'image': db_entry.image,
                        "ports": json.loads(db_entry.ports),
                        "volumes": json.loads(db_entry.volumes),
                        'dependencies': json.loads(db_entry.dependencies),
                        "version": db_entry.version,
                        "author_site": db_entry.author_site,
                        "logo": db_entry.logo,
                        'status': db_entry.status
                    }

            # Combine all the apps into one entry var
            database_entries.append(entry)

        # Return a list of all the database entries
        return database_entries, 200


class set_ui(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Fetch current settings toggle and field status
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
                    print_message('set_wifi',
                                  'Failed starting wifi-connect',
                                  ex)
                    abort(500, status=500,
                          message='Wifi-connect failed to launch',
                          error=str(ex))

        return {'message': 'success'}, 200
