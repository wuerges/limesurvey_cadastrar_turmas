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

def main(dataset: Path, curso: str):
    data = pd.read_csv(dataset, sep=";")
    data = filtra_curso(data, curso)
    data = filtra_ativos(data)

    typer.echo(f"Columns: {data.columns}")
    # typer.echo(data['descricao_turma'].unique())
    # typer.echo(data.describe())
    # typer.echo(data)

    for i, l in data.iterrows():
        # if i > 10: break

        e = Estudante(l)
        typer.echo(f"Est({i}): {e.nome()} ({e.email()}) -> {e.disciplina()} ({e.line.codigo_turma})")
        break


if __name__ == "__main__":
    typer.run(main)
