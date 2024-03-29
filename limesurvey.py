import requests
import base64
import json
import typer
import inspect
import cadastrar
import config
import pandas as pd
from pathlib import Path
from typing import Optional


def from_YN(t):
    x = {'Y': True, 'N': False}
    return x[t]


class Survey:
    def __init__(self, data):
        # {'sid': 141771, 'surveyls_title': '2020/1 (remoto) - Turma#27481: Banco de dados I', 'startdate': None, 'expires': None, 'active': 'N'}
        self.sid = data['sid']
        self.title = data['surveyls_title']
        self.active = from_YN(data['active'])
        self.data = data
        self.properties = None

    def __repr__(self):
        return f"Survey({self.data})"

    def load_properties(self, client, k):        
        self.properties = client.get_survey_properties(k, self.sid)
        self.gsid = int(self.properties['gsid'])


def client(func):
    def wrap(self, *params, **kwargs):
        payload = {'method': func.__name__, 'params': params, 'id': 1}
        r = requests.post(self.url, json=payload)
        # print(r.headers)
        return r.json()['result']
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

    @client
    def list_surveys(self, sSessionKey, logis):
        pass

    @client
    def activate_survey(self, sSessionKey, sSurveyID):
        pass

    @client
    def get_survey_properties(self, sSessionKey, iSurveyID):
        pass

# /**
# * Invite participants in a survey (RPC function)
# *
# * Returns array of results of sending
# *
# * @access public
# * @param string $sSessionKey Auth credentials
# * @param int $iSurveyID ID of the survey that participants belong
# * @param array $aTokenIds Ids of the participant to invite
# * @param bool $bEmail Send only pending invites (TRUE) or resend invites only (FALSE)
# * @return array Result of the action
# */
    @client
    def invite_participants(self, sSessionKey, iSurevyID, aTokenIds, bEmail):
        pass

    @client
    def mail_registered_participants(self, sSessionKey, iSurveyID, conditions):
        pass

    @client
    def remind_participants(self, sSessionKey, iSurveyID):
        pass

    @client
    def get_group_properties(self, iGroupID, aGroupSettings):
        pass

    @client
    def export_statistics(self, sSessionKey, iSurveyID, docType, sLanguage, graph):
        pass

    @client
    def export_responses(self, sSessionKey, iSurveyID, docType, lang, completStatus, headingType, responseType):
        pass

    @client
    def list_questions(self, sSessionKey, iSurveyID): 
        pass


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


@app.command()
def listar(gsid : Optional[int] = typer.Argument(None)): # pylint: disable=unsubscriptable-object
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    s = [Survey(si) for si in s]

    for si in s:
        si.load_properties(client, k)
        if gsid:
            if gsid == si.gsid:
                typer.echo(si)
        else:
            typer.echo(si)
        # typer.echo(si.gsid)
        # typer.echo(p)


@app.command()
def ativartodos():
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    s = [Survey(si) for si in s]

    for si in s:
        if not si.active:
            client.activate_survey(k, si.sid)
            typer.echo(f"activated survey {si.title}")

@app.command()
def ativargrupo(gsid : int):
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    s = [Survey(si) for si in s]

    for si in s:
        si.load_properties(client, k)
        if not si.active and si.gsid == gsid:
            client.activate_survey(k, si.sid)
            typer.echo(f"activated survey {si.title}")


@app.command()
def enviaremailregistrados():
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    s = [Survey(si) for si in s]

    for si in s:
        if si.active:
            typer.echo(f"Survey: {si.sid}")
            r = client.mail_registered_participants(k, si.sid, [])
            typer.echo(f"result: {r}")


@app.command()
def estatistica_turma():
    import urllib
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    surveys = [Survey(si) for si in s]

    for surv in surveys:
        stats = client.export_statistics(k, surv.sid, "xls", 0, "yes")

        if stats:
            typer.echo(f"Carregada estatistica da turma: {surv.title}")

            filename = urllib.parse.quote_plus(surv.title)
            data = base64.b64decode(stats)

            with open(filename, "wb") as out:
                out.write(data)

            typer.echo(f"Salva estatistica da turma: {filename}")
        else:
            typer.echo(f"Impossivel carregar estatistica da turma: {surv.title}")

@app.command()
def survey_questions(json_outfile : Path):
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)

    surveys = [Survey(si) for si in s]

    questions = []
    for surv in surveys:
        questions.extend(client.list_questions(k, surv.sid))
    
    with open(json_outfile, 'wb') as file:
        file.write(json.dumps(questions).encode('utf8'))

        typer.echo(f"Generated JSON file with questions: {json_outfile}")

@app.command()
def respostas_turma():
    import urllib
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    surveys = [Survey(si) for si in s]

    for surv in surveys:
        stats = client.export_responses(k, surv.sid, "csv", 0, "all", "full", "long")

        if stats:
            typer.echo(f"Carregada estatistica da turma: {surv.title}")

            filename = urllib.parse.quote_plus(surv.title)

            try: 
                data = base64.b64decode(stats)
                typer.echo(f"Decoded data.")
                with open(filename, "wb") as out:
                    out.write(data)
                typer.echo(f"Saved data to file: {filename}")

            except:
                typer.echo(f"Could not parse data.")


            # typer.echo(f"Data: {data}")

        #     # with open(filename, "wb") as out:
        #     #     out.write(data)

        #     typer.echo(f"Salva estatistica da turma: {filename}")
        # else:
        #     typer.echo(f"Impossivel carregar estatistica da turma: {surv.title}")

@app.command()
def respostas_pandas(outfile: Path):
    import urllib
    from io import BytesIO

    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    surveys = [Survey(si) for si in s]

    frames = []

    for surv in surveys:
        stats = client.export_responses(k, surv.sid, "csv")

        if stats:
            typer.echo(f"Carregada estatistica da turma: {surv.title}")

            try: 
                data = base64.b64decode(stats)
                typer.echo(f"Decoded data.")

                frame = pd.read_csv(BytesIO(data), encoding="utf8", sep=";")
                frame["turma"] = surv.title

                typer.echo(f"Loaded in Pandas")

                frames.append(frame)

                typer.echo(f"Concated dataframes")


            except:
                typer.echo(f"                 Error: Could not parse data.")


            # typer.echo(f"Data: {data}")

        #     # with open(filename, "wb") as out:
        #     #     out.write(data)

        #     typer.echo(f"Salva estatistica da turma: {filename}")
        # else:
        #     typer.echo(f"Impossivel carregar estatistica da turma: {surv.title}")


    result = pd.concat(frames)
    result.to_csv(outfile)
    typer.echo(f"Stored result in {outfile}")

@app.command()
def enviarlembretes(gsid : int):
    client = LimeClient(config.URL)
    k = client.get_session_key(config.LOGIN, config.PASSWORD)
    s = client.list_surveys(k, config.LOGIN)
    s = [Survey(si) for si in s]

    for si in s:
        si.load_properties(client, k)
        if si.active and si.gsid == gsid:

            typer.echo(f"Survey: {si.sid}")
            r = client.remind_participants(k, si.sid)
            typer.echo(f"result: {r}")


if __name__ == "__main__":
    app()
