from common.errors import logger
from common.docker import docker_py
from common.models import App_Store
import json
import os
import requests
import shutil


# For all the existing apps in the database, handle updates
# and deleted entries
def update_existing_app_status(app_list):
    for db_entry in App_Store.query.all():
        # If the database entry is not in the app-store repo
        if db_entry.name not in app_list:

            # Remove any container dependecies
            if db_entry.dependencies:
                # Fetch dependecies and convert to JSON
                json_dep = json.loads(db_entry.dependencies)

                # Remove the dependency containers and images
                for dependency in json_dep:
                    # Stop and remove the dependency containers
                    docker_py.remove(name=dependency)

                    # Remove related dependency images
                    try:
                        docker_py.prune(image=json_dep
                                        [dependency]
                                        ["image"],
                                        network=db_entry.name)
                    except Exception:
                        logger.exception("Dependency image may already have "
                                         "been pruned.")

            # Remove the main container and image
            docker_py.remove(name=db_entry.name)

            try:
                docker_py.prune(image=db_entry.image,
                                network=db_entry.name)
            except Exception:
                logger.exception("Image may already have been pruned.")

            # If a logo was downloaded then remove it
            if db_entry.logo and os.path.exists(os.path.realpath('.') +
                                                db_entry.logo):
                try:
                    os.remove(os.path.realpath('.') + db_entry.logo)
                except FileNotFoundError:
                    logger.exception("Failed deleting image.")

            # Remove the application entry from local database
            App_Store.query.filter_by(name=db_entry.name).delete()
            App_Store.commit()

        # If the application is installed and there is an update available
        elif db_entry.status.lower() == "installed" and \
                db_entry.version < app_list[db_entry.name]['version']:

            logger.info('Update available for ' + str(db_entry.name))

            # Change the database entry to update_available
            lb_database = App_Store.query.filter_by(name=db_entry.name).first()
            lb_database.status = 'update_available'
            lb_database.save_to_db()

    return True


# For all new entries in app store, add them to the database
def update_new_apps(app_list):
    # For each app in the online app-store repo
    for app in app_list:
        # Set vars
        logo_path = False
        database_logo_path = ''

        # Get the app entry from the database
        lb_database = App_Store.query.filter_by(name=app).first()

        # Check logo entry is present to avoid exceptions
        try:
            logo_path = app_list[app]['logo']
        except Exception:
            pass

        # Fetch logo if this is a new entry
        if logo_path:
            try:
                database_logo_path = '/asset_share/assets/' + \
                                   app + \
                                   '/' + logo_path \
                                   .split('/')[-1]

                r = requests.get(logo_path,
                                 stream=True,
                                 timeout=5)

                if r.status_code == 200:
                    logoFolder = './asset_share/assets/' + app
                    if os.path.exists(logoFolder):
                        shutil.rmtree(logoFolder)

                    os.makedirs(logoFolder)

                    with open('.' + database_logo_path, 'wb') as f:
                        for chunk in r:
                            f.write(chunk)
                else:
                    logger.warning(f"failed fetching image: {r.status_code}")
            except Exception:
                logger.exception("Failed saving image.")

        # Set the object for submitting to database
        app_entry = {'name': app,
                     'long_name': app_list[app]['long_name'],
                     'env_vars': json.dumps(app_list[app]['env_vars']),
                     'image': app_list[app]['image'],
                     'ports': json.dumps(app_list[app]['ports']),
                     'volumes': json.dumps(app_list[app]['volumes']),
                     'info': app_list[app]['info'],
                     'dependencies': json.dumps(app_list[app]['dependencies']),
                     'version_name': app_list[app]['version_name'],
                     'version': app_list[app]['version'],
                     'author_site': app_list[app]['author_site'],
                     'logo': database_logo_path}

        # Add/Update entry in database
        if lb_database is None:
            lb_database = App_Store(**app_entry)
        else:
            for key, value in app_entry.items():
                setattr(lb_database, key, value)

        # Save any changes to the DB
        lb_database.save_to_db()

    return True
