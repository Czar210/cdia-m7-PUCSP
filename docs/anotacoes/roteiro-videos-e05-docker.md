# Roteiros de vídeo — Série e05 (Docker) · Bella Tavola

Material de apoio para gravar 3 vídeos (um por caderno). Cada seção tem:
1. **Roteiro** — o que falar e o que mostrar na tela.
2. **Comandos ao vivo** — cheat sheet copy-paste da versão final (testado neste repo).
3. **Perguntas & respostas pra ensinar** — as reflexões dos exercícios, com respostas curtas.

> Repo real: `Czar210/cdia-m7-PUCSP` · Imagem no Docker Hub: `zaras210/bella-tavola`
> A API vive na pasta `api/` (por isso o build é `./api`). Python 3.12.

---

## ⚙️ Antes de gravar (setup comum)

```powershell
# 1. Docker Desktop ligado (confirma o Server)
docker info | Select-Object -First 6

# 2. Estar na raiz do projeto
cd "$HOME\Documents\GitHub\cdia-m7-PUCSP"   # ajuste se necessário

# 3. Ambiente limpo (pro vídeo 1 mostrar o build do zero)
docker rm -f bella-test 2>$null
docker rmi bella-tavola:v1 2>$null

# 4. 1 terminal basta — subimos os contêineres com -d (background), então a janela fica livre.
#    (Um 2º terminal só é necessário se você rodar SEM -d, em foreground.)
```

> 💡 **Shell:** você grava no **PowerShell** (terminal padrão do VS Code). Três ajustes pra nada quebrar ao vivo:
> - Use **`curl.exe`** (com `.exe`) — senão o PowerShell chama o `Invoke-WebRequest`, que tem outra sintaxe. (Ou abra as rotas GET no navegador.)
> - Para rodar dois comandos na mesma linha, use **`;`** — o PowerShell 5.1 **não** aceita `&&`.
> - **Não** existe `grep` no PowerShell; use `Select-String` (ou só leia a saída).
> - `docker` e `gh` são idênticos em qualquer shell.
>
> 💡 Para demonstrar `/ml/predict` **sem depender do token do Hub** (mais confiável na gravação), monte a pasta do modelo e aponte o `MODEL_PATH` — comando pronto e testado no Vídeo 2.

---

## 📂 Mapa de arquivos pra mostrar na tela (por vídeo)

> Todos os caminhos partem da **raiz** do projeto: `cdia-m7-PUCSP\`.
> No VS Code: `Ctrl+P` e cole o caminho pra abrir rapidinho na hora da gravação.
> ⚠️ Atenção a uma pegadinha: o **build é `./api`**, então o `Dockerfile`, o `.dockerignore` e o `requirements.txt` que importam pra imagem ficam **dentro de `api\`** — não na raiz. Já o `docker-compose.yml` e o `nginx.conf` ficam **na raiz**.

**🎬 Vídeo 1 — Dockerfile**
| Mostrar na tela | Caminho | O que apontar |
|---|---|---|
| Dockerfile da API | `api\Dockerfile` | ordem `requirements` → código (cache); `--host 0.0.0.0` no CMD |
| Código da API | `api\main.py` | editar a mensagem da rota `/` pra demonstrar o cache do build |
| Dependências | `api\requirements.txt` | é o arquivo que "trava" a camada do `pip install` |

**🎬 Vídeo 2 — Compose + boas práticas**
| Mostrar na tela | Caminho | O que apontar |
|---|---|---|
| Orquestração | `docker-compose.yml` *(raiz)* | 3 serviços: `api`, `db`, `nginx`; `depends_on` + `healthcheck` |
| Proxy reverso | `nginx.conf` *(raiz)* | `proxy_pass` apontando pra `api:8000` (nome do serviço, não localhost) |
| Exclusões do build | `api\.dockerignore` | `.env`, testes e `.pkl` **fora** da imagem |
| Boas práticas | `api\Dockerfile` | multi-stage (`builder`); `USER appuser` **depois** do `pip install` |
| Modelo (montado) | `datagen\models\credit_rf.pkl` | é a pasta que você monta com `-v` no `/ml/predict` |
| Secrets locais | `api\.env` | citar que existe, mas **não abrir** na tela (tem segredo); está no `.gitignore` e `.dockerignore` |

**🎬 Vídeo 3 — CI + Docker Hub**
| Mostrar na tela | Caminho | O que apontar |
|---|---|---|
| Pipeline de CI | `.github\workflows\ci.yml` | o job `docker`: `needs: integracao`, `login-action`, `build-push-action`, as 2 tags |
| Secrets (no site) | GitHub → **Settings → Secrets and variables → Actions** | `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `HF_TOKEN` (valores ocultos) |
| Pipeline rodando | GitHub → aba **Actions** | os 4 jobs verdes em sequência |
| Imagem publicada | `hub.docker.com/r/zaras210/bella-tavola/tags` | as tags `latest` e o SHA do commit |

---

# 🎬 Vídeo 1 — e05-p01: Primeira imagem e o Dockerfile da API
**Duração alvo: ~6–7 min**

## Roteiro

**Abertura (~30s)**
> "Neste vídeo eu containerizo a API Bella Tavola. Na Semana 3 meu CI já estava verde, mas a API só rodava 'na minha máquina'. Aqui eu empacoto ela numa imagem Docker que roda igual em qualquer lugar."

**Por que Docker, e não só venv (~1min30)**
> "Eu já usava ambiente virtual, mas o venv isola só os **pacotes Python**. Ele não isola a versão do Python, nem as bibliotecas de sistema — o scikit-learn, por exemplo, é compilado contra a `libgomp` do sistema. O contêiner isola **tudo**: SO, binários, variáveis de ambiente e rede."
>
> "A distinção central é **imagem vs contêiner**: a imagem é a receita imutável; o contêiner é a receita em execução. É como classe e objeto — de uma imagem eu subo vários contêineres."

🖥️ Tela: `docker --version`

**O Dockerfile (~2min)** — abrir `api/Dockerfile`
> "`FROM python:3.12-slim` — base mínima, mesma versão do meu CI. Não uso Alpine porque numpy e scikit-learn quebram nele (explico no fim)."
>
> "Repara na **ordem**: copio o `requirements.txt` e instalo as dependências **antes** de copiar o código. Essa é a regra de ouro do cache — enquanto o `requirements.txt` não muda, o Docker reaproveita a camada do `pip install`, que é a parte lenta."
>
> "No `CMD` eu uso `--host 0.0.0.0`. O uvicorn por padrão escuta em 127.0.0.1, que dentro do contêiner é só o próprio contêiner. Pra requisição de fora chegar, ele precisa escutar em todas as interfaces."

**Build e run ao vivo (~2min)** — ver cheat sheet abaixo. Mostrar: build com layers, tamanho (776 MB), `curl /` e `/pratos/`, e o cache em ação.

**Fecho (~30s)**
> "Resumindo: escrevi o Dockerfile, fiz o build, e a API roda num contêiner reproduzível. Mas ficaram dois problemas: o `/ml/predict` precisa do token do Hugging Face, e dado criado no contêiner some quando ele para. É o que eu resolvo no próximo vídeo."

## 🖥️ Comandos ao vivo

```bash
# Build da imagem (contexto = pasta api/)
docker build -t bella-tavola:v1 ./api

# Tamanho da imagem
docker images bella-tavola:v1

# Sobe em background e confirma a porta mapeada
docker run -d -p 8000:8000 --name bella-test bella-tavola:v1

# (mesmo terminal — o contêiner está em -d) a API responde de dentro do contêiner
curl.exe http://localhost:8000/
curl.exe -L http://localhost:8000/pratos/

# Mostrar o cache: edite a mensagem da rota / em api/main.py, salve, e:
docker build -t bella-tavola:v1 ./api
#  -> repare: "CACHED" no pip install; só o COPY do código re-roda

# Demonstrar a Falha B (sem --host) — opcional, didático:
#  edite o CMD do Dockerfile tirando "--host","0.0.0.0", rebuild e veja o curl falhar

# Limpeza
docker stop bella-test; docker rm bella-test
```

## 🎓 Perguntas & respostas pra ensinar

**Qual a diferença entre imagem e contêiner?**
Imagem = definição estática e imutável (o que existe no ambiente), não consome recursos em repouso. Contêiner = imagem em execução, consome CPU/memória. Análogo a classe vs objeto.

**O que um contêiner isola além de um venv?**
O venv isola só pacotes Python. O contêiner isola o SO inteiro, bibliotecas de sistema (libgomp, libssl), binários, variáveis de ambiente, processos, rede e a própria versão do Python.

**Um arquivo criado dentro do contêiner sobrevive ao próximo `run`?**
Não. Cada `docker run` cria um contêiner novo a partir da imagem imutável; o estado é descartado (efemeridade). Por isso dados que importam exigem **volume** (Vídeo 2).

**Por que copiar o `requirements.txt` antes do código?**
Cache de layers. O `pip install` (lento) só re-roda quando o `requirements.txt` muda. Se o código fosse copiado antes, qualquer alteração num `.py` invalidaria o `pip install`.

**Por que `--host 0.0.0.0` é obrigatório no CMD?**
Sem ele, o uvicorn escuta em 127.0.0.1, que dentro do contêiner é só o próprio contêiner. O `-p` mapeia a interface de rede do contêiner, mas o servidor estaria no endereço errado. `0.0.0.0` = todas as interfaces.

**`EXPOSE 8000` abre a porta?**
Não — é documentação. Quem abre/mapeia é o `-p` no `docker run`.

**Depois de buildar `v2` sem a tag `latest`, pra onde aponta `latest`?**
Continua em `v1`. `latest` é só uma tag convencional, não é automática. Por isso, em produção, usa-se o **SHA do commit** como tag (rastreabilidade) — tema do Vídeo 3.

**Por que Alpine falha em projetos de ML?**
Alpine usa `musl libc`, não `glibc`. Os wheels do PyPI (numpy, scikit-learn) são compilados pra glibc; no Alpine o pip tenta compilar do código-fonte, exigindo gcc e headers que a imagem mínima não tem. O ganho de tamanho não compensa — para ML, use `slim`.

---

# 🎬 Vídeo 2 — e05-p02: Variáveis, volumes, Compose e boas práticas
**Duração alvo: ~7–8 min**

## Roteiro

**Abertura (~30s)**
> "Aqui eu pego a imagem do vídeo anterior e resolvo o que ficou em aberto: passo secrets com segurança, persisto dados com volumes, orquestro vários serviços com Docker Compose e refino o Dockerfile com boas práticas de segurança."

**Variáveis de ambiente e secrets (~1min30)**
> "A API precisa do `HF_TOKEN` pra baixar o modelo. A **regra de ouro**: nunca usar `ENV` no Dockerfile pra secret — fica gravado na imagem e aparece em `docker history`. Eu passo em runtime, com `-e` ou `--env-file`. O `.env` nunca é commitado: está no `.gitignore` e no `.dockerignore`."

**Volumes (~1min)**
> "Contêiner é efêmero. Pra dados que importam, uso **volume**: gerenciado pelo Docker, vive independente do contêiner. **Named volume** é pra produção (banco, uploads); **bind mount** espelha uma pasta minha no contêiner, ótimo pra desenvolvimento com `--reload`."

**Docker Compose: API + PostgreSQL + Nginx (~2min30)** — abrir `docker-compose.yml` e `nginx.conf`
> "Em vez de três `docker run` enormes, declaro tudo num arquivo. Três serviços: a `api` (buildada do `./api`), o `db` PostgreSQL, e o `nginx` como proxy reverso na porta 80."
>
> "O ponto que mais confunde: dentro da rede do Compose, cada serviço é acessível **pelo nome**. A API fala com o banco em `db:5432`, o Nginx fala com a API em `api:8000`. Se eu usasse `localhost`, seria o próprio contêiner — não o vizinho."
>
> "E o `healthcheck`: o `depends_on` sozinho só garante que o banco **iniciou**, não que está **pronto**. Com `condition: service_healthy` + `pg_isready`, a API só sobe depois que o Postgres aceita conexões."

🖥️ Subir ao vivo, mostrar `db` healthy → `api`, e o `curl` na porta **80** (via Nginx).

**Boas práticas no Dockerfile (~2min)** — abrir `api/.dockerignore` e `api/Dockerfile`
> "O `.dockerignore` evita copiar pra imagem o `.env` com secrets, testes, cadernos e o `.pkl` (que é baixado em runtime)."
>
> "A API roda como `appuser`, não `root` — princípio do menor privilégio. E o `USER` vem **depois** do `pip install`, porque instalar pacotes exige root."
>
> "É **multi-stage**: o estágio `builder` instala as dependências com os compiladores; o estágio final copia só os pacotes prontos. Por isso a imagem caiu pra 776 MB."

**Fecho (~30s)**
> "Agora a imagem é segura, enxuta e orquestrada. Mas ela ainda só existe na minha máquina. No próximo vídeo ela entra no CI e é publicada automaticamente."

## 🖥️ Comandos ao vivo

```bash
# --- Compose: sobe API + PostgreSQL + Nginx ---
docker compose up -d
docker compose ps                 # db = healthy; api sobe depois

# (mesmo terminal) testa VIA NGINX, na porta 80 (sem :8000)
curl.exe http://localhost/
curl.exe -L http://localhost/pratos/

# Derruba preservando os volumes (dados ficam)
docker compose down
docker volume ls                  # os volumes bella-* continuam existindo

# --- Boas práticas: provar segurança ---
# .env NÃO entra na imagem:
docker run --rm bella-tavola:v1 find /app -name ".env"     # (sem saída)
# roda como usuário não-root:
docker run --rm bella-tavola:v1 whoami                      # appuser
```

**Demo CONFIÁVEL do `/ml/predict` (PowerShell, sem precisar de token)** — testado neste repo:

```powershell
# monta a PASTA do modelo e aponta o MODEL_PATH (schema = crédito)
docker run -d -p 8000:8000 --name bella-test `
  -e MODEL_PATH=/models/credit_rf.pkl `
  -v "${PWD}\datagen\models:/models:ro" `
  bella-tavola:v1

Start-Sleep -Seconds 4
curl.exe -s http://localhost:8000/health
# -> {"api":"ok","model":"loaded"}

curl.exe -s -X POST http://localhost:8000/ml/predict `
  -H "Content-Type: application/json" `
  -d '{\"renda_mensal\":3000,\"divida_atual\":1500,\"historico_pagamentos\":40,\"idade\":30,\"num_dependentes\":3}'
# -> {"prediction":1,"probability":0.65,"label":"inadimplente","model_version":"1.0.0"}

docker stop bella-test; docker rm bella-test
```

> Em **Git Bash** o mesmo comando exige `MSYS_NO_PATHCONV=1` antes do `docker run` (senão o Git Bash converte o caminho `/models` e o mount falha). Por isso o roteiro usa PowerShell.

## 🎓 Perguntas & respostas pra ensinar

**Por que nunca usar `ENV` no Dockerfile pra um secret?**
O valor fica gravado na imagem e aparece em `docker history`. Qualquer um com a imagem vê o token. Secrets vão em runtime (`-e`, `--env-file`) ou como secrets do CI.

**Por que os dados persistem com named volume?**
O volume é gerenciado pelo Docker e vive independente do contêiner. Destruí o contêiner, o volume continua; o novo contêiner reconecta e acha os dados. Sem `-v`, o banco fica no FS do contêiner e o `docker rm` apaga tudo.

**Named volume vs bind mount — quando usar cada um?**
Named volume = Docker gerencia, pra dados de produção. Bind mount = espelha uma pasta local, pra desenvolvimento (live reload). Bind mount **não** substitui o `COPY . .`: com ele o código só existe na minha máquina; em produção não há a minha pasta, só a imagem.

**Por que a API não conecta no banco usando `localhost` no Compose?**
Dentro do contêiner da API, `localhost` é o próprio contêiner da API — não há Postgres ali. O banco está noutro contêiner, acessível pelo **nome do serviço** (`db`) via DNS interno do Compose. Mesma lógica: o Nginx fala com a API por `api`.

**`depends_on` garante que o banco está pronto?**
Não. Garante só que o contêiner **iniciou**. O Postgres leva alguns segundos pra aceitar conexões. Solução: `healthcheck` + `condition: service_healthy` (ou retry na aplicação).

**Diferença entre `docker compose down` e `down -v`?**
`down` remove contêineres e rede, mas **preserva volumes**. `down -v` remove os volumes também — apaga os dados. Perigoso em produção, útil pra resetar o ambiente em dev.

**Por que o `USER appuser` vem depois do `pip install`?**
O `pip install` escreve em diretórios do sistema (`/usr/local/...`) que exigem root. Se `USER` viesse antes, falharia com `PermissionError`. Ordem: instala (root) → copia código → cria usuário → `chown` → `USER` → `CMD`.

**Por que rodar como usuário não-root?**
Princípio do menor privilégio. Se explorarem uma falha na API, não ganham root no contêiner. A API só precisa ler arquivos e servir HTTP.

**O que o multi-stage build elimina?**
O estágio builder usa compiladores e headers pra instalar numpy/scikit-learn — nada disso é necessário pra **rodar** a API. O estágio final copia só os pacotes prontos; somem o cache do pip e as ferramentas de build, reduzindo a imagem.

**O `.dockerignore` reduz muito o tamanho da imagem?**
Pouco em MB (o peso são os pacotes, não o código). O ganho real é **segurança** (`.env` não entra), **velocidade de build** (contexto menor) e **cache**. A redução de tamanho de verdade vem do multi-stage.

---

# 🎬 Vídeo 3 — e05-p03: Docker no pipeline de CI
**Duração alvo: ~6–7 min**

## Roteiro

> 🎯 **A ideia única do vídeo:** até agora a imagem só existia na **minha** máquina. Aqui ela passa a ser **publicada sozinha** num registry público a cada merge — desde que os testes passem. É o "funciona na minha máquina" virando artefato compartilhável.

**Abertura (~30s)**
> "Vídeo final da série. Nos dois anteriores eu transformei a API numa imagem Docker e deixei ela segura e orquestrada — mas essa imagem ainda morava só na minha máquina. Neste vídeo eu integro o Docker ao meu pipeline de CI: a cada merge na `main`, se os testes passarem, a imagem é buildada e publicada **automaticamente** no Docker Hub."

**1) Docker Hub: o que é e por que tag por commit (~1min30)**
> "Primeiro, o que é o **Docker Hub**? É pra imagens o que o Hugging Face Hub é pros modelos, ou o GitHub é pro código: um **registry**, um repositório central na nuvem. `docker push` manda a imagem pra lá; `docker pull` baixa. Uma vez publicada, qualquer máquina no mundo roda a minha API com um único comando, sem precisar do meu código nem instalar nada."
>
> "Agora o detalhe que separa amador de profissional: **a tag**. Todo mundo usa `latest`, mas `latest` é traiçoeira — ela é móvel, hoje aponta pra um código, amanhã pra outro. A tag confiável é o **hash do commit** (o SHA). Olha a cadeia que isso me dá: imagem em produção → SHA → commit exato → código → autor → data. Se uma imagem quebrar em produção, eu faço `git checkout <sha>` e recupero exatamente o código que a gerou. Rastreabilidade total."

🖥️ Tela: abrir `hub.docker.com/r/zaras210/bella-tavola/tags` e apontar que existem **duas tags pro mesmo push**: `latest` e o SHA longo (ex.: `529474f...`).

**2) O job `docker` no `ci.yml` — linha por linha (~2min)** — abrir `.github/workflows/ci.yml`
> "Meu pipeline tem **4 jobs encadeados**: `qualidade` → `integracao` → `docker` → `relatorio`. Os dois primeiros já existiam da Semana 3 (testes). O job novo deste caderno é o **`docker`**. Vou destrinchar ele."

Mostrar e narrar cada parte do job `docker`:
> - **`needs: integracao`** → "Essa é a linha mais importante do vídeo. O job docker **só começa depois** que o `integracao` (os testes completos) passou. O pipeline é um **portão**: código que não passa nos testes **nunca** vira imagem publicada. Qualidade antes de velocidade."
> - **`if: github.event_name == 'push'`** → "Só publica em push pra `main`. Num Pull Request ele nem roda — eu não quero publicar imagem de código que ainda está em revisão."
> - **`docker/setup-buildx-action`** → "Prepara o builder moderno do Docker (o Buildx), que dá suporte a cache de camadas na nuvem."
> - **`docker/login-action`** com `username`/`password` em `${{ secrets.* }}` → "Autentica no Docker Hub. Repara: usuário e senha **não estão escritos no arquivo** — vêm de `secrets`. O YAML é público no meu repo; a credencial, não."
> - **`docker/build-push-action`** com `context: ./api`, `push: true`, as duas `tags` e `cache-from/to: type=gha` → "Esse é o passo que faz o trabalho: builda a imagem a partir do Dockerfile em `api/`, e com `push: true` já manda pro Hub. Gera as **duas tags** (`github.sha` e `latest`) no mesmo build. E o `type=gha` reaproveita o cache de camadas do GitHub Actions — se o `requirements.txt` não mudou, o `pip install` não roda de novo, e o build cai de minutos pra segundos."

**3) Onde ficam os secrets (~1min)**
🖥️ GitHub → **Settings → Secrets and variables → Actions**. Mostrar os 3 secrets: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `HF_TOKEN` — nomes visíveis, **valores ocultos** (o GitHub criptografa e nunca mostra de volta).
> "Três coisas a dizer aqui: (1) o GitHub mostra só o nome, nunca o valor — nem eu consigo ler depois de salvar. (2) O `DOCKER_PASSWORD` **não é a senha da minha conta** — é um **token de acesso** que eu gerei no Docker Hub, com escopo limitado (Read & Write) e revogável sozinho. (3) Se esse token vazar, eu revogo só ele e gero outro, sem mexer na conta. Mesma filosofia do `HF_TOKEN` da Semana 3."

**4) O pipeline rodando de verdade (~1min30)**
🖥️ Aba **Actions** → abrir o último run verde da `main`. Mostrar o **grafo dos 4 jobs em sequência** (`qualidade → integracao → docker → relatorio`), todos com ✓.
> "Aqui está o portão funcionando: os jobs rodaram **em ordem**, cada um esperando o anterior. O `docker` só ficou verde porque o `integracao` ficou verde antes."

🖥️ Voltar pro Docker Hub e mostrar que a tag SHA bate com o commit do run.
> "E a prova final: o SHA da tag no Hub é exatamente o commit deste run. Imagem ↔ commit, fechado."

> **História real pra contar (~30s):** "Na primeira vez que rodei, o job docker **falhou** — eu ainda não tinha configurado os secrets do Docker Hub. E isso é ótimo de mostrar: prova que sem credencial válida a imagem **não sai**. Configurei os 3 secrets, re-rodei o pipeline, e ficou verde. O portão fez exatamente o trabalho dele."

**5) Demonstração ao vivo — "outra máquina" puxando do Hub (~1min30)**

> ⚠️ **É AQUI que entra o `rmi` (a parte que confunde).** O objetivo da demo é provar que **qualquer máquina** roda a API sem o meu código. Mas a minha máquina já tem a imagem (eu buildei nos vídeos 1 e 2). Se eu só der `docker pull`, o Docker responde **"Image is up to date"** e não baixa nada — a demonstração fica sem graça e parece batota. Então eu **apago a cópia local primeiro**; aí o `pull` baixa de verdade, como aconteceria numa máquina nova.

Passo a passo, narrando cada comando (ver cheat sheet abaixo):
> 1. `gh run list` e `gh secret list` → "Confirmo pelo terminal que o último run passou e que os 3 secrets existem."
> 2. **`docker rmi zaras210/bella-tavola:latest`** → "Apago a imagem **local**. Agora a minha máquina está 'limpa', como uma máquina qualquer que nunca viu esse projeto." *(o `docker rm -f bella-ci` junto só remove um contêiner de teste antigo, pra o `--name` não dar conflito.)*
> 3. **`docker pull zaras210/bella-tavola:latest`** → "Agora sim: olha ele **baixando** as camadas do Docker Hub. Isso é literalmente o que aconteceria num servidor novo." *(Aponta na tela: as camadas-base aparecem como "Already exists" porque ficam no cache do Docker; a camada do código é baixada. Isso é o cache de layers, mesmo conceito do build.)*
> 4. `docker run ... zaras210/bella-tavola:latest` + `curl /health` → "E rodo a imagem **que veio do Hub**, não a que eu buildei. O `/health` responde `model loaded` — a API publicada funciona igualzinho à local."

**Fecho — a série inteira (~30s)**
> "Fechando a série: no e05-p01 a API virou uma imagem Docker; no e05-p02 ela ficou segura, enxuta e orquestrada com Compose; e aqui no e05-p03 ela passou a ser publicada **sozinha** a cada merge, com tag rastreável pelo commit. A API saiu de 'funciona na minha máquina' pra um artefato versionado, rastreável e publicado — pronto pra rodar em qualquer lugar."

## 🖥️ Comandos ao vivo

```bash
# Ver os 4 jobs e o resultado do último run na main
gh run list --branch main --limit 1

# Confirmar os secrets (só nomes; valores ocultos)
gh secret list

# RESET (PowerShell): apaga a cópia LOCAL antes, senão o pull só diz "up to date"
docker rm -f bella-ci 2>$null ; docker rmi zaras210/bella-tavola:latest 2>$null

# Provar reprodutibilidade: simular "outra máquina" puxando a imagem do Hub
docker pull zaras210/bella-tavola:latest
```

**Rodar a imagem PUBLICADA pelo CI (PowerShell, com o modelo montado):**

```powershell
docker run -d -p 8000:8000 --name bella-ci `
  -e MODEL_PATH=/models/credit_rf.pkl `
  -v "${PWD}\datagen\models:/models:ro" `
  zaras210/bella-tavola:latest

Start-Sleep -Seconds 4
curl.exe -s http://localhost:8000/
curl.exe -s http://localhost:8000/health     # {"api":"ok","model":"loaded"}

docker stop bella-ci; docker rm bella-ci
```

> Links pra abrir na tela:
> - Actions: `https://github.com/Czar210/cdia-m7-PUCSP/actions`
> - Imagem: `https://hub.docker.com/r/zaras210/bella-tavola/tags`

## 🎓 Perguntas & respostas pra ensinar

**Por que usar token de acesso em vez da senha?**
Escopo limitado (só Read & Write), revogável individualmente sem trocar a senha da conta, e rastreável (vários tokens nomeados). É o padrão da indústria — mesmo raciocínio do `HF_TOKEN`.

**O que fazer se o token vazar?**
Revogar imediatamente no Docker Hub (Account Settings → Security), gerar um novo, atualizar o secret no GitHub, remover o token do histórico se foi commitado, e checar os logs de acesso. *(Foi exatamente o que fiz quando girei meu token depois de configurá-lo.)*

**Por que o segundo `docker push` é muito mais rápido?**
As camadas que não mudaram já estão no Hub ("Layer already exists"); só a camada nova (o código) é enviada. É o mesmo cache de layers do build local.

**Por que usar o SHA do commit como tag?**
Rastreabilidade total: imagem em produção → SHA → commit → código exato → autor → data. `git checkout <sha>` recupera o estado do código.

**Por que o job docker tem `needs: integracao` e não roda em paralelo?**
O pipeline é um portão. Se rodasse em paralelo, poderia publicar a imagem antes de o teste falhar (race condition), e a tag `latest` apontaria pra código quebrado. A sequência garante que código que não passa nos testes **nunca** chega ao registry — qualidade acima de velocidade.

**O que acontece com o Docker Hub quando os testes falham?**
O job docker fica skipped/cancelado, nenhuma imagem nova é publicada, e a tag `latest` continua na última imagem válida.

**A imagem publicada pelo CI é igual à que buildei localmente?**
Funcionalmente sim — mesmo Dockerfile, mesmo `requirements.txt`, mesmo commit (o CI usa `actions/checkout@v4`). Pode diferir em bytes (timestamps, ordem de arquivos), mas é equivalente.

**Por que `cache-from/to: type=gha`?**
Sem cache, cada execução refaz o build do zero, incluindo o `pip install` (minutos). O cache do GitHub Actions reaproveita as camadas; se o `requirements.txt` não mudou, o build fica em segundos.

---

## 📋 Checklist rápido antes de postar cada vídeo

- [ ] Áudio sem ruído e tela legível (fonte grande no terminal/editor).
- [ ] Mostrei o **arquivo** (Dockerfile / compose / ci.yml) e **rodei** o comando correspondente.
- [ ] Expliquei o **porquê**, não só o **o quê**.
- [ ] Vídeo 3: mostrei os 4 jobs verdes **e** as tags no Docker Hub.
- [ ] Encerrei amarrando com o próximo caderno (ou, no 3, com a série inteira).
