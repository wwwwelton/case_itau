# Case Técnico para Vaga de Engenheiro de Software Itaú
### Descrição do projeto
Este projeto é uma API que retorna uma lista de livros com base em autor e/ou gênero de livro preferido.

### Arquitetura e serviços utilizados
Utilizando [Python](https://www.python.org/) e com base no fator escalabilidade, foi utilizado o serviço [Amazon API Gateway](https://aws.amazon.com/pt/api-gateway/) que invoca uma [AWS Lambda](https://aws.amazon.com/pt/lambda/). Para extender as funcionalidades e permitir mais recursos, o framework [Flask](https://flask.palletsprojects.com/en/3.0.x/) é quem defina as rotas da API. Foram utilizados os serviços externos para consulta [Google Books APIs](https://developers.google.com/books/docs/overview?hl=pt-br) e [Open Library](https://openlibrary.org/) com o objetivo de principal de facilitar o teste da aplicação porque ambos não obrigam o uso de uma chave de autorização.
Com o objetivo de refinar o resultado de busca, a LLM da [OpenAI](https://openai.com/) com o modelo [gpt-4o-mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) foi implementado para dois casos de uso, o primeiro sendo o ranqueamento para filtrar os 10 melhores livros e o segundo para melhorar e corrigir campos como idioma e data de publicação.
O modelo [gpt-4o-mini](https://openai.com/index/gpt-4o-mini-advancing-cost-efficient-intelligence/) foi escolhido para obter o melhor balanço entre qualidade, custo e velocidade. Testado extensivamente atráves do [playground](https://platform.openai.com/playground/) da OpenAi. Algumas ténicas foram aplicadas no prompt, como definir uma personalidade e usar parâmetros como temperature baixa, afim de evitar alteração do conteúdo e alucinações.

### Ilustração da arquitetura utilizada
IMAGEM AQUI

## Começando
#### Requisitos:
- [Python 3.10](https://www.python.org/downloads/)
- [pip >= 24.0](https://pip.pypa.io/en/stable/cli/pip_install/)
- [virtualenv >= 20](https://virtualenv.pypa.io/en/latest/installation.html)
- [AWS CLI](https://aws.amazon.com/pt/cli/)
- [Terraform](https://www.terraform.io/)

#### Opcional:
- [AWS SAM CLI](https://aws.amazon.com/pt/serverless/sam/)

### Siga os passos
```Faça o download e descompacte o arquivo case_itau.zip em seguida entre na pasta case_itau. Você verá algo como a seguinte estrutura de pastas:```
```
.
├── README.md
├── app
│   ├── application
│   │   ├── llm_service.py
│   │   ├── request_service.py
│   │   └── services.py
│   ├── domain
│   │   └── models.py
│   ├── infrastructure
│   │   └── repositories.py
│   └── interfaces
│       └── api.py
├── function.zip
├── requirements.txt
├── run.py
├── setup.sh
├── template.yaml
├── .env
└── terraform
    ├── main.tf
    └── variables.tf
```

#### Antes de começar
```Na raíz do projeto existe um arquivo chamado .env e na pasta terraform outro variables.tf. Preencha as variáveis de ambiente {GOOGLE_API} com uma chave válida do serviço Google Books APIs para evitar um possível limite de chamadas usando o parâmetro use_api=1. Para refinar os resultados usando LLM com a API da OpenAI, preencha a varíavel {OPENAI_API_KEY}. No caso de ignorar a variável {GOOGLE_API} pode ocorrer simplesmente um erro na chamada resultando em erro na busca. Caso a variável {OPENAI_API_KEY} for inexistente, o sistema simplesmente não envia os resultados para o serviço da OpenAI e o retorno será o resultado bruto das APIs de busca externa.```

#### Rodando localmente
```Obs: A pasta contém um arquivo template.yaml para ser usado com AWS SAM CLI para testar localmente se desejado simular um ambiente mais próximo da AWS.```
```bash
# Crie um ambiente virtual para a instalação dos pacotes do Python
virtualenv venv

# Ative o ambiente virtual, para não poluir o sistema com vários pacotes
source venv/bin/activate # Linux
.\venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt ou pip3 install -r requirements.txt # dependendo do sistema

# Rode o projeto
python3 run.py ou python run.py # dependendo do sistema

# Agora no navegador ou aplicativo preferido teste se tudo está ok com um exemplo de URL com os parâmetros:
http://localhost:5000/?authors=Tolkien,J.R.R&genres=Fantasy,Adventure&use_api=2

# A resposta vai ser algo como
{
    "books": [
        {
            "title": "The Lord of the Rings",
            "authors": ["J.R.R. Tolkien"],
            "buy_link": "http://example.com/buy/lotr",
            "description": "An epic fantasy trilogy.",
            "genres": ["Fantasy", "Adventure"],
            "image_link": "http://example.com/images/lotr.jpg",
            "isbn": ["978-0-261-10238-6"],
            "languages": ["English"],
            "page_count": "1178",
            "published_date": ["1954-07-29"],
            "publisher": ["George Allen & Unwin"],
            "subtitle": ""
        }
    ],
    "message": "Request processed successfully",
    "status": "successful"
}

# Localmente você pode também pode utilizar pelo navegador o OpenAPI/Swagger para realizar as chamadas atráves da URL:
http://localhost:5000/apidocs/

# Depois de tudo testado, o servidor pode ser encerrado e o ambiente virtual desativado
deactivate

# Bom trabalho!
```

#### Deploy da aplicação com terraform
```Para facilitar o deploy da aplicação o projeto juntamente com as dependências foram compactados no arquivo function.zip.```

```Caso algum arquivo seja alterado e seja necessário compactar novamente a aplicação, crie uma pasta chamada dependencies e instale as dependências dentro desta pasta em seguida compacte o diretório inteiro novamente em um arquivo chamado function.zip```

```Obs: Tenha certeza de ter as credenciais e permissões da AWS configuradas, qualquer dúvida quanto as políticas e permissões que o usuário deve ter, consulte o arquivo terraform/main.tf e realize as modificações caso necessário. As permissões também apareceram quando o deploy for iniciado com o terraform.```

```bash
# Apartir da raíz do projeto acessa a pasta terraform e execute os comandos
# Inicie o projeto do terraform
terraform init

# Inicie o deploy e faça as confirmações necessárias
terraform apply

# Se tudo deu certo você verá a URL pública da aplicação na saída ou poderá consulta no painel da AWS
# Exemplo de saída
api_gateway_url = "https://a4o1yhc02cc.execute-api.sa-east-1.amazonaws.com/dev"

# Como localmente basta realizar os testes atráves do seu aplicativo preferido com a URL e parâmetros de exemplo
https://a4o1yhc02cc.execute-api.sa-east-1.amazonaws.com/dev/?authors=Tolkien,J.R.R&genres=Fantasy,Adventure&use_api=2

# A resposta vai ser algo como
{
    "books": [
        {
            "title": "The Lord of the Rings",
            "authors": ["J.R.R. Tolkien"],
            "buy_link": "http://example.com/buy/lotr",
            "description": "An epic fantasy trilogy.",
            "genres": ["Fantasy", "Adventure"],
            "image_link": "http://example.com/images/lotr.jpg",
            "isbn": ["978-0-261-10238-6"],
            "languages": ["English"],
            "page_count": "1178",
            "published_date": ["1954-07-29"],
            "publisher": ["George Allen & Unwin"],
            "subtitle": ""
        }
    ],
    "message": "Request processed successfully",
    "status": "successful"
}

# Depois de tudo testado, os serviços da AWS podem ser parados/excluídos
# Apartir da pasta do terraform onde os comandos foram executados, basta rodar o comando
terraform destroy -auto-approve

# Bom trabalho!
```

---

## Documentação da API

#### Realizando as requisições

<details>
 <summary><code>GET</code> <code><b>/</b></code> <code>(retorna um erro de parâmetros inválidos ou ausentes)</code></summary>

##### Parâmetros

> Nenhum

##### Respostas

> | código http     | tipo do conteúdo                      | resposta                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `400`         | `application/json`                | `{ "books": [], "message": "Invalid arguments or no arguments were provided", "status": "error" }`                            |

##### Examplo cURL

> ```bash
>  curl -X GET "http://localhost:5000/" -H "accept: application/json"
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/?{authors}&{use_api}</b></code> <code>(retorna uma lista de livros com base nos autores)</code></summary>

##### Parâmetros

> | nome              |  tipo     | tipo de dado      | descrição                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `authors` |  opcional | lista de string  | Pesquisa por livros atráves de um ou mais autores        |
> | `use_api` |  opcional | inteiro  | Seleciona a API de pesquisa externa 1 ou 2        |

##### Respostas

> | código http     | tipo do conteúdo                      | resposta                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{ "books": [ { "title": "Harry Potter and the Philosopher's Stone", "authors": ["J.K. Rowling"], "buy_link": "http://example.com/buy/hp1", "description": "A young wizard's journey begins.", "genres": ["Fantasy"], "image_link": "http://example.com/images/hp1.jpg", "isbn": ["978-0-7432-1234-5"], "languages": ["English"], "page_count": "223", "published_date": ["1997-06-26"], "publisher": ["Bloomsbury"], "subtitle": "" } ], "message": "Request processed successfully", "status": "successful" }`                                                          |
> | `404`         | `application/json`                | `{ "books": [], "message": "No recommended books found", "status": "error" }`                            |
> | `408`         | `application/json`                | `{ "books": [], "message": "No search API available at this time", "status": "error" }`                            |

##### Examplo cURL

> ```bash
>  curl -X GET "http://localhost:5000/?authors=J.K.%20Rowling,J.R.R.%20Tolkien&use_api=1" -H "accept: application/json"
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/?{genres}&{use_api}</b></code> <code>(retorna uma lista de livros com base nos gêneros)</code></summary>

##### Parâmetros

> | nome              |  tipo     | tipo de dado      | descrição                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `genres` |  opcional | lista de string  | Pesquisa por livros atráves de um ou mais gêneros        |
> | `use_api` |  opcional | inteiro  | Seleciona a API de pesquisa externa 1 ou 2        |

##### Respostas

> | código http     | tipo do conteúdo                      | resposta                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{ "books": [ { "title": "The Hobbit", "authors": ["J.R.R. Tolkien"], "buy_link": "http://example.com/buy/hobbit", "description": "A fantasy novel about a hobbit's adventure.", "genres": ["Fantasy", "Adventure"], "image_link": "http://example.com/images/hobbit.jpg", "isbn": ["978-3-16-148410-0"], "languages": ["English"], "page_count": "310", "published_date": ["1937-09-21"], "publisher": ["George Allen & Unwin"], "subtitle": "There and Back Again" } ], "message": "Books found", "status": "success" }`                                                          |
> | `404`         | `application/json`                | `{ "books": [], "message": "No recommended books found", "status": "error" }`                            |
> | `408`         | `application/json`                | `{ "books": [], "message": "No search API available at this time", "status": "error" }`                            |

##### Examplo cURL

> ```bash
>  curl -X GET "http://localhost:5000/?genres=Fantasy,Adventure&use_api=2" -H "accept: application/json"
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/?{authors}&{genres}&{use_api}</b></code> <code>(retorna uma lista de livros com base nos autores e gêneros)</code></summary>

##### Parâmetros

> | nome              |  tipo     | tipo de dado      | descrição                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `authors` |  opcional | lista de string  | Pesquisa por livros atráves de um ou mais autores        |
> | `genres` |  opcional | lista de string  | Pesquisa por livros atráves de um ou mais gêneros        |
> | `use_api` |  opcional | inteiro  | Seleciona a API de pesquisa externa 1 ou 2        |

##### Respostas

> | código http     | tipo do conteúdo                      | resposta                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`        | `{ "books": [ { "title": "The Hobbit", "authors": ["J.R.R. Tolkien"], "buy_link": "http://example.com/buy/hobbit", "description": "A fantasy novel about a hobbit's adventure.", "genres": ["Fantasy", "Adventure"], "image_link": "http://example.com/images/hobbit.jpg", "isbn": ["978-3-16-148410-0"], "languages": ["English"], "page_count": "310", "published_date": ["1937-09-21"], "publisher": ["George Allen & Unwin"], "subtitle": "There and Back Again" }, { "title": "Harry Potter and the Philosopher's Stone", "authors": ["J.K. Rowling"], "buy_link": "http://example.com/buy/hp1", "description": "A young wizard's journey begins.", "genres": ["Fantasy", "Adventure"], "image_link": "http://example.com/images/hp1.jpg", "isbn": ["978-0-7432-1234-5"], "languages": ["English"], "page_count": "223", "published_date": ["1997-06-26"], "publisher": ["Bloomsbury"], "subtitle": "" } ], "message": "Request processed successfully", "status": "successful" }`                                                          |
> | `404`         | `application/json`                | `{ "books": [], "message": "No recommended books found", "status": "error" }`                            |
> | `408`         | `application/json`                | `{ "books": [], "message": "No search API available at this time", "status": "error" }`                            |

##### Examplo cURL

> ```bash
>  curl -X GET "http://localhost:5000/?authors=J.R.R.%20Tolkien,J.K.%20Rowling&genres=Fantasy,Adventure&use_api=2" -H "accept: application/json"
> ```

</details>

#### Exemplo de uso com um programa de consultas
IMAGEM AQUI

</br>

##### Observações
```Qualquer consulta além do método GET ou path não especificados resultaram em erro.```
```O parâmetro {use_api} tem por padrão o valor 2.```
```Se a aplicação não encontrar a variável de ambiente {OPENAI_API_KEY} ela simplesmente devolve a lista de livros sem tratamento pela LLM.```
```Se a aplicação não encontrar a variável de ambiente {GOOGLE_API} pode acontecer um limite de requisições diárias, resultado em falha na consulta.```

---

## Links úteis
| Nome | Link |
| - | - |
| OpenAI Docs | https://platform.openai.com/docs/overview |
| OpenAI Playground | https://platform.openai.com/playground |
| AWS Lambda Documentation | https://docs.aws.amazon.com/lambda/ |
| Amazon API Gateway Documentation | https://docs.aws.amazon.com/apigateway/ |
| Terraform Docs Overview | https://developer.hashicorp.com/terraform/docs |
| Flask | https://flask.palletsprojects.com/en/3.0.x/ |
| Swagger Documentation | https://swagger.io/docs/ |
| Excalidraw | https://excalidraw.com/ |
| ChatGPT | https://chat.openai.com/ |
| GitHub Copilot Chat | https://code.visualstudio.com/docs/copilot/getting-started-chat |

---

Desenvolvido por: Welton Leite 👋 [Acesse meu LinkedIn](https://www.linkedin.com/in/welton-leite-b3492985/)
