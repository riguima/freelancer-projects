# Freelancer Projects

Simples aplicação que junta projetos do 99freelas e do Workana em uma única página para fácil acesso.

# Instalação

Segue script para instalação:

```
git clone https://github.com/riguima/freelancer-projects
cd freelancer-projects
pip install -r requirements.txt
```

Renomeie o arquivo __.base.config.toml__ para __.config.toml__ e altere as configurações se necessário.

- DATABASE_URI = URL do banco de dados, exemplo com postgres: `postgresql://username:password@localhost:5432/database`
- MAX_PROJECTS = Número máximo de projetos que o banco de dados vai armazenar

Você vai precisar exportar os cookies da página do Workana com seu login, para isso utilize a extensão de navegador __Export cookie JSON file for Puppeter__.

Depois de exportar para JSON, renomeie para __workana-cookies.json__ e mova para __freelancer-projects__.

Rode com `flask run` e acesse `http://localhost:5000/`.

Ou usando Docker:

```
sudo docker build -t freelancer-projects .
sudo docker run --name freelancer-projects -p 5000:5000 -d freelancer-projects
```
