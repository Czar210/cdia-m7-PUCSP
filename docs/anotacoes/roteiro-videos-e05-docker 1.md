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

**Abertura (~30s)**
> "Vídeo final: integro o Docker ao meu pipeline de CI. A cada merge na `main`, se os testes passarem, a imagem é buildada e publicada automaticamente no Docker Hub."

**Docker Hub e tags por commit (~1min30)**
> "O **Docker Hub** é pra imagens o que o Hugging Face Hub é pros modelos: um registry central. `docker push` envia, `docker pull` recebe. A tag mais confiável não é `latest` — é o **hash do commit**. Assim, dada qualquer imagem, eu sei exatamente qual commit a gerou: imagem → SHA → commit → código → autor."

**O job docker no ci.yml (~2min)** — abrir `.github/workflows/ci.yml`
> "Adicionei um quarto job. Ele usa as actions oficiais: `setup-buildx`, `login-action` pra autenticar com segurança, e `build-push-action` pro build + push com cache de layers (`type=gha`). Duas tags: o `github.sha` e `latest`."
>
> "Detalhe crucial: `needs: integracao`. O job docker **só roda depois** dos testes passarem — o pipeline é um portão. E os secrets (`DOCKER_USERNAME`, `DOCKER_PASSWORD`) ficam em `${{ secrets.* }}`, nunca escritos no YAML. A senha é um **token de acesso** revogável, não a senha da conta."

🖥️ Mostrar no GitHub: **Settings → Secrets and variables → Actions** (3 secrets, valores ocultos).

**O pipeline rodando de verdade (~2min)**
🖥️ Aba **Actions**: o run verde da `main` com os 4 jobs (`qualidade → integracao → docker → relatorio`).
🖥️ Docker Hub `hub.docker.com/r/zaras210/bella-tavola/tags`: as tags `latest` e o SHA `529474f...`.
> "História real: na primeira vez o job docker **falhou** — eu ainda não tinha configurado os secrets do Docker Hub. Isso prova o ponto: sem credencial válida, a imagem não sai. Configurei os secrets, re-rodei, e ficou verde. O portão funcionou."

**Fecho — a série inteira (~30s)**
> "Resumindo: no e05-p01 a API virou imagem; no e05-p02 ficou segura, enxuta e orquestrada; e aqui no e05-p03 é publicada automaticamente a cada merge. Saiu de 'funciona na minha máquina' pra um artefato versionado, rastreável e publicado."

## 🖥️ Comandos ao vivo

```bash
# Ver os 4 jobs e o resultado do último run na main
gh run list --branch main --limit 1

# Confirmar os secrets (só nomes; valores ocultos)
gh secret list

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
