import json
from flask import Flask, redirect, url_for
from flask import request, jsonify
from quiver import quiver
from quiver import unpack_params as unpack
import admix
from flask import Response


VERSION=0.1
app = Flask(__name__)

OK_STATUS = 200
DEF_ERROR_CODE = 500

@app.route("/")
def root():
  return redirect(url_for("about"))

@app.route("/version")
def version():
  version = dict(
    status=OK_STATUS,
    api_name='Apollo',
    version=VERSION,
    license='Apache 2.0'
  )
  return jsonify(version)

@app.route("/about")
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
  error_api_404 = dict(status=404,error_message='Apollo API endpoint not found.',api_name='Apollo',version=VERSION,author='juanantonioaguilar@gmail.com',license='Apache 2.0')
  return jsonify(error_api_404)

@app.route("/help/aggregate")
def help():
  return 'Apollo v{0}'.format(VERSION)

@app.route('/get-table', methods=['POST'])
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
    metadata['status_code']=DEF_ERROR_CODE
    metadata['error_message']=str(e)
    return Response(json.dumps(metadata), status=metadata['status_code'], mimetype='application/json')


@app.route('/join', methods=['POST'])
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
    metadata['status_code']=DEF_ERROR_CODE
    metadata['error_message']=str(e)
    return Response(json.dumps(metadata), status=metadata['status_code'], mimetype='application/json')

@app.route('/union', methods=['POST'])
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
    metadata['status_code']=DEF_ERROR_CODE
    metadata['error_message']=str(e)
    return Response(json.dumps(metadata), status=metadata['status_code'], mimetype='application/json')

@app.route('/create_table', methods=['POST'])
def create_table():
  metadata = {}
  try:
    if request.method == 'POST':
      request_json = request.get_json()
      # data fill in
      metadata['keyspace'] = request_json.get('keyspace',None)
      metadata['tablename'] = request_json.get('tablename',None)
      metadata['columns'] = request_json.get('columns',None)
      # spark call
      metadata['data'] = admix.create_table(**metadata)
      # return data
      metadata['success'] = True
      metadata['status'] = OK_STATUS
      return jsonify(metadata)
  except Exception as e:
    metadata['status_code']=DEF_ERROR_CODE
    metadata['error_message']=str(e)
    return Response(json.dumps(metadata), status=metadata['status_code'], mimetype='application/json')

if __name__ == "__main__":
  app.run()