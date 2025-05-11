1 - Acesse o link abaixo e crie um projeto no Google Cloud Platform:
https://console.cloud.google.com/projectcreate

2 - Após a criação do projeto e clique em IAM e administradores a esquerda -> Contas de Serviço.

Crie uma conta de serviço: informe apenas o ID da conta de serviço: google-api-tutorial

Clique em Criar e continuar -> Continuar -> Concluir

3 - Clique na conta de serviço criada, e selecione a aba Chaves para criar a chave.

Clique no botão Adicionar chave -> Criar nova chave.

Selecione o formato JSON e a chave vai ser criada automaticamente e baixada na máquina.

A chave é um arquivo JSON que precisará ser armazenado no Secrets Manager da AWS.

Dentro do arquivo JSON da chave existe um endereço de e-mail. Compartilhe a pasta do Google drive com o e-mail informado no arquivo.

O e-mail termina com "<>.iam.gserviceaccount.com"

3 - Clique no ícone de três traços (Menu de navegação) a esquerda no começo da página e procure por APIs e serviços -> APIs e serviços ativados.

Clique na opção "+ Ativar APIs e serviços"

Então, procure pela Biblioteca do Google Drive API.

Clique no ícone e depois no botão Ativar.
