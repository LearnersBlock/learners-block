from common.system_processes import human_size
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from natsort import os_sorted
from resources.errors import print_message
import json
import os
import shutil


def generate_path(path):
    if path:
        path = os.path.join(*path)
    else:
        path = ''
    return path


class filemanager_copy(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']

        fromPath = generate_path(content['fromPath'])
        toPath = generate_path(content['toPath'])
        for item in content['object']:
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(root, toPath, item['name'])
                if os.path.isfile(existingFile):
                    os.remove(existingFile)

                # Copy new item
                shutil.copy2(os.path.join(root, fromPath, item['name']),
                             os.path.join(root, toPath))
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(root, toPath, item['name'])
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

                # Copy new item
                shutil.copytree(os.path.join(root, fromPath, item['name']),
                                os.path.join(root, toPath, item['name']))

        return {'message': 'success'}


class filemanager_delete(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']
        path = os.path.join(root, generate_path(content['path']))

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
        root = content['root']

        path = generate_path(content['path'])

        file_size = os.path.getsize(os.path.join(root, path, content['item']))

        return {'size': human_size(file_size)}


class filemanager_list(Resource):
    def post(self):
        output = []
        content = request.get_json()
        root = content['root']

        path = generate_path(content['path'])

        for direc in os_sorted(next(os.walk(os.path.join(root, path)))[1]):
            output.append({'name': direc,
                           'format': 'folder'})

        for f in os_sorted(next(os.walk(os.path.join(root, path)))[2]):
            file_ext = os.path.splitext(f)
            output.append({'name': f,
                           'format': 'file',
                           'extension': file_ext[1]})

        return {'rows': output, 'path': path}


class filemanager_move(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']

        fromPath = generate_path(content['fromPath'])
        toPath = generate_path(content['toPath'])

        for item in content['object']:
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(root, toPath, item['name'])
                if os.path.isfile(existingFile):
                    os.remove(existingFile)
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(root, toPath, item['name'])
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

            shutil.move(os.path.join(root, fromPath, item['name']),
                        os.path.join(root, toPath))

        return {'message': 'success'}


class filemanager_newfolder(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']

        path = generate_path(content['path'])

        fPath = os.path.join(root, path, content['directory'])

        os.mkdir(fPath)
        os.chown(fPath, 65534, 65534)

        return {'message': 'success'}


class filemanager_rename(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']

        path = generate_path(content['path'])

        os.rename(os.path.join(root, path, content['from']),
                  os.path.join(root, path, content['to']))

        return {'message': 'success'}


class filemanager_unzip(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        root = content['root']

        path = generate_path(content['path'])

        pid = os.fork()

        if pid == 0:
            try:
                os.setuid(65534)
                shutil.unpack_archive(os.path.join(root,
                                                   path,
                                                   content['file']),
                                      os.path.join(root,
                                                   path))
            except Exception as ex:
                print_message('filemanager_unzip', 'Failed extracting', ex)
        else:
            os.waitpid(pid, 0)
            return {'message': 'finished'}


class filemanager_upload(Resource):
    @jwt_required()
    def post(self):
        root = request.headers['rootPath']
        path = generate_path(json.loads(request.headers['savePath']))

        for fname in request.files:
            f = request.files.get(fname)
            f.save(os.path.join(root, path, fname))
            os.chown(os.path.join(root, path, fname), 65534, 65534)

        return {'message': 'success'}
