import pandas as pd
import typer
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

    def disciplina(self):
        return self.line.disciplina

    def limesurvey(self):
        n = self.line.nome_estudante.strip().split()
        last = n[-1]
        first = " ".join(n[:-1])

        return {"email": self.line.email,"lastname":last,"firstname": first}


def load_students(path: Path, curso):
    data = pd.read_csv(path, sep=";")
    data = filtra_curso(data, curso)
    data = filtra_ativos(data)
    students = []
    for _, l in data.iterrows():
        students.append(Estudante(l))
    return students

def load_turmas(path: Path, curso):
    data = pd.read_csv(path, sep=";")
    data = filtra_curso(data, curso)
    data = filtra_ativos(data)

    print(data.columns)

    data = data.groupby(['codigo_turma', 'disciplina'])

    return data
    


def main(dataset: Path, curso: str):

    data = load_students(dataset, curso)

    turmas = load_turmas(dataset, curso)
    typer.echo(f"Turmas: {len(turmas)}")

    for k,v in turmas:
        g = turmas.get_group(k)
        disc = g['disciplina']
        doc = g['docentes']
        # typer.echo(turmas.get_group(k))
        typer.echo(disc)
        typer.echo(doc)
    # typer.echo(data['descricao_turma'].unique())
    # typer.echo(data.describe())
    # typer.echo(data)

    for i, e in enumerate(data):
        if i > 10: break

        typer.echo(f"Est: {e.nome()} {e.limesurvey()}")


    # data.group_by([''])

    # for i, l in data.iterrows():
    #     # if i > 10: break

    #     e = Estudante(l)
    #     typer.echo(f"Est({i}): {e.nome()} ({e.email()}) -> {e.disciplina()} ({e.line.codigo_turma})")
    #     break


if __name__ == "__main__":
    typer.run(main)
