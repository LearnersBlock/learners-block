import json
import requests
from common.app_store import update_existing_app_status
from common.app_store import update_new_apps
from common.errors import AppStoreFetchFailed
from common.errors import logger
from common.models import App_Store
from flask_jwt_extended import jwt_required
from flask_restful import Resource

app_store_url = ("https://raw.githubusercontent.com/"
                 "LearnersBlock/app-store/main/"
                 "database.json")


class appstore_get_apps(Resource):
    @jwt_required()
    def get(self):
        # Fetch list of available apps from app-store repo
        try:
            app_list = requests.get(app_store_url,
                                    timeout=8).json()

        except Exception:
            logger.exception("Failed fetching app list from Git.")
            raise AppStoreFetchFailed

        update_existing_app_status(app_list)

        update_new_apps(app_list)

        return {'message': 'done'}


class appstore_status(Resource):
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
                        'info': db_entry.info,
                        'dependencies': json.loads(db_entry.dependencies),
                        "version_name": db_entry.version_name,
                        "version": db_entry.version,
                        "author_site": db_entry.author_site,
                        "logo": db_entry.logo,
                        'status': db_entry.status
                    }

            # Combine all the apps into one entry var
            database_entries.append(entry)

        # Return a list of all the database entries
        return database_entries
