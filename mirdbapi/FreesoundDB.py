import json
import sys
import urllib2
import subprocess
# import oauth2
# import base64
# Add doc
# ## Freesound API Access
# ```
# $ sudo pip2 install oauth2
# ```

from mirdbapi.imirdbapi import * 
class FreesoundAPI(IMirDbApi):
    __api_key = ""

    def get_access_token(self, client_id, client_secret, auth_code):
        """
            Aquire an OAuth2 access token
            To be run one time (then use refresh token)
        """
        # curl -X POST -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=authorization_code&code=THE_GIVEN_CODE" https://www.freesound.org/apiv2/oauth2/access_token/
        data = "client_id=%(client_id)s&client_secret=%(client_secret)s&grant_type=authorization_code&code=%(auth_code)s"%locals()
        print data
        request = urllib2.Request( 'https://www.freesound.org/apiv2/oauth2/access_token/', data=data )
        # request.add_header('Accept', 'application/json')
        # try:
        response = urllib2.urlopen(request)
        # except urllib2.HTTPError, exc:
        #     if exc.code == 401: # Unauthorized
        #         raise Unauthorized("Bad request")

        return json.JSONDecoder().decode(response)

    def refresh_token(self, client_id, client_secret, refresh_token):
        """
        To get a new access token using your refresh token you basically need to repeat Step 3 setting the grant_type parameter to ‘refresh_token’ (instead of ‘authorization_code’) and adding a refresh_token parameter with your refresh token (instead of adding the code parameter with the authorization code). See the following example:
# curl -X POST -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=refresh_token&refresh_token=REFRESH_TOKEN" "https://www.freesound.org/apiv2/oauth2/access_token/"
        """
        data = "client_id=%(client_id)s&client_secret=%(client_secret)s&grant_type=refresh_token&refresh_token=%(refresh_token)s"%locals()
        print data
        request = urllib2.Request( 'https://www.freesound.org/apiv2/oauth2/access_token/', data=data )
        # request.add_header('Accept', 'application/json')
        # try:
        response = urllib2.urlopen(request)
        # except urllib2.HTTPError, exc:
        #     if exc.code == 401: # Unauthorized
        #         raise Unauthorized("Bad request")
        print(response)
        return json.JSONDecoder().decode(response)

    def setApiKey(self, api_key):
        self.__api_key = api_key

    def download_by_id(self, id=""):
        #TODO wait process? run in another thread?
        auth_token = self.auth_token
        callstr =  """curl -H "Authorization: Bearer %(auth_token)s" 'https://www.freesound.org/apiv2/sounds/%(id)s/download/' > %(id)s.wav"""%locals()
        #FIXME: use urrlib2, check exceptions (Authentication credentials were not provided)
        print(callstr)
        subprocess.call( callstr, shell=True)
        return

    def search_by_id(self, id=""):
        """
            Returns a json
        """
        request = urllib2.Request("http://www.freesound.org/apiv2/sounds/%s/"%id)
        request.add_header('Authorization','Token %s'%self.__api_key)
        response = urllib2.urlopen(request).read()
        return json.JSONDecoder().decode(response)
    #search_by_id()
    
    def search_by_content(self, content=""):
        """
            Returns a json
        """
        content = content.replace (" ","%20")
        #TODO: use urllib3.request.urlencode.
        request = urllib2.Request("http://www.freesound.org/apiv2/search/content/?target=%s"%content)
        request.add_header('Authorization','Token %s'%self.__api_key)
        response = urllib2.urlopen(request).read()
        return json.JSONDecoder().decode(response) 
        #search_by_content()

    #TODO: add as a parameter and callback function processing in other methods
    def json_to_id_list(self, json_content):
        """
            Input: json
            Output: id list
        """
        ids = list()
        # print json_content
        for r in json_content["results"]:
            ids.append(r["id"])
            # print r
        return ids
    #json_to_id_list()

if __name__ == '__main__':
    # JSON config file
    config = ""
    try:
        config = json.load( open(".apicultor_config.json",'r') )
    except Exception, e:
        print(e)
        print("No json config file or error.")
        sys.exit(2)

    api = FreesoundAPI()
    api.setApiKey( config["Freesound.org"][0]["API_KEY"] )
    #api.search_by_id(31362)
    
    #content = "lowlevel.pitch.mean:220"
    #content = "lowlevel.pitch.mean:220 AND lowlevel.pitch.var:0"
    content = "lowlevel.spectral_centroid.mean:100"
    
    # TODO: ver  "distance_to_target": 5.960464477539063e-08

    # result = api.search_by_content(content)
    # print( api.json_to_id_list(result) )
    # [208252, 28638, 10549, 28966, 180268, 331309, 174398, 186752, 293605, 151033, 35426, 308937, 313960, 99203, 43943]

    """
        https://www.freesound.org/docs/api/authentication.html
    """
    client_id = config["Freesound.org"][0]["client_id"]

    auth_code = config["Freesound.org"][0]["auth_code"]
    #See: https://www.freesound.org/docs/api/authentication.html
    #if there is no auth code in config file
    # Auth code for client_id (user auth to apicultor App)
    #auth_code = api.first_auth(client_id)
    #first auth:  https://www.freesound.org/apiv2/oauth2/authorize/?client_id=YOUR_CLIENT_ID&response_type=code&state=xyz
    # then save to the config file
    # client_secret = config["Freesound.org"][0]["API_KEY"]
    # access_token_json = api.get_access_token(client_id, client_secret, auth_code)
    # print access_token
    # setup new values (&save)
    # access_token = access_token_json["access_token"]
    # refresh_token = access_token_json["refresh_token"]

    #Refresh token
    # refresh_token = config["Freesound.org"][0]["refresh_token"]
    # refresh_token_json = api.refresh_token(client_id, client_secret, refresh_token)
    # print(refresh_token_json)

    #Download file by ID
    api.auth_token = config["Freesound.org"][0]["access_token"]
    api.download_by_id(10549)
    # api.download_by_id(208252)