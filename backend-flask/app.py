from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
import os
import json
import time
import urllib.request
from jose import jwk, jwt
from jose.utils import base64url_decode
import requests
import json
import sys

from services.home_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.notifications_activities import *
from services.users_short import *
from services.update_profile import * 


# Cloudwatch logs-----------
import watchtower
import logging
from time import strftime

# Configuring Logger to use Cloudwatch
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
LOGGER.addHandler(console_handler)
LOGGER.addHandler(cw_handler)
LOGGER.info("App Test Log")

# Honeycomb------------------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Honeycomb---------------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Rollbar ------
from time import strftime
import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

# AWS X-RAY--------------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
patch_all()

from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask',dynamic_naming=xray_url)

app = Flask(__name__)
app.secret_key = 'kvsvk'


XRayMiddleware(app,xray_recorder)

# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
client_id = os.getenv('GOOGLE_CLIENT_ID')
origins = [frontend, backend,client_id]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": "*"}},
  supports_credentials=True,
  expose_headers="Authorization",
  methods="OPTIONS,GET,HEAD,POST"
)

region = os.environ.get('AWS_DEFAULT_REGION')
user_pool_id = os.environ.get('USER_POOL_ID')
app_client_id = os.environ.get('APP_CLIENT_ID')
# cognito_user_id='EMPTY'

# @app.before_request
def verify_jwt_token():
    app.logger.debug("verifying jwt started")
    auth_header = request.headers.get("Authorization")
    app.logger.debug(auth_header)
    cognito_user_id='na'
    if auth_header is None or auth_header == 'Bearer null':
      # Authorization header is missing
      app.logger.debug("No header in Auth Token")
      return False, None
    else:
      app.logger.debug('enetered')
      token = auth_header.split(' ')[1]
      iss = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'
      aud = app_client_id

      # Retrieve the JSON Web Key Set (JWKS) from the Cognito User Pool
      keys_url = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}/.well-known/jwks.json'
      with urllib.request.urlopen(keys_url) as f:
        response = f.read()
      keys = json.loads(response.decode('utf-8'))['keys']

      headers = jwt.get_unverified_headers(token)
      kid = headers['kid']
      # search for the kid in the downloaded public keys
      key_index = -1
      for i in range(len(keys)):
          if kid == keys[i]['kid']:
              key_index = i
              break
      if key_index == -1:
          print('Public key not found in jwks.json')
          return False, None
      # construct the public key
      public_key = jwk.construct(keys[key_index])
      # get the last two sections of the token,
      # message and signature (encoded in base64)
      message, encoded_signature = str(token).rsplit('.', 1)
      
      decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
      # verify the signature
      if not public_key.verify(message.encode("utf8"), decoded_signature):
          app.logger.debug('Signature verification failed')
          return False, None
      print('Signature successfully verified')
      # since we passed the verification, we can now safely
      # use the unverified claims
      claims = jwt.get_unverified_claims(token)
      app.logger.debug(claims)
      cognito_user_id = claims['sub']
      # additionally we can verify the token expiration
      if time.time() > claims['exp']:
          app.logger.debug('Token is expired')
          return False, None
      # and the Audience  (use claims['client_id'] if verifying an access token)
      if claims['client_id'] != app_client_id:
          app.logger.debug('Token was not issued for this audience')
          return False, None
      # now we can use the claims
      app.logger.debug(claims)
    return True, cognito_user_id

# Rollbar ----------
rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token
        rollbar_access_token,
        # environment name
        'production',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)

# @app.route('/rollbar/test')
# def rollbar_test():
#   rollbar.report_message('Hello World','warning')
#   return "Hello world"

@app.route('/api/health-check')
def health_check():
  return {'success': True}, 200

@app.route("/api/activities/home", methods=['GET'])
def data_home():

  session['is_auth'],_ = verify_jwt_token()
  is_auth = session.get('is_auth', False)
  app.logger.debug("What is status:- ")
  app.logger.debug(is_auth)
  if is_auth:
    app.logger.info('******Authenticated********')
    data = HomeActivities.run(logger=LOGGER) 
    return data, 200
  else: 
    app.logger.info('******NOT Authenticated********')
    data = HomeActivities.run(logger=LOGGER) 
    return data, 200

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
  
  session['is_auth'], cognito_user_id = verify_jwt_token()
  is_auth = session.get('is_auth', False)
  app.logger.debug(is_auth)

  if is_auth:
    app.logger.info('******Authenticated********')
    app.logger.debug(cognito_user_id)
    model = MessageGroups.run(cognito_user_id=cognito_user_id)
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  else:
    app.logger.info('******NOT Authenticated********')
    return jsonify({"Authenticated": "NO"}), 401


@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
def data_messages(message_group_uuid):

  session['is_auth'], cognito_user_id = verify_jwt_token()
  is_auth = session.get('is_auth', False)
  app.logger.debug(is_auth)

  if is_auth:
    app.logger.info('******Authenticated********')
    app.logger.debug(cognito_user_id)
    model = Messages.run(cognito_user_id=cognito_user_id, message_group_uuid=message_group_uuid)
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  else:
    app.logger.info('******NOT Authenticated********')
    return jsonify({"Authenticated": "NO"}), 401


@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
  session['is_auth'], cognito_user_id = verify_jwt_token()
  is_auth = session.get('is_auth', False)
  app.logger.debug(is_auth)
  
  message_group_uuid   = request.json.get('message_group_uuid',None)
  user_receiver_handle = request.json.get('handle',None)
  message = request.json['message']


  if is_auth:
    app.logger.info('******Authenticated********')
    app.logger.debug(cognito_user_id)
    if message_group_uuid == None:
      # Create for the first time
      model = CreateMessage.run(
        mode="create",
        message=message,
        cognito_user_id=cognito_user_id,
        user_receiver_handle=user_receiver_handle
      )
    else:
      # Push onto existing Message Group
      model = CreateMessage.run(
        mode="update",
        message=message,
        message_group_uuid=message_group_uuid,
        cognito_user_id=cognito_user_id
      )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  else:
    app.logger.info('******NOT Authenticated********')
    return jsonify({"Authenticated": "NO"}), 401



@app.route("/api/activities/notifications", methods=['GET'])
def data_notifications():
  data = NotificationsActivities(xray_recorder).run()
  return data, 200

@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
  # user_handle  = 'andrewbrown'
  user_handle = request.json["user_handle"]
  message = request.json['message']
  ttl = request.json['ttl']
  model = CreateActivity.run(message, user_handle, ttl)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200
  return

@app.route("/api/users/@<string:handle>/short", methods=['GET'])
def data_users_short(handle):
  data = UsersShort.run(handle)
  return data, 200

@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401

if __name__ == "__main__":
  app.run(debug=True)