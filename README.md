# Webservices da ANTT (coleção Postman)

Coleção Postman dos webservices e serviços eletrônicos da **ANTT**: CIOT
(pefServices), RNTRC e dados abertos.

Arquivo: `postman/ANTT-Webservices.postman_collection.json` (13 itens em 3 pastas).

## O que muda em relação à SEFAZ

A ANTT **não** tem um webservice único para tudo. O núcleo transacional é a API
**pefServices** (ciclo de vida do CIOT: gerar, consultar, cancelar, encerrar),
que a ANTT abriu em 2026 (Portaria SUROC 6/2026). RNTRC e dados abertos (CKAN)
são superfícies separadas.

O `POST /pefServices/gerar` foi **testado em homologação em 12/09/2026** com um
e-CNPJ A1 real: HTTP 200, CIOT retornado.

## Autenticação

- **pefServices (CIOT)**: mTLS com certificado e-CNPJ ICP-Brasil, o MESMO
  usado na SEFAZ. Configure em Settings > Certificates para
  `appservices-hml.antt.gov.br` (homolog) e `appservices.antt.gov.br` (prod).
- **RNTRC / dados abertos**: consulta pública/CKAN, sem certificado.

## Setup no Postman

1. **Import** > `postman/ANTT-Webservices.postman_collection.json`.
2. Adicione o certificado por host (acima) e desligue a verificação SSL do
   servidor se necessário.
3. Ajuste a variável `cnpj` (14 dígitos, só números) e dispare.

## Honestidade sobre as fontes

Os endpoints do CIOT vêm do guia FlexDocs e dos paths reais da API. Confirme os
campos no Swagger oficial do Portal do Desenvolvedor ANTT antes de produção.
Itens `[a confirmar]` não têm spec pública fechada. A API RNTRC do Portal do
Desenvolvedor pode exigir credenciamento.

Referências: Lei 11.442/2007, MP 1.343/2026, Res. ANTT 6.078/2026,
Portaria SUROC 6/2026.

## Como é gerado

Fonte de verdade: `gen_antt.py` monta o `.json` do Postman. Para propor mudança,
edite o gerador, rode e abra um PR.

## Repositórios irmãos

- [sefaz-webservices-postman](https://github.com/stoix-dev/sefaz-webservices-postman): catálogo completo dos webservices da SEFAZ (NF-e, NFC-e, CT-e, MDF-e)
- [ciot-integradoras-postman](https://github.com/stoix-dev/ciot-integradoras-postman): CIOT via ANTT (pefServices) e integradoras de pagamento de frete

## Sobre

Mantido pela [Stoix](https://stoix.dev). Licença MIT.
