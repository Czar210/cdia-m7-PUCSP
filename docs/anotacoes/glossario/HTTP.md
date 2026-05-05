
Códigos de 3 dígitos que servem como respostas de servidores para requisições

Eles são divididos em 5 categorias e totalizam 63 erros

- 1xx: Informativo - Indicam que a requisição foi recebida e o processo continua. Muito raro de ver hoje em dia
	- 100 Continue: O servidor recebeu o inicio da requisição e o Cliente pode continuar
	- 101 Switching Protocols
	- 102 Processing
- 2xx: Sucesso - Indicam que seja lá o que você fez deu certo (ou quem criou as respostas é preguiçoso)
	- 200 Ok: A mais padrão de sucesso
	- 201 Created
	- 204 No Content: Sucesso mas não tem nada no corpo da resposta pra ser entregue
- 3xx: Redirecionamento - Recurso solicitado mudou de endereço
	- 301 Moved Permanently
	- 302 Found: Mudança temporaria de endereço
	- 304 Not Modified
- 4xx: Erro do lado do Cliente
	- 400 Bad Request: O servidor não atendeu o que vc pediu
	- 401 Unauthorized: Você precisa de um Bearer ou uma autenticação pra retornar a informação
	- 403 Forbidden: Você está logado mas não tem a permissão pra ver isso
	- 404 Not Found: O servidor não achou oq vc queria
	- 429 Too Many Requests: Flood em APIs com Rate Limit
- 5xx: Erro do Servidor
	- 500 Internal Server Error: Erro Genérico
	- 502 Bad Gateway: O Servidor intermediário recebeu uma resposta invalida
	- 503 Service Unavailable
	- 504 Gateway Timeout: Demorou muito