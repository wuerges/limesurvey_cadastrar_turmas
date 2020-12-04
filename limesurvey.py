import requests
import json
import typer
import inspect
import cadastrar
from pathlib import Path

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

# activate_tokens
#    /**
#         * Activate survey participants (RPC function)
#         *
#         * Initialise the survey participant table of a survey where new participant tokens may be later added.
#         *
#         * @access public
#         * @param string $sSessionKey Auth credentials
#         * @param integer $iSurveyID ID of the Survey where a survey participants table will be created for
#         * @param array $aAttributeFields  An array of integer describing any additional attribute fields
#         * @return array Status=>OK when successful, otherwise the error description
#         */

@client(url)
def activate_tokens(sSessionKey, iSurveyID, aAttributeFields):
    pass

from jsonrpcclient.clients.http_client import HTTPClient

def main(dataset: Path, curso: str):
    data = cadastrar.load_students(dataset, curso)

    k = get_session_key("admin", "admin")
    typer.echo(k)

    r = copy_survey(k, 683333, "Auto-avaliação do Curso de Ciência da Computação da UFFS - Chapecó (Cópia 2)")
    typer.echo(r)
    #{'status': 'OK', 'newsid': 638847}
    newsid = r['newsid']

    typer.echo(activate_tokens(k, newsid, []))

    ps = add_participants(k, newsid, [e.limesurvey() for e in data], True)
    typer.echo(ps)

    typer.echo(release_session_key(k))
if __name__ == "__main__":
    typer.run(main)