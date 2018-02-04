import json
from functools import wraps
from flask import Flask, make_response, redirect, url_for, request, jsonify
from flask import Response
# project configuration wrapper: yaml formatted file
from misc.config import settings as conf
from quiver import quiver
from quiver import unpack_params as unpack
import admix

VERSION = 0.1
app = Flask(__name__)

OK_STATUS = 200
OK_CREATE_STATUS = 201
DEF_ERROR_CODE = 500


def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


@app.route("/")
@add_response_headers(dict(Location="/about"))
def root():

    return redirect(url_for("about"))


@app.route("/version")
@add_response_headers(dict(Location="/version"))
def version():
    version = dict(
        status=OK_STATUS,
        api_name='Apollo',
        version=VERSION,
        license='Apache 2.0'
    )
    return jsonify(version)


@app.route("/about")
@add_response_headers(dict(Location="/about"))
def about():

    about = dict(
        api_name='Apollo',
        version=VERSION,
        author_name='Juan A. Aguilar',
        author_email='juanantonioaguilar@gmail.com',
        project_repository='https://github.com/jasset75/apollo.github',
        documentation='http://jasset75.github.io/apollo',
        license='Apache 2.0'
    )

    return jsonify(about)


@app.errorhandler(404)
def page_not_found(e):

    error_api_404 = dict(
        status=404,
        error_message='Apollo API endpoint not found.',
        api_name='Apollo',
        version=VERSION,
        author='juanantonioaguilar@gmail.com',
        license='Apache 2.0'
    )

    return jsonify(error_api_404)


@app.route('/get-table', methods=['POST'])
@add_response_headers(dict(Location="/get-table"))
def get_table():
    metadata = {}
    try:

        if request.method == 'POST':

            request_json = request.get_json()

            # data fill in
            metadata = unpack.table(request_json)

            # spark call
            metadata['data'] = quiver.get_table(**metadata)

            # return data
            metadata['success'] = True
            metadata['status'] = OK_STATUS

            return jsonify(metadata)

    except Exception as e:

        metadata['status'] = DEF_ERROR_CODE
        metadata['error_message'] = str(e)

        return Response(json.dumps(metadata), status=metadata['status'],
                        mimetype='application/json')


@app.route('/join', methods=['POST'])
@add_response_headers(dict(Location="/join"))
def join():

    metadata = {}
    try:

        if request.method == 'POST':

            request_json = request.get_json()
            # data fill in
            metadata = unpack.join(request_json)
            # spark call
            metadata['data'] = quiver.join(**metadata, format='dict')
            # return data
            metadata['status'] = OK_STATUS
            metadata['success'] = True

            return jsonify(metadata)

    except Exception as e:

        metadata['status'] = DEF_ERROR_CODE
        metadata['error_message'] = str(e)

        return Response(json.dumps(metadata), status=metadata['status'],
                        mimetype='application/json')


@app.route('/union', methods=['POST'])
@add_response_headers(dict(Location="/union"))
def union():

    metadata = {}
    try:

        if request.method == 'POST':

            request_json = request.get_json()
            # data fill in
            metadata = unpack.union(request_json)
            # spark call
            metadata['data'] = quiver.union(**metadata, format='dict')
            # return data
            metadata['success'] = True
            metadata['status'] = OK_STATUS

            return jsonify(metadata)

    except Exception as e:

        metadata['status'] = DEF_ERROR_CODE
        metadata['error_message'] = str(e)

        return Response(json.dumps(metadata), status=metadata['status'],
                        mimetype='application/json')


@app.route('/create-table', methods=['POST'])
@add_response_headers(dict(Location="/create-table"))
def create_table():

    metadata = {}

    try:

        if request.method == 'POST':

            request_json = request.get_json()
            # data fill in
            metadata['keyspace'] = request_json.get('keyspace', None)
            metadata['tablename'] = request_json.get('tablename', None)
            metadata['columns'] = request_json.get('columns', None)
            # spark call
            metadata['data'] = admix.create_table(**metadata)
            # return data
            metadata['success'] = True
            metadata['status'] = OK_CREATE_STATUS

            return Response(json.dumps(metadata), status=metadata['status'],
                            mimetype='application/json')

    except Exception as e:

        metadata['status'] = DEF_ERROR_CODE
        metadata['error_message'] = str(e)

        return Response(json.dumps(metadata), status=metadata['status'],
                        mimetype='application/json')


if __name__ == "__main__":

    app.run(debug=conf.app.debug)
