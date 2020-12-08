# Gerando formularios para todas as turmas:

```
pipenv run python limesurvey.py turmas <url_limesurvey> <database> Comput <surveyid> "Turma #{}: {}"
```

O primeiro campo e' o numero da turma e o segundo e' o nome da disciplina.

# G erando formulario geral para todos:

```
pipenv run python limesurvey.py geral <url_limesurvey> <database> Comput <suveyid> "Nome para formulario"
```
