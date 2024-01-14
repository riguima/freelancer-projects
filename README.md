# Freelancer Projects

Simples aplicação que junta projetos do 99freelas e do Workana em uma única página para fácil acesso.

# Instalação

Segue script para instalação:

```
git clone https://github.com/riguima/freelancer-projects
cd freelancer-projects
pip install -r requirements.txt
```

Você vai precisar exportar os cookies da página do Workana com seu login, para isso utilize a extensão de navegador __Export cookie JSON file for Puppeter__.

Depois de exportar para JSON, renomeie para __workana-cookies.json__ e mova para __freelancer-projects__.

Rode com `flask run` e acesse `http://localhost:5000/`.
