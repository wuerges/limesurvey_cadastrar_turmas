import requests
import json
import typer
import inspect
import cadastrar
from pathlib import Path

your_domain = "localhost"
your_limesurvey_dir = "limesurvey/limesurvey"
url = f"http://{your_domain}/{your_limesurvey_dir}/index.php/admin/remotecontrol"


def client(func):
    def wrap(self, *params, **kwargs):
        payload = {'method': func.__name__, 'params': params, 'id': 1}

        return requests.post(self.url, json=payload).json()['result']
    return wrap


class LimeClient:

    def __init__(self, url):
        self.url = url

    # function get_session_key(string $username, string $password, string $plugin = 'Authdb')

    @client
    def get_session_key(self, username, password, plugin='AuthDb'):
        pass

    # function release_session_key(string $sSessionKey)
    @client
    def release_session_key(self, sSessionKey):
        pass

    # add_participants(string $sSessionKey,integer $iSurveyID,array
    # $aParticipantData,boolean $bCreateToken = true): array
    @client
    def add_participants(self, sSessionKey, iSurveyID, aParticipantData, bCreateToken):
        pass

    # copy_survey(string $sSessionKey,integer $iSurveyID_org,string $sNewname): array
    @client
    def copy_survey(self, sSessionKey, iSurveyID_org, sNewname):
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

    @client
    def activate_tokens(self, sSessionKey, iSurveyID, aAttributeFields):
        pass

# from jsonrpcclient.clients.http_client import HTTPClient


def main(dataset: Path, curso: str):

    your_domain = "localhost"
    your_limesurvey_dir = "limesurvey/limesurvey"
    url = f"http://{your_domain}/{your_limesurvey_dir}/index.php/admin/remotecontrol"

    data = cadastrar.load_students(dataset, curso)

    client = LimeClient(url)

    k = client.get_session_key("admin", "admin")
    typer.echo(k)

    r = client.copy_survey(
        k, 683333, "Auto-avaliação do Curso de Ciência da Computação da UFFS - Chapecó (Cópia 2)")
    typer.echo(r)
    newsid = r['newsid']

    typer.echo(client.activate_tokens(k, newsid, []))

    ps = client.add_participants(
        k, newsid, [e.limesurvey() for e in data], True)
    typer.echo(ps)

    typer.echo(client.release_session_key(k))


if __name__ == "__main__":
    typer.run(main)
