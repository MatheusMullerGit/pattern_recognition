Clonar o repositório para a máquina local

Abrir Prompt de Comando/ Windows PowerShell
Entrar na pasta do projeto que contém o arquivo Dockerfile
Executar os comandos na sequência abaixo:

Sobe o container com a imagem desta pasta com o nome de Usuário: MatheusMullerGit e nome da Imagem: pattern_recognition para a pasta local (.) do Docker.
"""
docker build -t matheusmullergit/pattern_recognition .
"""
Cria cada container (no exemplo são utilizados 10) utilizando a imagem criada no passo anterior, expondo a porta 8501 de cada container para uma porta distinta na máquina local.
""" 
docker run -d --name pattern_recognition_01 -p 8501:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_02 -p 8502:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_03 -p 8503:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_04 -p 8504:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_05 -p 8505:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_06 -p 8506:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_07 -p 8507:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_08 -p 8508:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_09 -p 8509:8501 matheusmullergit/pattern_recognition
docker run -d --name pattern_recognition_10 -p 8510:8501 matheusmullergit/pattern_recognition
"""
Após a execução destes passos, as máquinas virtuais podem ser acessadas pelo navegador na máquina local através dos endereços sequenciais localhost:8501 à localhost:8510.