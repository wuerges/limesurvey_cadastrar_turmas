import pandas as pd
import typer
import json
from pathlib import Path


def filtra_curso(dataset, curso):
    return dataset[dataset.descricao_turma.str.contains(curso)]

def filtra_ativos(dataset):
    return dataset[dataset.situacao_matricula.str.contains("ATIVA")]

class Estudante:
    def __init__(self, line):
        self.line = line

    def __repr__(self):
        return self.line.nome_estudante
    
    def nome(self):
        return self.line.nome_estudante

    def email(self):
        return self.line.email

    def limesurvey(self):
        n = self.line.nome_estudante.strip().split()
        last = n[-1]
        first = " ".join(n[:-1])

        return {"email": self.line.email,"lastname":last,"firstname": first}

class Turma:
    def __init__(self, key, data):
        (codigo, self.nome, docentes) = key
        self.codigo = int(codigo)
        self.data = data
        self.estudantes = [Estudante(e) for i, e in self.data.iterrows()]
        self.docentes = [d.strip() for d in docentes.split(";")]

    def __iter__(self):
        return self.estudantes.__iter__()

    def json(self):
        estudantes = [e.limesurvey() for e in self.estudantes]
        return {'nome': self.nome, 'docentes': self.docentes, 'codigo':self.codigo, 'estudantes': estudantes }



def load_students(path: Path, curso):
    data = pd.read_csv(path, sep=";")
    data = filtra_curso(data, curso)
    data = filtra_ativos(data)
    data = data[["nome_estudante", "email"]].drop_duplicates()
    students = []
    for _, l in data.iterrows():
        students.append(Estudante(l))
    return students

def load_turmas(path: Path, curso):
    data = pd.read_csv(path, sep=";")
    data = filtra_curso(data, curso)
    data = filtra_ativos(data)
    groups = data.groupby(['codigo_turma', 'disciplina', 'docentes'])

    turmas = [Turma(k, groups.get_group(k)) for k,_ in groups]

    return turmas
    


def main(dataset: Path, curso: str, comando: str):

    # data = load_students(dataset, curso)

    if comando == "estudantes":
        estudantes = load_students(dataset, curso)    
        for e in estudantes:
            typer.echo(json.dumps(e.limesurvey()))

    elif comando == "turmas":

        turmas = load_turmas(dataset, curso)

        for t in turmas:
            typer.echo(json.dumps(t.json()))
            # typer.echo(t.json())


if __name__ == "__main__":
    typer.run(main)
