# NextAPI para Python (`sharpfy-nextapi`)

SDK oficial da [NextAPI](https://nextapi.com.br) para Python 3.11+: CNPJ (inclusive alfanumérico), Simples Nacional, inscrições estaduais, conformidade, sócios, CEP com busca geográfica, pesquisa de empresas, localidades, mercado e créditos. Sem dependências: só a biblioteca padrão. As respostas são `dict` com tipos (`TypedDict`), prontas para `json.dumps` ou para o seu modelo.

## Requisitos

- Python 3.11 ou mais recente (testado no 3.11 e no 3.15)
- Uma chave de API (veja abaixo)

## Instalação

```bash
pip install sharpfy-nextapi
```

## Chave de API

Crie a sua em [app.nextapi.com.br](https://app.nextapi.com.br). São dois tipos:

| Prefixo | Ambiente | Custo |
|---|---|---|
| `nxa_test_…` | Sandbox: dados de um subconjunto real, limites próprios e CNPJs de teste que provocam cada erro | Nenhum: nada é debitado |
| `nxa_live_…` | Produção | Créditos do seu plano |

O ambiente sai do prefixo da chave; o endereço da API é o mesmo. Guarde a chave na variável de ambiente
`NEXTAPI_KEY`, que o cliente lê quando você não passa a chave. **Nunca** a coloque no código, no repositório ou num
front-end: quem tem a chave consome os seus créditos.

## Início rápido

```python
from sharpfy_nextapi import NextApiClient

nextapi = NextApiClient()  # lê NEXTAPI_KEY

empresa = nextapi.cnpj.consultar("11.222.333/0001-81")
print(empresa["razaoSocial"], empresa["situacaoCadastral"])
```

## Configuração

```python
import os
from sharpfy_nextapi import NextApiClient

nextapi = NextApiClient(
    os.environ["NEXTAPI_KEY"],              # padrão: NEXTAPI_KEY
    base_url="https://api.nextapi.com.br",  # só https (http apenas para localhost)
    timeout=15.0,                           # segundos, por tentativa; padrão 30
    max_retries=3,                          # padrão 2; 0 desliga
    app_info="minha-app/1.4.0",             # identifica a sua aplicação
)
```

| Parâmetro | Padrão | Efeito |
|---|---|---|
| `api_key` | `NEXTAPI_KEY` | Chave de API; o prefixo define o ambiente (`nextapi.environment`) |
| `base_url` | `https://api.nextapi.com.br` | Endereço da API |
| `timeout` | 30.0 | Tempo limite de cada tentativa, em segundos |
| `max_retries` | 2 | Novas tentativas em falha transitória, só em GET |
| `app_info` | — | Nome e versão da sua aplicação, nos cabeçalhos |
| `transport` | `urllib` | Transporte HTTP próprio (proxy, testes) |

### Django, Flask, FastAPI

Crie o cliente uma vez, no carregamento do módulo:

<!-- readme-check: ignorar (depende do framework) -->
```python
# servicos/nextapi.py
from sharpfy_nextapi import NextApiClient
nextapi = NextApiClient(app_info="erp/5.2")

# views.py
from servicos.nextapi import nextapi
def fornecedor(request, cnpj):
    return JsonResponse(nextapi.cnpj.consultar(cnpj))
```

O cliente é síncrono. Em código `async` (FastAPI, aiohttp), chame-o numa thread:
`await asyncio.to_thread(nextapi.cnpj.consultar, cnpj)`.

## Exemplos

### CNPJ

```python
# Cadastro (1 crédito). tolerance_days: idade máxima aceita do dado em cache (0 a 45); 0 força tempo real.
empresa = nextapi.cnpj.consultar("11222333000181", tolerance_days=30)
ao_vivo = nextapi.cnpj.consultar_ao_vivo("11222333000181")  # tempo real; exige plano que permita

simples = nextapi.cnpj.obter_simples("11222333000181")
ies = nextapi.cnpj.obter_inscricoes_estaduais("11222333000181")
conformidade = nextapi.cnpj.obter_conformidade("11222333000181")  # sanções e dívida ativa
alfanumerico = nextapi.cnpj.consultar("12.ABC.345/01DE-35")
```

### Lotes (até 100 CNPJs)

```python
lote = nextapi.cnpj.consultar_lote(["11222333000181", "45997418000153"])  # 1 crédito por CNPJ encontrado
simples_lote = nextapi.cnpj.obter_simples_lote(["11222333000181"])

# Mais de 100: divida em blocos. Lote nunca é repetido sozinho; decida você numa falha.
for i in range(0, len(todos), 100):
    resultados.extend(nextapi.cnpj.consultar_lote(todos[i:i + 100]))
```

### Sócios e grupo econômico

```python
rel = nextapi.cnpj.obter_relacionamentos("11222333000181", page=1, page_size=50)
for socio in rel.get("socios") or []:
    # hashSocio só é estável quando vinculoVerificavel é True: não guarde os provisórios.
    empresas = nextapi.socios.listar_empresas(socio["hashSocio"])
```

### CEP

```python
cep = nextapi.ceps.consultar("01001-000")
por_rua = nextapi.ceps.buscar(uf="SP", nome_municipio="São Paulo", logradouro="Paulista")
raio = nextapi.ceps.buscar_proximos(latitude=-23.5505, longitude=-46.6333, raio_metro=500)
vizinhos = nextapi.ceps.buscar_proximos_do_cep("01001000", raio_metro=1000, page_size=100)
```

### Pesquisa de empresas, com paginação

```python
from datetime import date

page = 1
while True:
    pagina = nextapi.empresas.pesquisar(
        uf="SP",
        cnaes="1091101",                    # vários: separados por vírgula
        data_abertura_inicio=date(2024, 1, 1),
        page=page,
        page_size=100,
    )
    for e in pagina["items"]:
        print(e["cnpj"], e["razaoSocial"])
    if page * pagina["pageSize"] >= pagina["total"]:
        break
    page += 1
```

### Localidades, mercado e créditos

```python
estados = nextapi.estados.listar()
municipios = nextapi.municipios.listar(uf="MG", page_size=100)
bh = nextapi.municipios.obter_por_id(3106200)
cnaes = nextapi.cnaes.listar(page=1, page_size=50)

mercado = nextapi.mercado.obter_cnae("1091101", uf="SP", meses=12)
creditos = nextapi.creditos.consultar()
print(f"restam {creditos['totalRemainingCredits']} créditos")
```

## Erros

Toda falha vira uma exceção do SDK; a classe diz o que fazer, e o código detalha.

| Classe | Quando | Status / código | O que fazer |
|---|---|---|---|
| `NextApiAuthenticationError` | Chave ausente, inválida ou revogada | 401 / 1002, 400 / 1001 | Confira a chave e o ambiente |
| `NextApiInsufficientCreditsError` | Créditos do período acabaram | 405 / 1004, 1006 | Aguarde a renovação ou compre créditos avulsos |
| `NextApiPaidPlanRequiredError` | Recurso exige plano pago | 405 / 1012, 1005 | Mude de plano |
| `NextApiNotFoundError` | CNPJ, CEP ou município não existe | 404 / 1000 | Trate como resultado, não como falha |
| `NextApiValidationError` | Entrada recusada pela API ou pelo SDK | 400 / 1007, ou status 0 | Corrija a entrada; não repita |
| `NextApiRateLimitError` | Limite de requisições por minuto | 429 / 1003 | Já repetido sozinho; diminua o ritmo |
| `NextApiServerError` | Falha da API ou do provedor externo | 5xx / 1014, 9999 | 503 é repetido sozinho; persistindo, fale com o suporte |
| `NextApiConnectionError` | Rede, tempo esgotado ou redirecionamento | status 0 | Verifique a conexão; GETs já foram repetidos |

Todas trazem o status HTTP, o código da API, a mensagem, o corpo da resposta e o **request id**. Ao falar com o
suporte, mande o request id: ele localiza a requisição nos nossos logs.

```python
import time
from sharpfy_nextapi import (NextApiError, NextApiNotFoundError, NextApiInsufficientCreditsError,
                             NextApiRateLimitError)

try:
    empresa = nextapi.cnpj.consultar(cnpj)
except NextApiNotFoundError:
    empresa = None
except NextApiInsufficientCreditsError as e:
    log.warning("sem créditos (%s)", e.request_id)
except NextApiRateLimitError as e:
    time.sleep(e.retry_after or 5)
except NextApiError as e:  # qualquer outra falha do SDK
    log.error("NextAPI %s/%s %s req=%s", e.status, e.code, e.message, e.request_id)
```

## Comportamento

**Novas tentativas.** Só requisições `GET` são repetidas, e só em falha transitória: `429`, `502`, `503`, `504` e
erro de rede. O cliente respeita o `Retry-After` da resposta (até 60 s); sem ele, espera de 0,5 s a 8 s, com
crescimento exponencial e variação aleatória. Os lotes (`POST`) **nunca** são repetidos sozinhos, porque consomem
créditos: numa falha, decida você se repete. O padrão é 2 novas tentativas; `max_retries=0` desliga.

**Tempo limite.** `timeout` por tentativa (padrão 30 s). Com novas tentativas, o tempo total pode passar disso.

**Validação local.** Entrada que a API recusaria com certeza nem sai do processo: vira
`NextApiValidationError` (status 0) antes da requisição. É o caso de CNPJ com tamanho ou dígitos verificadores errados,
lote vazio ou acima de 100, CEP sem 8 dígitos, raio menor ou igual a zero e latitude ou longitude fora da faixa.
CNPJ e CEP aceitam pontuação (`11.222.333/0001-81`, `01001-000`).

**CNPJ alfanumérico.** O formato novo da Receita (IN RFB 2.229/2024, a partir de julho de 2026) é aceito em todos os
métodos de CNPJ: `12.ABC.345/01DE-35` vira `12ABC34501DE35`, com letras em maiúsculas.

**Segurança.** A chave não aparece em logs, mensagens de erro nem na representação do cliente. O cliente não segue
redirecionamento, para a chave nunca ir para outro host, e só aceita `https` no `baseUrl` (`http` apenas para
`localhost`).

**Cabeçalhos enviados.** Além da autorização, cada requisição leva `User-Agent`, `X-NextApi-Client`
(`python/<versão>`) e `X-NextApi-Client-Info` (runtime, sistema e o seu `appInfo`). Servem para o suporte e para
medirmos o uso de cada versão; não carregam dado do seu negócio. O `appInfo` passa por um filtro: só
`A-Za-z0-9._/@+-`, até 64 caracteres.

**Reuso.** Crie um cliente e reutilize. Ele não guarda estado entre chamadas e pode ser usado por várias threads.

## Sandbox

Com a chave `nxa_test_`, estes CNPJs provocam cada resposta da API, para você testar o tratamento de erro sem
gastar nada:

| CNPJ | Resposta |
|---|---|
| `99999991000125` | 404, não encontrado |
| `99999992000170` | 405 / 1004, sem créditos |
| `99999993000114` | 429 / 1003, limite por minuto |
| `99999994000169` | 503 / 1014, falha do provedor |
| `99999995000103` | sucesso depois de 8 s (consulta lenta) |
| `99999996000158` | 405 / 1012, exige plano pago |
| `99999997000100` | 401 / 1002, chave inválida |

O sandbox tem limite próprio de requisições por minuto e por dia, e os dados vêm de um subconjunto real: um CNPJ ou
CEP pode existir em produção e não no sandbox.

## Testes

Os testes não usam rede: conferem cada método contra o contrato da API, em `contract/cases.json` (rota, parâmetros, corpo, respostas e erros).

```bash
docker run --rm -v "$PWD":/src -w /src python:3.12 python -m unittest discover -s tests -v
```

Com `NEXTAPI_SMOKE_KEY` definida (e `NEXTAPI_SMOKE_ENV=sandbox` ou `production`), roda também a fumaça contra a API
publicada, com os passos de `contract/smoke.json`.

## Suporte e licença

Dúvidas e problemas: abra uma issue neste repositório ou escreva pelo [app.nextapi.com.br](https://app.nextapi.com.br),
com o request id do erro. Licença MIT.
