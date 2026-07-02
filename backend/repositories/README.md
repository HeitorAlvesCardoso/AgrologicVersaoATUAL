# Repositories

Nesta arquitetura, o CRUD simples fica dentro das Models que herdam de `db.Model`.

A pasta `repositories` foi mantida porque faz parte da estrutura esperada do projeto. Ela deve ser usada quando for necessário criar consultas que não sejam CRUD básico, por exemplo:

- relatórios de preços por período;
- filtros por raça, categoria ou faixa de peso;
- consultas envolvendo várias tabelas;
- rankings de valorização do gado;
- buscas específicas do negócio (ex: histórico de cotações da arroba).
