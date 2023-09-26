import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from .policy import Policy
import json

""" The code at the top is from Google's documentation"""
# Use the client_secret.json file to identify the application requesting
# authorization. The client ID (from that file) and access scopes are required.
flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile', 'openid',
            'https://www.googleapis.com/auth/userinfo.email'])

# Indicate where the API server will redirect the user after the user completes
# the authorization flow. The redirect URI is required. The value must exactly
# match one of the authorized redirect URIs for the OAuth 2.0 client, which you
# configured in the API Console. If this value doesn't match an authorized URI,
# you will get a 'redirect_uri_mismatch' error.
flow.redirect_uri = settings.LOGIN_URL

# Generate URL for request to Google's OAuth 2.0 server.
# Use kwargs to set optional request parameters.
authorization_url, state = flow.authorization_url(
    # Enable offline access so that you can refresh an access token without
    # re-prompting the user for permission. Recommended for web server apps.
    access_type='offline',
    # Enable incremental authorization. Recommended as a best practice.
    include_granted_scopes='true')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


"""
I use DRF(Django Rest Framework) in practice. I didn't use any models here and therefore didn't need the serialization
and other tools that it provides. I relied on basic Django to keep it simple.
Note: I didn't implement SSL due to the nature of the task, but it would be a must in production.
"""

@require_http_methods(["GET"])
def login(request):
    return JsonResponse({"auth_url": authorization_url})


@require_http_methods(["GET"])
def logged_in(request):
    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    request.session.modified = True
    return redirect(settings.FRONTEND_URL)


@require_http_methods(["GET"])
def logout(request):
    del request.session['credentials']
    request.session.modified = True
    return JsonResponse({"success": True})


@require_http_methods(["GET"])
def user_info(request):
    data = {"name": None, "loggedIn": False}
    if 'credentials' in request.session:
        credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])
        oauth2_client = build('oauth2', 'v2', credentials=credentials)
        user_info = oauth2_client.userinfo().get().execute()
        data["name"] = user_info["name"]
        data["loggedIn"] = True
    return JsonResponse(data)


@require_http_methods(["POST"])
def unstructured(request):
    policy_string = json.loads(request.body)['policy']
    policy = Policy(policy_string)
    try:
        data = policy.review_policy()
    except Exception as e:
        print(e)
        data = policy.get_result()
    return JsonResponse(data)
