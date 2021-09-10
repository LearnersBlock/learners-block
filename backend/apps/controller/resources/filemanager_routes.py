from common.system_processes import human_size
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from natsort import os_sorted
from resources.errors import print_message
import json
import os
import shutil


def generate_path(root, path):
    system_root = '/app/storage/'
    return os.path.join(system_root, root, *path)


class filemanager_copy(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        fromPath = generate_path(content['root'], content['fromPath'])
        toPath = generate_path(content['root'], content['toPath'])
        for item in content['object']:
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(toPath, item['name'])
                if os.path.isfile(existingFile):
                    os.remove(existingFile)

                # Copy new item
                shutil.copy2(os.path.join(fromPath, item['name']),
                             os.path.join(toPath))
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(toPath, item['name'])
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

                # Copy new item
                shutil.copytree(os.path.join(fromPath, item['name']),
                                os.path.join(toPath, item['name']))

        return {'message': 'success'}


class filemanager_delete(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        path = generate_path(content['root'], content['path'])

        for item in content['object']:
            if item['format'] == 'file':
                os.remove(os.path.join(path, item['name']))
            elif item['format'] == 'folder':
                shutil.rmtree(os.path.join(path, item['name']))
            else:
                return {'message': 'error, invalid type.'}, 500

        return {'message': 'success'}


class filemanager_file_size(Resource):
    def post(self):
        content = request.get_json()

        path = generate_path(content['root'], content['path'])

        file_size = os.path.getsize(os.path.join(path, content['item']))

        return {'size': human_size(file_size)}


class filemanager_list(Resource):
    def post(self):
        output = []
        content = request.get_json()

        path = generate_path(content['root'], content['path'])

        for direc in os_sorted(next(os.walk(os.path.join(path)))[1]):
            output.append({'name': direc,
                           'format': 'folder'})

        for f in os_sorted(next(os.walk(os.path.join(path)))[2]):
            file_ext = os.path.splitext(f)
            output.append({'name': f,
                           'format': 'file',
                           'extension': file_ext[1]})

        # Return compiled path for use in interface
        if content['path']:
            return_path = os.path.join(content['root'], *content['path'])
        else:
            return_path = content['root']

        return {'rows': output, 'path': return_path}


class filemanager_move(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        fromPath = generate_path(content['root'], content['fromPath'])
        toPath = generate_path(content['root'], content['toPath'])

        for item in content['object']:
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(toPath, item['name'])
                if os.path.isfile(existingFile):
                    os.remove(existingFile)
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(toPath, item['name'])
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

            shutil.move(os.path.join(fromPath, item['name']),
                        os.path.join(toPath))

        return {'message': 'success'}


class filemanager_newfolder(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        path = generate_path(content['root'], content['path'])

        fPath = os.path.join(path, content['directory'])

        os.mkdir(fPath)
        os.chown(fPath, 65534, 65534)

        return {'message': 'success'}


class filemanager_rename(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        path = generate_path(content['root'], content['path'])

        os.rename(os.path.join(path, content['from']),
                  os.path.join(path, content['to']))

        return {'message': 'success'}


class filemanager_unzip(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        path = generate_path(content['root'], content['path'])

        pid = os.fork()

        if pid == 0:
            try:
                os.setuid(65534)
                shutil.unpack_archive(os.path.join(path,
                                                   content['file']),
                                      os.path.join(path))
            except Exception as ex:
                print_message('filemanager_unzip', 'Failed extracting', ex)
        else:
            os.waitpid(pid, 0)
            return {'message': 'finished'}


class filemanager_upload(Resource):
    @jwt_required()
    def post(self):
        path = generate_path(request.headers['rootPath'],
                             json.loads(request.headers['savePath']))

        for fname in request.files:
            f = request.files.get(fname)
            f.save(os.path.join(path, fname))
            os.chown(os.path.join(path, fname), 65534, 65534)

        return {'message': 'success'}
