import json
import os
import shutil
from common.errors import logger
from common.errors import FileManagerExtractFail
from common.errors import FileManagerInvalidString
from common.processes import human_size
from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from natsort import os_sorted
from pathlib import Path


# System fileshare root
system_root = '/app/storage/'


def generate_path(root, path):
    return os.path.join(system_root,
                        sanitise(string=root),
                        *sanitise(obj=path))


def sanitise(**item):
    if 'string' in item:
        if '../' in item['string'] or item['string'][:1] == '/':
            raise FileManagerInvalidString
        else:
            return item['string']
    elif 'obj' in item:
        for i in item['obj']:
            if '../' in i or i[:1] == '/':
                raise FileManagerInvalidString
        return item['obj']
    else:
        raise FileManagerInvalidString


class filemanager_copy(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        fromPath = generate_path(content['root'], content['fromPath'])
        toPath = generate_path(content['root'], content['toPath'])
        for item in content['object']:
            itemName = sanitise(string=item['name'])
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(toPath, itemName)
                if os.path.isfile(existingFile):
                    os.remove(existingFile)

                # Copy new item
                shutil.copy2(os.path.join(fromPath, itemName),
                             toPath)
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(toPath, itemName)
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

                # Copy new item
                shutil.copytree(os.path.join(fromPath, itemName),
                                os.path.join(toPath, itemName))

        return {'message': 'success'}


class filemanager_delete(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()
        path = generate_path(content['root'], content['path'])

        for item in content['object']:
            itemName = sanitise(string=item['name'])
            if item['format'] == 'file':
                os.remove(os.path.join(path, itemName))
            elif item['format'] == 'folder':
                shutil.rmtree(os.path.join(path, itemName))
            else:
                raise FileManagerInvalidString

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

        # Store path as pathlib POSIX
        p = Path(path)

        # Return compiled path for use in interface
        if content['path']:
            # Use the sanitised path
            p = Path(path)
            return_path = p.relative_to(*p.parts[:3])
        else:
            return_path = p.parts[3]

        return {'rows': output, 'path': str(return_path)}


class filemanager_move(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        fromPath = generate_path(content['root'], content['fromPath'])
        toPath = generate_path(content['root'], content['toPath'])

        for item in content['object']:
            itemName = sanitise(string=item['name'])
            if item['format'] == 'file':
                # Remove existing item
                existingFile = os.path.join(toPath, itemName)
                if os.path.isfile(existingFile):
                    os.remove(existingFile)
            elif item['format'] == 'folder':
                # Remove existing item
                existingFile = os.path.join(toPath, itemName)
                if os.path.isdir(existingFile):
                    shutil.rmtree(existingFile)

            shutil.move(os.path.join(fromPath, itemName),
                        toPath)

        return {'message': 'success'}


class filemanager_newfolder(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Add the directory here before sanitising the pathnames
        content['path'].append(content['directory'])

        path = generate_path(content['root'], content['path'])

        os.mkdir(path)
        os.chown(path, 65534, 65534)

        return {'message': 'success'}


class filemanager_rename(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json()

        # Add the new from and to names here before sanitising the pathnames
        fromPath = content['path'][:]
        fromPath.append(content['from'])

        toPath = content['path'][:]
        toPath.append(content['to'])

        fromItem = generate_path(content['root'], fromPath)
        toItem = generate_path(content['root'], toPath)

        os.rename(fromItem,
                  toItem)

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
            # Inside the Fork
            try:
                os.setuid(65534)

                shutil.unpack_archive(os.path.join(path,
                                                   content['file']),
                                      os.path.join(path, new_path))
            except Exception:
                logger.exception("Failed extracting.")
                os._exit(1)
            os._exit(0)
        else:
            # Outside the Fork, wait for return code
            _, status = os.waitpid(pid, 0)
            if status == 0:
                return {'message': 'done', 'new_path': new_path}
            else:
                raise FileManagerExtractFail


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
