# Roteiro da apresentação — AgroLogic (7 minutos)

> Guia para consultar na hora. Fala curta, explicação simples. Tempo total: 7 min (demo até 2 min).

---

## 1. O projeto em 3 frases (decore isto)

1. O **AgroLogic** é um sistema para o produtor rural avaliar o preço do gado.
2. Ele calcula o valor do animal a partir do **peso** e do **valor da arroba** e guarda essas avaliações num banco de dados.
3. O produtor usa isso para **negociar com referência de preço**, em vez de vender "no escuro".

---

## 2. Glossário rápido (para entender o que você vai falar)

| Termo | Em palavras simples |
|---|---|
| **API** | O "cérebro" do sistema que roda no servidor. O site pede, a API responde. |
| **Rota** | Um endereço da API. Ex.: `GET /bois` = "me devolva a lista de bois". |
| **JSON** | O formato de texto em que os dados viajam entre o site e a API. |
| **Camada** | Cada "setor" do código com uma função. Aqui são 4: controller, service, repository, model. |
| **Controller** | Recebe o pedido que chega pela internet (o garçom). |
| **Service** | Onde ficam as regras: validar, calcular, decidir (a cozinha). |
| **Repository** | Quem faz as consultas mais elaboradas no banco (o estoquista). |
| **Model** | A ficha do animal + o básico de salvar, editar e apagar no banco. |
| **ORM** | Um tradutor: você mexe com objetos Python e ele gera o SQL sozinho. |
| **SQL** | A linguagem de consulta do banco (`SELECT`, `WHERE`, `ORDER BY`). |
| **Blueprint** | Um jeito do Flask agrupar as rotas num arquivo só. |
| **CORS** | Permissão para o site (porta 5173) conversar com a API (porta 5000). |

---

## 3. Roteiro com tempo (o que falar em cada bloco)

### 3.1 Abertura — 20 segundos
> "Somos [nomes], turma [X]. Nosso projeto é o AgroLogic. Ele atende produtores rurais de médio porte e resolve um problema simples: a falta de referência de preço na hora de vender o gado."

### 3.2 Problema, público e casos de uso — 55 segundos
> "Hoje o produtor negocia com o comprador da região sem saber o preço de mercado, então muitas vezes vende abaixo do valor. O AgroLogic dá essa referência: ele calcula o preço pelo peso e pelo valor da arroba e guarda o histórico."

Mostre as telas e diga só o objetivo de cada caso de uso:

| Caso de uso | Tela | Para que serve |
|---|---|---|
| Estimar o preço | Calcular | saber quanto vale o animal antes de vender |
| Registrar a avaliação | Calcular → "Salvar" | guardar o histórico |
| Consultar e filtrar | Avaliações | achar animais por raça, peso, preço, nome ou data |
| Comparar resultados | Avaliações | ordenar por preço/peso e passar de página |
| Acompanhar o rebanho | Resumo | ver médias, maior e menor preço, totais por categoria |

### 3.3 Diagrama de classes — 35 segundos
Abra `docs/diagrama-de-classes.md`.

> "O sistema tem uma entidade principal: **Boi**. Ela herda de `db.Model`, que é o recurso do SQLAlchemy que liga a classe à tabela do banco. Os atributos são: id, nome, raça, categoria, peso, idade, valor da arroba, preço estimado e data da avaliação. O preço estimado não é digitado: ele é calculado pela regra de negócio. Como o domínio tem uma entidade só, não existem relacionamentos entre entidades — o que existe é a ligação entre as camadas."

### 3.4 Os dois fluxos — 55 segundos

**Fluxo de entrada (cadastrar uma avaliação) — `POST /bois`**

1. O site manda os dados em JSON.
2. O **Controller** recebe (`criar_boi`).
3. O **Service** valida: campos obrigatórios, números positivos.
4. O **Service de cálculo** faz `preço = (peso ÷ 15) × valor da arroba`.
5. A **Model** salva no banco (ORM → `INSERT`).
6. A API responde com o registro criado.

**Fluxo de recuperação (consultar) — `GET /bois/filtrar/peso`**

1. O Controller recebe o filtro da URL.
2. Chama o **Service**, que chama o **Repository**.
3. O Repository monta o **SQL** (`WHERE`, `ORDER BY`, `LIMIT`) e executa com parâmetros seguros.
4. O banco devolve os dados e o SQLAlchemy transforma em objetos `Boi`.
5. O Service converte em dicionário e a API devolve em JSON.

> Frase para fechar: "Repare que o Controller só recebe e responde. A regra de negócio nunca fica nele."

### 3.5 Arquitetura — 1 minuto

> "O código é separado em quatro pastas, cada uma com uma responsabilidade:
> `controllers/` conversa com a internet, `services/` tem as regras (uma classe por caso de uso, 19 no total), `repositories/` tem as consultas em SQL e `models/` tem a entidade e o CRUD com ORM.
> Além disso, o frontend e a API são separados: o site roda na porta 5173 e a API na 5000, conversando por JSON."

### 3.6 Demonstração — até 2 minutos
Veja a seção 5. Não diga nada demais: aponte a tela e o resultado.

### 3.7 Persistência e consultas — 35 segundos

> "O cadastro, a edição e a exclusão usam ORM: a Model chama `db.session` e faz o commit. As consultas mais elaboradas — filtros, ordenação, paginação e o resumo estatístico — ficam no Repository em SQL explícito, com parâmetros vinculados, que é o que evita SQL Injection."

### 3.8 Tecnologias e README — 30 segundos

> "No backend: Python com Flask, Flask-SQLAlchemy, Flask-CORS e PyMySQL, com banco MySQL (ou SQLite para testes). No frontend: React com Vite, além de um painel em JavaScript publicado no GitHub Pages por GitHub Actions. O README documenta as 20 funcionalidades e todas as rotas."

**Sobre os bônus da rubrica (fale com sinceridade):** o único bônus que se aplica é o *frontend hospedado* (GitHub Pages). Não há IA integrada e não há consentimento registrado de verdade — a tela de conta é só visual. Não apresente isso como bônus.

### 3.9 Encerramento — 10 segundos
> "O AgroLogic dá ao produtor uma referência de preço confiável para negociar melhor. Obrigado."

---

## 4. O diagrama em linguagem simples

Pense em três "andares":

- **Andar de cima (Controller):** atende o pedido que chega. Não decide nada.
- **Andar do meio (Service + Repository):** o Service decide e calcula; o Repository busca os dados com SQL.
- **Andar de baixo (Model + Banco):** a Model é a ficha do boi e sabe se salvar; o Banco guarda tudo.

Regra de ouro para responder qualquer pergunta: **"quem decide é o Service, quem busca é o Repository, quem guarda é a Model/banco, quem só atende é o Controller."**

---

## 5. Demonstração: clique a clique (até 2 min)

Antes de apresentar, deixe tudo rodando:

```bash
# terminal 1 — ligue o MySQL do WAMP e rode:
cd backend
python app.py

# terminal 2:
cd agrologic-pages
npm run dev
```

Abra: **http://127.0.0.1:5173/AgrologicVersaoATUAL/**

Demonstre **4 funcionalidades que não são CRUD** (como a rubrica pede):

1. **Cálculo do preço** (25s) — aba *Calcular*: peso 480, arroba 300 → **R$ 9.600,00**.
   Fale: "1 arroba = 15 kg; o backend calcula e devolve sem gravar."
2. **Resumo estatístico** (25s) — aba *Resumo*: total, peso médio, menor e maior preço, totais por categoria.
   Fale: "isso vem de `AVG`, `SUM` e `GROUP BY` no Repository."
3. **Filtro por faixa de peso** (30s) — aba *Avaliações*: peso mínimo 400 → só os animais acima disso.
4. **Ordenação + paginação** (30s) — mesma aba: ordenar por preço crescente/decrescente e trocar "por página" ou usar Anterior/Próxima.
   Fale: "`ORDER BY` e `LIMIT/OFFSET` estão no Repository."

Não perca tempo cadastrando/editando/excluindo: a rubrica não considera CRUD isolado.

### Se quiser mostrar filtro por data
Todos os registros novos ficam com a data de hoje. Para ter datas diferentes, rode no banco antes:

```sql
-- MySQL
UPDATE bois SET data_avaliacao = DATE_SUB(NOW(), INTERVAL id*5 DAY);
```

---

## 6. ORM e SQL: como explicar em 20 segundos

- **Escrever no banco (cadastrar, editar, excluir):** uso **ORM**. Eu chamo `boi.salvar()` e o SQLAlchemy monta o `INSERT`; chamo `atualizar()` e ele monta o `UPDATE`.
- **Ler com filtros e contas (relatórios):** uso **SQL puro** no Repository, porque fica claro o que a consulta faz (filtro opcional, ordenação, paginação, `GROUP BY`).
- **Segurança:** os valores entram como **parâmetros** (`:peso_min`), nunca grudados no texto da consulta. É isso que impede SQL Injection.

Arquivos para abrir se o professor pedir prova:
`backend/controllers/boi_controller.py` (rotas) · `backend/services/` (regras) · `backend/repositories/boi_repository.py` (SQL) · `backend/models/boi_model.py` (entidade e CRUD) · `backend/database/create_database.sql` (tabela).

---

## 7. Perguntas prováveis (respostas curtas)

1. **Por que SQL puro se já existe ORM?** Foi requisito da disciplina e dá controle explícito de `GROUP BY`, `LIMIT/OFFSET` e filtros opcionais.
2. **Como você evita SQL Injection?** Uso parâmetros vinculados; só a direção `ASC/DESC` é interpolada, depois de validada.
3. **Onde fica a regra de negócio?** Nos Services: validação, fórmula do preço, arredondamento e limites da paginação.
4. **Por que 19 Services?** Um caso de uso por classe, então cada rota tem uma responsabilidade clara.
5. **Por que não tem relacionamento no diagrama?** Porque só existe uma entidade, `Boi`, sem chave estrangeira.
6. **Como o site conversa com a API?** Por requisições JSON; o CORS libera o acesso e, em desenvolvimento, o Vite faz proxy de `/bois` para a porta 5000.
7. **Como o banco é criado?** Com `db.create_all()` no start, ou pelo `create_database.sql` no MySQL; a URL vem do arquivo `.env`.
8. **O que acontece com dados inválidos?** O Service barra e a API responde 400; id inexistente dá 404; erro de banco dá 500 com rollback.
9. **Como você testou o cálculo?** 480 kg ÷ 15 = 32 arrobas × R$ 300 = R$ 9.600,00, conferido também com outros valores.
10. **O que é um Blueprint?** O agrupador de rotas do Flask usado pelo Controller.

---

## 8. Checklist do dia e armadilhas

- [ ] Ligar o MySQL do WAMP **antes** (ou usar `DATABASE_URL="sqlite:///agrologic.db"`).
- [ ] Deixar uns 6 registros variados no banco (raças, categorias e pesos diferentes).
- [ ] Abrir a apresentação e o navegador já na tela inicial do painel.
- [ ] Testar uma vez o cálculo e o resumo antes de entrar.
- [ ] Levar o roteiro impresso ou no celular.
- [ ] Cronometrar: 7 min no total, 2 min de demo.

**Armadilhas:**

- **Não demonstre pelo link do GitHub Pages.** Lá o site é só estático: a tela abre, mas as chamadas `/bois` não têm backend e os dados não aparecem. Demonstre no seu computador.
- **Não prometa login.** A tela de conta é apenas visual, sem autenticação implementada.
- **Não invente bônus.** Sem IA, sem consentimento registrado.
- Se o professor perguntar de algo que você não lembra, responda: "essa parte está na camada X, posso mostrar no código" e abra o arquivo.

---

## 9. Versão ultra-resumida (para colar no celular)

1. **Problema:** produtor vende sem referência de preço.
2. **Solução:** calcula o preço pelo peso e pela arroba e guarda o histórico.
3. **Domínio:** uma entidade, `Boi`, que herda de `db.Model`.
4. **Fluxo:** site → Controller → Service → Repository/Model → banco.
5. **Arquitetura:** 4 camadas, cada uma com uma responsabilidade; frontend separado da API.
6. **Persistência:** ORM no CRUD, SQL no Repository, parâmetros contra SQL Injection.
7. **Demo:** cálculo, resumo, filtro por peso, ordenação e paginação.
8. **Encerramento:** referência de preço para negociar melhor.
