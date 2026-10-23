# Diagrama de Classes — AgroLogic

Diagrama do domínio do sistema, coerente com as Models implementadas em
`backend/models/` e com a arquitetura Controller → Service → Model/Repository
trabalhada na disciplina.

## 1. Domínio (entidades do banco)

```mermaid
classDiagram
    class Base {
        <<abstract Flask-SQLAlchemy db.Model>>
    }

    class Boi {
        <<tabela bois>>
        +Integer id
        +String(100) nome
        +String(100) raca
        +String(50) categoria
        +Float peso_kg
        +Integer idade_meses
        +Float valor_arroba
        +Float preco_estimado
        +DateTime data_avaliacao
        +salvar() void
        +atualizar(nome, raca, categoria, peso_kg, idade_meses, valor_arroba, preco_estimado) void
        +deletar() void
        +listar_todos() list~Boi~
        +buscar_por_id(boi_id) Boi
        +to_dict() dict
    }

    Base <|-- Boi : herda (db.Model)
```

**Notas sobre a entidade `Boi`:**

- **Herança:** `Boi` herda de `db.Model` (Flask-SQLAlchemy), exigência do enunciado
  para CRUD convencional. A classe pai `Base` representa essa classe-mãe do framework.
- **Persistência:** operações básicas (`salvar`, `atualizar`, `deletar`,
  `listar_todos`, `buscar_por_id`) estão na própria Model.
- **Atributo derivado:** `preco_estimado` não é digitado pelo usuário — é calculado
  pelo `CalcularValorBoiService` (`(peso_kg / 15) * valor_arroba`) e persistido junto.
- **Relacionamento:** o sistema possui uma única entidade de domínio (`Boi`), portanto
  não há associação, agregação ou composição entre entidades próprias do projeto.

## 2. Camadas do sistema (como as classes se relacionam)

```mermaid
classDiagram
    class BoiController {
        <<Blueprint Flask /bois>>
        +calcular_valor_boi()
        +criar_boi()
        +listar_bois()
        +buscar_boi_por_id()
        +atualizar_boi()
        +deletar_boi()
        +filtrar_*()
        +buscar_por_nome()
        +filtrar_por_preco_*()
        +filtrar_por_data()
        +listar_recentes()
        +paginar_bois()
        +ordenar_*()
        +gerar_resumo()
    }

    class Service~17 classes~ {
        <<um Service por caso de uso>>
        +executar(...)
    }

    class Boi {
        <<Model — CRUD>>
        +salvar()
        +atualizar()
        +deletar()
        +listar_todos()
        +buscar_por_id()
    }

    class BoiRepository {
        <<consultas especiais>>
        +filtrar_por_raca()
        +filtrar_por_categoria()
        +filtrar_por_faixa_de_peso()
        +buscar_por_nome()
        +filtrar_por_preco_minimo()
        +filtrar_por_preco_maximo()
        +filtrar_por_periodo()
        +listar_recentes()
        +paginar()
        +ordenar_por_preco_crescente()
        +ordenar_por_preco_decrescente()
        +ordenar_por_peso()
        +gerar_resumo()
    }

    class BancoDeDados {
        <<tabela bois>>
    }

    BoiController --> Service : chama (sem regra de negócio)
    Service --> Boi : CRUD simples
    Service --> BoiRepository : filtros, ordenações, relatórios
    Boi --> BancoDeDados : persistência
    BoiRepository --> BancoDeDados : SQL / aggregates
```

**Regras de responsabilidade (conforme o material da disciplina):**

| Classe | Responsabilidade |
|---|---|
| `BoiController` | Recebe a requisição HTTP, interpreta os dados e devolve a resposta. **Não** contém regra de negócio. |
| `Service` (17 classes) | Um caso de uso por classe: valida, coordena e chama a Model ou o Repository. |
| `Boi` (Model) | Representa a entidade do domínio e concentra o CRUD básico. |
| `BoiRepository` | Somente consultas especiais: filtros, ordenações, paginação e agregações. Não repete CRUD. |
