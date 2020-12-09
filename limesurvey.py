import requests
import json
import typer
import inspect
import cadastrar
import config
from pathlib import Path



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


app = typer.Typer()

@app.command()
def check(dataset: Path, curso: str):
    client = LimeClient(config.URL)

    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    typer.echo(k)
    typer.echo(client.release_session_key(k))



@app.command()
def geral(dataset: Path, curso: str, modelo: int, nome: str):
    client = LimeClient(config.URL)

    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    estudantes = cadastrar.load_students(dataset, curso)
    estudantes = [e.limesurvey() for e in estudantes]

    r = client.copy_survey(
        k,
        modelo,
        nome
    )

    typer.echo("Created a new survey")
    newsid = r['newsid']

    client.activate_tokens(k, newsid, [])
    typer.echo("Created survey user table")

    client.add_participants(
         k, newsid, estudantes, True)

    typer.echo("Added participants to survey")



@app.command()
def turmas(dataset: Path, curso: str, modelo: int, padrao: str):
    client = LimeClient(config.URL)

    k = client.get_session_key(config.LOGIN, config.PASSWORD)

    turmas = cadastrar.load_turmas(dataset, curso)

    for t in turmas:

        nome_formulario = padrao.format(t.codigo, t.nome)
        estudantes = [e.limesurvey() for e in t.estudantes]
        # typer.echo(nome_formulario)


        r = client.copy_survey(
            k,
            modelo,
            nome_formulario
        )

        newsid = r['newsid']
        client.activate_tokens(k, newsid, [])

        client.add_participants(
            k, newsid, estudantes, True)

        typer.echo(f"Created survey for: {nome_formulario}")



if __name__ == "__main__":
    app()
