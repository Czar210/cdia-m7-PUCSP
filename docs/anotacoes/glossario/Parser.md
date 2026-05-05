---
aliases:
  * Analisador Sintático
---
Um componente de software que pega dados de entrada e transforma esses dados numa outra estrutura de dados organizada.

Geralmente divido em duas etapas 

1. Scanning: Ler o código e quebrar ele em pequenas partes (tokens)
2. Parsing: Passar por esses tokens verificar se eles respeitam as regras da linguagem para qual eles vão ser traduzidos e se estiver tudo certo ele gera uma AST (Árvore de Sintaxe Abstrata)

Eles são usados por exemplo para transformar linguagem de código em linguagem de maquina para que o computador possa executar, ou pra transformar o código de HTML no DOM que fica na página renderizada da web ou pro sistema ler os dados de um arquivo XML ou [[JSON]] e obviament em PLN
