---
aliases:
  - JavasScript Object Notation
---
JSON é uma extensão de arquivo surgido no inicio dos anos 2000 para resolver um problema de web, numa época onde páginas web eram estáticas se você quisesse uma informação nova tinha que recarregar a página inteira que numa época onde a internet era lerda se tornava uma tortura de ficar refazendo o tempo inteiro.

Nesse tempo o antigo padrão era de arquivos XLM(eXtensible Markup Language) que eram extremamente carregados de informação pra poder funcionar, isso tornava ele lento de carregar e pesado de transportar ex:

```
<livraria>
  <livro categoria="ficcao">
    <titulo>Dom Casmurro</titulo>
    <autor>Machado de Assis</autor>
    <ano>1899</ano>
    <preco>29.90</preco>
  </livro>
</livraria>
```

O excesso de marcações deixava um arquivo pesado e a obrigatoriedade de abrir e fechar todas as etiquetas era peso a mais.

Daí veio a ideia de que talvez pudesse ser usado algo interno do próprio Javascript pra resolver isso, assim eliminando a necessidade de um [[Parser]] externo ser instalado pra conseguir resolver isso o próprio Javascript já consegue traduzir extremamente rápido a informação

O JSON segue a ideia de Chave -> Valor com algumas regras como lista sendo dentro de [] e objetos dentro de {} e que nomes tem que estar dentro de "" e os valores são separados por ,

exemplo:

```
{
  "nome": "Ana Silva",
  "idade": 28,
  "esta_logada": true,
  "habilidades": ["Python", "Design", "Gestão"],
  "endereco": {
    "cidade": "São Paulo",
    "estado": "SP"
  }
}
```

