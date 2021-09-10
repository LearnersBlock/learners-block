from common.system_processes import human_size
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from natsort import os_sorted
from pathlib import Path
from resources.errors import print_message
import json
import os
import shutil


# System fileshare root
system_root = '/app/storage/'


def generate_path(root, path):
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

        for direc in os_sorted(next(os.walk(path))[1]):
            output.append({'name': direc,
                           'format': 'folder'})

        for f in os_sorted(next(os.walk(path))[2]):
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
                        toPath)

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

        # Generate a safe extraction path to avoid overwriting
        if os.path.exists(os.path.join(path,
                                       Path(content['file']).stem)):
            i = 1
            while True:
                new_path = Path(content['file']).stem + str(i)
                if os.path.exists(os.path.join(path, new_path)):
                    i = i+1
                else:
                    break
        else:
            new_path = Path(content['file']).stem

        pid = os.fork()

        if pid == 0:
            try:
                os.setuid(65534)

                shutil.unpack_archive(os.path.join(path,
                                                   content['file']),
                                      os.path.join(path, new_path))
            except Exception as ex:
                print_message('filemanager_unzip', 'Failed extracting', ex)
                os._exit(1)
            os._exit(0)
        else:
            _, status = os.waitpid(pid, 0)
            if status == 0:
                return {'message': 'done', 'new_path': new_path}
            else:
                return {'message': 'error'}


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
