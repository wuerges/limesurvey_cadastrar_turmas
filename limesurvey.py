import requests
import json
import typer
import inspect

your_domain = "localhost"
your_limesurvey_dir = "limesurvey/limesurvey"
url = f"http://{your_domain}/{your_limesurvey_dir}/index.php/admin/remotecontrol"

def client(url):
    def client_pars(func):
        def wrap(*params, **kwargs):
            payload = { 'method': func.__name__, 'params': params, 'id': 1 }

            return requests.post(url, json=payload).json()['result']
        return wrap
    return client_pars

# function get_session_key(string $username, string $password, string $plugin = 'Authdb')
@client(url)
def get_session_key(username, password, plugin='AuthDb'):
    pass

# function release_session_key(string $sSessionKey)
@client(url)
def release_session_key(sSessionKey):
    pass

# add_participants(string $sSessionKey,integer $iSurveyID,array 
# $aParticipantData,boolean $bCreateToken = true): array
@client(url)
def add_participants(sSessionKey, iSurveyID, aParticipantData, bCreateToken):
    pass

# copy_survey(string $sSessionKey,integer $iSurveyID_org,string $sNewname): array
@client(url)
def copy_survey(sSessionKey, iSurveyID_org, sNewname):
    pass

from jsonrpcclient.clients.http_client import HTTPClient

def main():

    k = get_session_key("admin", "admin")
    typer.echo(k)
    typer.echo(release_session_key(k))

if __name__ == "__main__":
    typer.run(main)