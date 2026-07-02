# AgroLogic

Produtores rurais de médio porte enfrentam dificuldade para definir o preço justo de venda da sua produção quando negociam com compradores locais sem acesso a referências atualizadas de mercado, o que resulta em margens reduzidas e perda recorrente de receita.

O AgroLogic nasce para resolver esse problema: uma calculadora que estima o preço do gado o mais próximo possível do valor praticado no mercado atual, a partir de dados como peso, categoria e valor da arroba na praça, dando ao produtor uma referência confiável antes de fechar negócio.

## Estrutura do projeto

```text
AgroLogic1/
├── frontend/
└── backend/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── controllers/
    │   └── boi_controller.py
    ├── models/
    │   ├── database.py
    │   └── boi_model.py
    ├── repositories/
    │   └── README.md
    ├── services/
    │   ├── criar_boi_service.py
    │   ├── listar_bois_service.py
    │   ├── buscar_boi_por_id_service.py
    │   ├── atualizar_boi_service.py
    │   └── deletar_boi_service.py
    └── database/
        └── create_database.sql
```

## Arquitetura usada

```text
Frontend
   ↓
Controller
   ↓
Service
   ↓
Model
   ↓
Banco de Dados
```

Cada camada tem uma responsabilidade única: o **Controller** recebe a requisição HTTP e devolve a resposta, o **Service** contém a regra de negócio de cada caso de uso, e a **Model** concentra o acesso ao banco (herdando de `db.Model`) e o cálculo de preço do boi.

## Funcionalidades implementadas (backend)

CRUD de Bois:

- Cadastrar um boi, informando raça, categoria, peso, idade e valor da arroba (o preço é calculado automaticamente);
- Listar todos os bois cadastrados;
- Buscar um boi pelo id;
- Atualizar os dados de um boi (o preço estimado é recalculado quando peso ou valor da arroba mudam);
- Excluir um boi.

### Como o preço é calculado

O valor estimado segue a lógica usada no mercado pecuário: o peso do animal é convertido de quilos para arrobas (1 arroba = 15 kg) e multiplicado pelo valor da arroba informado.

```text
preço_estimado = (peso_kg / 15) * valor_arroba
```

## Como executar o backend

Entre na pasta do backend:

```bash
cd backend
```

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual.

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o arquivo `.env` com base no exemplo:

```bash
cp .env.example .env
```

Execute o backend:

```bash
python app.py
```

A API ficará disponível em:

```text
http://127.0.0.1:5000
```

## Banco de dados

Por padrão, o projeto usa SQLite para facilitar o teste local:

```text
DATABASE_URL=sqlite:///agrologic.db
```

Para usar MySQL, execute o script:

```text
backend/database/create_database.sql
```

Depois altere o `.env` para:

```text
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/agrologic
```

## Rotas da API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/bois` | Lista todos os bois cadastrados |
| GET | `/bois/<id>` | Busca um boi pelo id |
| POST | `/bois` | Cadastra um boi e calcula o preço estimado |
| PUT | `/bois/<id>` | Atualiza um boi e recalcula o preço quando necessário |
| DELETE | `/bois/<id>` | Remove um boi |

## Exemplo de JSON para cadastrar

```json
{
  "raca": "Nelore",
  "categoria": "Boi Gordo",
  "peso_kg": 480,
  "idade_meses": 36,
  "valor_arroba": 300.00
}
```

## Resposta esperada

```json
{
  "id": 1,
  "raca": "Nelore",
  "categoria": "Boi Gordo",
  "peso_kg": 480,
  "idade_meses": 36,
  "valor_arroba": 300.0,
  "preco_estimado": 9600.0,
  "data_avaliacao": "2026-07-01T12:00:00"
}
```

## Status atual do projeto

Esta etapa cobre apenas o backend: models, controllers, services e persistência no banco. A camada de frontend (telas de cadastro, listagem, edição e exclusão consumindo essas rotas) faz parte da próxima etapa do trabalho.
