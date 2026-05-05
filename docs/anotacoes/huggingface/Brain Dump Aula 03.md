
#Machine_Learning

## Parâmetros importantes

* n_samples : Quantidade de linhas
* n_features : Quantidade de Features
* n_informative : Features que realmente importam para a predição
* n_redundant : Features correlacionadas com as informativas
* class_sep : O quão separáveis são as classes
* weights : Proporção de Cada Classe
* random_state : Seed aleatória

## O perigo de dados muitos simples

Dados muito separáveis conseguem facilmente valores de acerto muito muito altos exemplo se você tiver só  3 features num modelo de adivinhar se o aluno passou ou não passou sendo essas 3 features 

* Horas de Estudo
* Horas de Sono
* Bananeiras Plantadas

Ele vai acabar percebendo que horas de Sono e de Estudo afetam fortemente a diferença entre 0 reprovado e 1 aprovado, e a separação vai ficar alta pois quem estuda no geral passa, quem dorme também, se você faz um e não outro talvez crie um pouco de sobreposição e possibilidade de passar ou não mas vai ser isso.

Um problema realista vai ter valores entre 0.8 e 1.5 em class_sep, mais que isso é um problema muito fácil, menos que isso um problema muito complexo e difícil de resolver