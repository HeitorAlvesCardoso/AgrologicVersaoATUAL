# AgroLogic

Produtores rurais de médio porte enfrentam dificuldade para definir o preço justo de venda da sua produção quando negociam com compradores locais sem acesso a referências atualizadas de mercado, o que resulta em margens reduzidas e perda recorrente de receita.

O AgroLogic nasce para resolver esse problema: uma calculadora que estima o preço do gado o mais próximo possível do valor praticado no mercado atual, a partir de dados como peso, categoria e valor da arroba na praça, dando ao produtor uma referência confiável antes de fechar negócio.

## Estrutura do projeto

```text
AgroLogic1/
├── frontend/
├── agrologic-pages/          # cópia do front publicada no GitHub Pages
├── .github/
│   └── workflows/
│       └── deploy-pages.yml  # publica o site a cada push
├── docs/
│   └── diagrama-de-classes.md
└── backend/
    ├── app.py
    ├── requirements.txt
    ├── .env.example
    ├── controllers/
    │   └── boi_controller.py
    ├── services/
    │   ├── calcular_valor_boi_service.py
    │   ├── criar_boi_service.py
    │   ├── listar_bois_service.py
    │   ├── buscar_boi_por_id_service.py
    │   ├── atualizar_boi_service.py
    │   ├── deletar_boi_service.py
    │   ├── filtrar_por_raca_service.py
    │   ├── filtrar_por_categoria_service.py
    │   ├── filtrar_por_faixa_peso_service.py
    │   ├── buscar_boi_por_nome_service.py
    │   ├── filtrar_por_preco_minimo_service.py
    │   ├── filtrar_por_preco_maximo_service.py
    │   ├── filtrar_por_data_service.py
    │   ├── listar_avaliacoes_recentes_service.py
    │   ├── paginar_bois_service.py
    │   ├── ordenar_por_preco_crescente_service.py
    │   ├── ordenar_por_preco_decrescente_service.py
    │   ├── ordenar_por_peso_service.py
    │   └── gerar_resumo_service.py
    ├── repositories/
    │   └── boi_repository.py
    ├── models/
    │   ├── database.py
    │   └── boi_model.py
    └── database/
        └── create_database.sql
```

## Arquitetura usada

```text
Frontend/API
   ↓
Controller (recebe requisição HTTP)
   ↓
Service (regra de negócio)
   ↓
Model (acesso ao banco - CRUD)
Repository (consultas especiais)
   ↓
Banco de Dados
```

Cada camada tem uma responsabilidade única:
- **Controller** recebe a requisição HTTP e devolve a resposta.
- **Service** contém a regra de negócio de cada caso de uso (cálculo de preço, filtros, resumo).
- **Model** concentra o CRUD básico (salvar, listar, buscar, atualizar, deletar).
- **Repository** é usado para consultas especiais que vão além do CRUD simples (filtros, relatórios).

## Diagrama de classes

O diagrama de classes do domínio está em [`docs/diagrama-de-classes.md`](docs/diagrama-de-classes.md).

Ele apresenta:

- a entidade **`Boi`** com todos os atributos e operações de CRUD, herdando de `db.Model` (herança);
- o relacionamento entre as camadas **Controller → Service → Model / Repository → Banco de Dados**;
- a regra de responsabilidade de cada classe, coerente com a arquitetura trabalhada em aula.

O diagrama usa a sintaxe [Mermaid](https://mermaid.js.org/) — é renderizado automaticamente pelo GitHub ao abrir o arquivo.

## Funcionalidades Implementadas

1. **Calcular valor do boi** – Calcula automaticamente o preço estimado com base no peso (kg) e valor da arroba na praça.
2. **Cadastrar avaliação** – Salva uma nova avaliação de boi no banco de dados, com cálculo automático do preço.
3. **Listar avaliações** – Exibe todas as avaliações de bois cadastradas no sistema.
4. **Consultar avaliação** – Exibe os detalhes de uma avaliação específica pelo ID.
5. **Editar avaliação** – Altera nome, peso, raça, categoria, idade ou valor da arroba e recalcula o preço automaticamente.
6. **Excluir avaliação** – Remove uma avaliação do banco de dados.
7. **Filtrar por raça** – Encontra avaliações de determinada raça (busca parcial, case-insensitive).
8. **Filtrar por categoria** – Filtra avaliações por categoria (ex: Boi Gordo, Novilho, Garrote).
9. **Filtrar por faixa de peso** – Filtra avaliações dentro de uma faixa de peso específica (peso mínimo e/ou máximo).
10. **Gerar resumo das avaliações** – Gera estatísticas gerais: total de avaliações, peso médio, valor médio da arroba, preço médio, menor/maior preço, e totais por categoria e raça.
11. **Buscar avaliação pelo nome** – Localiza avaliações utilizando o nome cadastrado do animal (busca parcial, case-insensitive).
12. **Filtrar por preço mínimo** – Apresenta avaliações cujo preço estimado é igual ou superior ao valor informado.
13. **Filtrar por preço máximo** – Apresenta avaliações cujo preço estimado é igual ou inferior ao valor informado.
14. **Filtrar por data de cadastro** – Consulta avaliações realizadas em um determinado período (data inicial e/ou final).
15. **Mostrar avaliações recentes** – Exibe primeiro as avaliações cadastradas mais recentemente, com limite opcional.
16. **Paginar os resultados** – Divide a listagem em páginas para navegar entre grandes quantidades de registros.
17. **Validar campos obrigatórios** – Verifica se os campos necessários foram preenchidos corretamente antes de cadastrar ou atualizar uma avaliação, retornando mensagens de erro claras.
18. **Ordenar por preço crescente** – Exibe as avaliações começando pelo menor preço estimado.
19. **Ordenar por preço decrescente** – Exibe as avaliações começando pelo maior preço estimado.
20. **Ordenar por peso** – Organiza os animais do mais leve ao mais pesado, ou vice-versa (parâmetro `direcao=asc|desc`).

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

Para usar MySQL, edite o `.env`:

```text
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/agrologic
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
| GET | `/` | Lista todas as rotas disponíveis |
| POST | `/bois/calcular` | Calcula o preço estimado sem salvar |
| POST | `/bois` | Cadastra um boi e calcula o preço estimado |
| GET | `/bois` | Lista todos os bois cadastrados |
| GET | `/bois/<id>` | Busca um boi pelo id |
| PUT | `/bois/<id>` | Atualiza um boi e recalcula o preço |
| DELETE | `/bois/<id>` | Remove um boi |
| GET | `/bois/filtrar/raca?raca=...` | Filtra por raça |
| GET | `/bois/filtrar/categoria?categoria=...` | Filtra por categoria |
| GET | `/bois/filtrar/peso?peso_min=...&peso_max=...` | Filtra por faixa de peso |
| GET | `/bois/buscar?nome=...` | Busca avaliações pelo nome do animal |
| GET | `/bois/filtrar/preco-minimo?preco_min=...` | Filtra por preço estimado mínimo |
| GET | `/bois/filtrar/preco-maximo?preco_max=...` | Filtra por preço estimado máximo |
| GET | `/bois/filtrar/data?data_inicio=...&data_fim=...` | Filtra por período de data de cadastro |
| GET | `/bois/recentes?limite=...` | Lista as avaliações mais recentes primeiro |
| GET | `/bois/paginar?pagina=...&por_pagina=...` | Pagina os resultados da listagem |
| GET | `/bois/ordenar/preco-crescente` | Ordena do menor para o maior preço |
| GET | `/bois/ordenar/preco-decrescente` | Ordena do maior para o menor preço |
| GET | `/bois/ordenar/peso?direcao=asc\|desc` | Ordena do mais leve ao mais pesado (ou vice-versa) |
| GET | `/bois/resumo` | Gera resumo estatístico das avaliações |

## Exemplos de Requisições

### Calcular valor (sem salvar)

```json
POST /bois/calcular
{
  "peso_kg": 480,
  "valor_arroba": 300.00
}
```

### Cadastrar avaliação

```json
POST /bois
{
  "nome": "Boi 01",
  "raca": "Nelore",
  "categoria": "Boi Gordo",
  "peso_kg": 480,
  "idade_meses": 36,
  "valor_arroba": 300.00
}
```

### Filtrar por raça

```text
GET /bois/filtrar/raca?raca=Nelore
```

### Filtrar por categoria

```text
GET /bois/filtrar/categoria?categoria=Boi+Gordo
```

### Filtrar por faixa de peso

```text
GET /bois/filtrar/peso?peso_min=400&peso_max=500
```

### Gerar resumo

```text
GET /bois/resumo
```

## Respostas Esperadas

### Cadastrar/Listar/Consultar boi

```json
{
  "id": 1,
  "nome": "Boi 01",
  "raca": "Nelore",
  "categoria": "Boi Gordo",
  "peso_kg": 480,
  "idade_meses": 36,
  "valor_arroba": 300.0,
  "preco_estimado": 9600.0,
  "data_avaliacao": "2026-08-21T12:00:00"
}
```

### Filtrar por raça

```json
{
  "total": 1,
  "filtro": {"raca": "Nelore"},
  "resultados": [
    {
      "id": 1,
      "nome": "Boi 01",
      "raca": "Nelore",
      "categoria": "Boi Gordo",
      "peso_kg": 480,
      "idade_meses": 36,
      "valor_arroba": 300.0,
      "preco_estimado": 9600.0,
      "data_avaliacao": "2026-08-21T12:00:00"
    }
  ]
}
```

### Resumo das avaliações

```json
{
  "total_avaliacoes": 5,
  "peso_medio": 420.5,
  "valor_arroba_medio": 295.0,
  "preco_medio": 8280.0,
  "menor_preco": 5200.0,
  "maior_preco": 11200.0,
  "valor_total": 41400.0,
  "por_categoria": [
    {
      "categoria": "Boi Gordo",
      "quantidade": 3,
      "peso_medio": 480.0,
      "preco_medio": 9600.0
    }
  ],
  "por_raca": [
    {
      "raca": "Nelore",
      "quantidade": 3,
      "peso_medio": 450.0,
      "preco_medio": 9000.0
    }
  ]
}
```

## Como executar o frontend

Entre na pasta do frontend:

```bash
cd frontend
```

Instale as dependências (precisa ter o [Node.js](https://nodejs.org) instalado):

```bash
npm install
```

Execute o servidor de desenvolvimento:

```bash
npm run dev
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

> O backend precisa estar rodando (`python app.py` em outro terminal) para o frontend funcionar.

## Como publicar o site (GitHub Pages)

O site estático publicado fica na pasta `agrologic-pages/` (cópia do `frontend/`, com o `base` do Vite ajustado para `/AgrologicVersaoATUAL/`).

A cada push na branch `main`, o workflow [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) instala as dependências, gera o build (`npm run build`) e publica o site automaticamente no GitHub Pages.

Endereço do site: `https://heitoralvescardoso.github.io/AgrologicVersaoATUAL/`

Na primeira publicação, é preciso ativar o Pages no repositório: **Settings → Pages → Source: GitHub Actions**.

> O GitHub Pages hospeda apenas o site estático. O frontend usa caminhos de API relativos (`/bois/...`) e, em desenvolvimento, o Vite os encaminha via proxy para o backend em `http://127.0.0.1:5000`. No Pages não existe esse proxy, então a interface carrega, mas os dados só aparecem com o backend hospedado — nesse caso, ajuste a `API_URL` em `agrologic-pages/app.js` para o endereço da API na nuvem.

## Status do projeto

Projeto completo com backend (Flask) e frontend (Vite + vanilla JS). O backend expõe 19 rotas REST e o frontend consome todas elas, oferecendo dashboard, calculadora, CRUD de avaliações, filtros, pesquisa, paginação, ordenações e resumo estatístico. O site estático é publicado automaticamente no GitHub Pages a cada push na branch `main`.
