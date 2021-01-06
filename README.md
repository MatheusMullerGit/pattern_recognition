Clonar o repositório para a máquina local

Abrir CMD
Entrar na pasta do projeto que contém o arquivo Dockerfile
Executar "docker build -t matheusmullergit/pattern_recognition ."
Executar "docker run -d --name pattern_recognition_01 -p 8501:8501 matheusmullergit/pattern_recognition"
Executar "docker run -d --name pattern_recognition_02 -p 8502:8501 matheusmullergit/pattern_recognition"
Executar "docker run -d --name pattern_recognition_03 -p 8503:8501 matheusmullergit/pattern_recognition"