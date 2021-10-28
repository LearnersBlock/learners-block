from common.errors import logger
from common.docker import docker_py
from common.models import App_Store
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource


class docker_pull(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies, pull those too
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.pull(env_vars=content["dependencies"]
                                      [dependency]["env_vars"],
                                      image=content["dependencies"]
                                      [dependency]["image"],
                                      name=dependency,
                                      ports=content["dependencies"]
                                      [dependency]["ports"],
                                      volumes=content["dependencies"]
                                      [dependency]["volumes"],
                                      network=content["name"],
                                      detach=True)

                logger.info(deps)

        # Pull latest containers and run them
        response = docker_py.pull(env_vars=content["env_vars"],
                                  image=content["image"],
                                  name=content["name"],
                                  ports=content["ports"],
                                  volumes=content["volumes"],
                                  network=content["name"],
                                  detach=True)

        # Fetch database entry based on passed name
        lb_database = App_Store.query.filter_by(
            name=content["name"]).first()

        # Update entry
        lb_database.status = 'installed'
        lb_database.save_to_db()

        return {"message": response}


class docker_remove(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies then remove them
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.remove(name=dependency)
                logger.info(deps)

        # Remove main container
        response = docker_py.remove(name=content["name"])

        # Fetch database entry based on passed name
        lb_database = App_Store.query.filter_by(
            name=content["name"]).first()

        # Update entry
        lb_database.status = 'install'
        lb_database.save_to_db()

        return {"message": response}


class docker_run(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # If there are container dependencies start them
        if content["dependencies"]:
            for dependency in content["dependencies"]:
                deps = docker_py.run(env_vars=content["dependencies"]
                                     [dependency]["env_vars"],
                                     image=content["dependencies"]
                                     [dependency]["image"],
                                     name=dependency,
                                     ports=content["dependencies"]
                                     [dependency]["ports"],
                                     volumes=content["dependencies"]
                                     [dependency]["volumes"],
                                     network=content["name"],
                                     detach=True)

                logger.debug(deps)

        # Run the primary container
        response = docker_py.run(env_vars=content["env_vars"],
                                 image=content["image"],
                                 name=content["name"],
                                 ports=content["ports"],
                                 volumes=content["volumes"],
                                 network=content["name"],
                                 detach=True)

        # Fetch database entry based on passed name
        lb_database = App_Store.query.filter_by(
            name=content["name"]).first()

        # Update entry
        lb_database.status = 'installed'
        lb_database.save_to_db()

        return {"message": response}
