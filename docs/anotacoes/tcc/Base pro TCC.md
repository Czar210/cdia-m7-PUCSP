## 1. Elementos Pré-Textuais

* **Capa e Folha de Rosto:** Nomes (Andre, César e Enzo), Título e Instituição.
    
* **Resumo/Abstract:** Onde vocês vendem o peixe: "Detecção de fake news via topologia de rede no Bluesky utilizando GCNs".
    
* **Listas:** Figuras, Tabelas e Siglas (GNN, GCN, AT Proto, NLP, etc.).
    

---

## 2. Capítulo 1: Introdução

* **1.1 Contextualização:** A saturação do NLP tradicional e o surgimento das IAs generativas que mimetizam o estilo humano de escrita.
    
* **1.2 O Problema do Cold Start:** Como classificar notícias em redes sociais novas (Bluesky) onde não há histórico consolidado.
    
* **1.3 Objetivos:** Migrar do "o que foi dito" (texto) para "quem disse e como se espalhou" (grafo).
    
* **1.4 Justificativa:** A relevância social de combater desinformação em novas infraestruturas descentralizadas.
    

---

## 3. Capítulo 2: Fundamentação Teórica

* **2.1 Processamento de Linguagem Natural (NLP):**
    
    * Explique _Word Embeddings_ e Transformers.
        
    * Equação de similaridade de cosseno para vetores: $S_c(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$.
        
* **2.2 Teoria de Grafos:** Definição formal de $G = (V, E)$, onde $V$ são usuários e $E$ as interações (reposts/likes).
    
* **2.3 Graph Neural Networks (GNN):** * O conceito de _Message Passing_.
    
    * A regra de atualização da GCN:
        
        $$H^{(l+1)} = \sigma \left( \tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}} H^{(l)} W^{(l)} \right)$$
        
    * Explique o papel da matriz de adjacência $\tilde{A}$ e dos pesos $W$.
        

---

## 4. Capítulo 3: Metodologia

* **3.1 Coleta de Dados e AT Protocol:** Como vocês consumiram o _firehose_ do Bluesky.
    
* **3.2 Engenharia de Atributos:** Uso do `sentence-transformers` para gerar os atributos iniciais dos nós.
    
* **3.3 Arquitetura do Sistema:** * **Pipeline de Dados:** Extração (`atproto`) → Processamento (`networkx`) → Treinamento (`PyTorch Geometric`).
    
    * **Interface:** Backend em FastAPI e Frontend em React/Next.js.
        
* **3.4 O Modelo Proposto:** Detalhe as 3 camadas de `GCNConv` e o `Global Mean Pooling`.
    

---

## 5. Capítulo 4: Resultados e Discussão

* **4.1 Configuração Experimental:** _Datasets_ utilizados (UPFD/PolitiFact + Dados Reais Bluesky).
    
* **4.2 Análise Comparativa (Duelo):** Comparação de acurácia entre modelos puramente textuais e modelos baseados em grafos.
    
* **4.3 Estudo de Ablação:** "O que acontece se eu tirar a estrutura do grafo?".
    
* **4.4 Visualização de Clusters:** Analisar o arquivo `resultado_final_clusters.png` para discutir a formação de câmaras de eco.
    

---

## 6. Capítulo 5: Conclusão

* **5.1 Considerações Finais:** Retomada dos objetivos.
    
* **5.2 Limitações:** Dificuldade de rotulagem em tempo real e custos computacionais de grafos gigantes.
    
* **5.3 Trabalhos Futuros:** Implementação de GAT (Graph Attention Networks) para pesos dinâmicos nas arestas.