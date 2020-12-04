import requests
import json
import typer
import inspect

your_domain = "localhost"
your_limesurvey_dir = "srv/http/limesurvey/limesurvey"
url = f"http://{your_domain}/{your_limesurvey_dir}/index.php/admin/remotecontrol"


def client(url):
    def client_pars(func):
        signature = inspect.signature(func)

        def wrap(*args, **kwargs):

            params = {}
            for k,v in signature.parameters.items():
                p = kwargs.get(k)
                if p:
                    params[k] = p
                else:
                    params[k] = v.default

            payload = { 'method': func.__name__, 'params': params }
            return requests.post(url, json=payload).json()
        return wrap
    return client_pars

@client(url)
def auth(username, password, plugin='AuthDb'):
    pass

def main():

    auth(username="kappa", password="pass")
    typer.echo(url)



# function get_session_key(string $username, string $password, string $plugin = 'Authdb')

if __name__ == "__main__":
    typer.run(main)