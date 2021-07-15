from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from common.models import User
from common.models import App_Store
import json
import requests


class app_store_set(Resource):
    @jwt_required()
    def get(self):
        try:
            image_list = requests.get("https://raw.githubusercontent.com/"
                                      "LearnersBlock/app-store/main/"
                                      "image_directory.json",
                                      timeout=8)
        except Exception:
            return {'response': 'error'}, 408

        for i in App_Store.query.all():
            try:
                if not image_list.json()[i.name]:
                    print('Entry deleted from database. Removing...')
                    App_Store.query.filter_by(name=i.name).delete()
                    continue

            except Exception:
                App_Store.query.filter_by(name=i.name).delete()
                continue

            try:
                if (image_list.json()[i.name]['version'] > i.version and
                        i.status.lower() == "installed"):
                    print('Update available for ' + str(i.name))
                    lb_database = App_Store.query.filter_by(
                                  name=i.name).first()
                    lb_database.status = 'Update available'
                    lb_database.save_to_db()
            except Exception as ex:
                print(self.__class__.__name__ + " - " + str(ex))
                return {'message': self.__class__.__name__ + " - " +
                        str(ex)}, 500

        try:
            for i in image_list.json():
                lb_database = App_Store.query.filter_by(name=i).first()

                if lb_database is None:
                    lb_database = App_Store(name=i,
                                            long_name=image_list.json()[i]
                                            ['long_name'],
                                            image=image_list.json()[i]
                                            ['image'],
                                            ports=json.dumps(image_list.json()
                                                             [i]['ports']),
                                            volumes=json.dumps(image_list
                                                               .json()[i]
                                                               ['volumes']),
                                            version=image_list.json()[i]
                                            ['version'],
                                            author_site=image_list.json()[i]
                                            ['author_site'])
                else:
                    lb_database.name = i
                    lb_database.long_name = image_list.json()[i]['long_name']
                    lb_database.image = image_list.json()[i]['image']
                    lb_database.ports = json.dumps(image_list.json()
                                                   [i]['ports'])
                    lb_database.volumes = json.dumps(image_list.json()[i]
                                                     ['volumes'])
                    lb_database.version = image_list.json()[i]['version']
                    lb_database.author_site = \
                        image_list.json()[i]['author_site']

                lb_database.save_to_db()
        except Exception as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'message': self.__class__.__name__ + " - " + str(ex)}, 500

        return {'response': 'done'}, 200


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
                        'status': i.status
                    }

            database_entries.append(entry)

        return database_entries, 200


class set_ui(Resource):
    @jwt_required()
    def post(self):
        try:
            lb_database = User.query.filter_by(username='lb').first()
        except Exception as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'response': self.__class__.__name__ + " - " + str(ex)}, 403

        try:
            content = request.get_json()
        except AttributeError as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'response': 'Error: Must pass valid string.'}, 403

        try:
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
        except Exception as ex:
            print(self.__class__.__name__ + " - " + str(ex))
            return {'message': self.__class__.__name__ + " - " + str(ex)}, 500

        return {'response': 'done'}, 200


class settings_ui(Resource):
    def get(self):
        lb_database = User.query.filter_by(username='lb').first()
        return {'files': lb_database.files,
                'library': lb_database.library,
                'website': lb_database.website,
                'start_page': lb_database.start_page}, 200
