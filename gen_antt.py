# -*- coding: utf-8 -*-
"""Coleção Postman dedicada da ANTT: CIOT (pefServices, testado), RNTRC e dados
abertos. Fonte: normas ANTT 2026, Portal do Desenvolvedor, guia FlexDocs, CKAN."""
import json
from urllib.parse import urlparse

HML = "https://appservices-hml.antt.gov.br"
PROD = "https://appservices.antt.gov.br"


def u(url):
    p = urlparse(url)
    return {"raw": url, "protocol": p.scheme,
            "host": p.hostname.split(".") if p.hostname else [],
            "path": [s for s in p.path.split("/") if s],
            "query": [{"key": k.split("=")[0], "value": k.split("=")[1] if "=" in k else ""}
                      for k in (p.query.split("&") if p.query else [])]}


CERT = ("mTLS com certificado e-CNPJ (ICP-Brasil). Settings > Certificates para "
        "appservices-hml.antt.gov.br (homolog) e appservices.antt.gov.br (prod).")


def post(nome, path, body, obs, base=HML):
    return {"name": nome, "request": {"method": "POST",
            "header": [{"key": "Content-Type", "value": "application/json"}],
            "url": u(base + path),
            "body": {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2)},
            "description": obs + "\n\n" + CERT}, "response": []}


def get(nome, url, obs):
    return {"name": nome, "request": {"method": "GET", "header": [], "url": u(url),
            "description": obs}, "response": []}


ciot = {"name": "CIOT · pefServices", "description":
        "Ciclo de vida do CIOT. REST/JSON, mTLS por e-CNPJ. Via direta para ETC com frota própria "
        "(sem subcontratar TAC). 'Gerar' testado em 12/09/2026 (HTTP 200, CIOT 560000554432 com o "
        "um e-CNPJ A1 real). Base homolog " + HML + "/pefServices, prod " + PROD + "/pefServices.\n\n" + CERT,
        "item": [
  post("1. Gerar CIOT [OK testado]", "/pefServices/gerar", {"CpfCnpj": "{{cnpj}}"},
       "Reserva o número do CIOT (12 díg.). Resposta: Dados.CIOT. TESTADO: HTTP 200, Sucesso:true."),
  post("2. Declarar Operação de Transporte", "/pefServices/api/DeclaracaoOperacaoTransporte",
       {"IdOperacaoTransporte": "{{idOperacao}}", "TipoOperacao": "{{tipoOperacao}}",
        "CpfCnpjContratado": "{{cpfCnpjTransportador}}", "RNTRCContratado": "{{rntrc}}",
        "ValorFrete": "{{valorFrete}}", "DataDeclaracao": "{{dataISO}}",
        "Veiculos": [{"Placa": "{{placa}}", "RNTRC": "{{rntrc}}", "Eixos": "{{eixos}}"}],
        "OrigemDestino": {"MunicipioOrigem": "{{ibgeOrigem}}", "MunicipioDestino": "{{ibgeDestino}}", "Distancia": "{{km}}"},
        "DadosCarga": {"NaturezaCarga": "{{naturezaCarga}}", "PesoTotalCarga": "{{peso}}"},
        "InfPagamento": {"ChavePix": "{{pix}}", "CpfCnpj": "{{cnpj}}"}},
       "Vincula dados e gera o código de 16 díg. Valida piso mínimo (bloqueia se abaixo). Antes da viagem. Confirmar campos no Swagger oficial."),
  post("3. Consultar CIOT Gerado", "/pefServices/api/ConsultarCIOTGerado",
       {"CodigoIdentificacaoOperacao": "{{ciot}}", "AnoDeclaracao": "{{ano}}"}, "Situação do CIOT."),
  post("4. Retificar Operação [a confirmar]", "/pefServices/api/RetificacaoOperacaoTransporte",
       {"CodigoIdentificacaoOperacao": "{{ciot}}"}, "Altera/adita. Path inferido; confirmar no Swagger."),
  post("5. Cancelar Operação", "/pefServices/api/CancelamentoOperacaoTransporte",
       {"CodigoIdentificacaoOperacao": "{{ciot}}", "MotivoCancelamento": "{{motivo}}"}, "Cancela (janela pré-viagem)."),
  post("6. Encerrar Operação", "/pefServices/api/EncerramentoOperacaoTransporte",
       {"CodigoIdentificacaoOperacao": "{{ciot}}", "DadosCarga": {"PesoTotalCarga": "{{peso}}"}}, "Encerra após a viagem."),
  post("7. Consultar Situação do Transportador", "/pefServices/api/ConsultaSituacaoTransportador",
       {"CpfCnpj": "{{cpfCnpjTransportador}}", "RNTRC": "{{rntrc}}"}, "Regularidade do transportador."),
  post("8. Consultar Frota do Transportador", "/pefServices/api/ConsultaFrotaTransportador",
       {"CpfCnpj": "{{cpfCnpjTransportador}}", "RNTRC": "{{rntrc}}"}, "Frota vinculada ao RNTRC."),
  post("9. Consultar Exceção (piso/bloqueios)", "/pefServices/api/ConsultaExcecao",
       {"CpfCnpj": "{{cnpj}}"}, "Exceções/bloqueios (ex.: piso)."),
]}

rntrc = {"name": "RNTRC · Registro de Transportadores", "description":
        "Consulta do Registro Nacional de Transportadores Rodoviários de Cargas. A consulta pública web "
        "não exige login; a API do Portal do Desenvolvedor pode exigir credenciamento (a confirmar, o portal "
        "é SPA e não abre a spec por fetch). Provedores privados (Infosimples, Netrin) revendem por API.",
        "item": [
  get("Consulta pública RNTRC (web)", "https://consultapublica.antt.gov.br/",
      "Página web de consulta por transportador (RNTRC/CPF/CNPJ), localidade ou veículo. Não é API REST; é tela pública. A confirmar se há endpoint JSON por trás."),
  get("Portal do Desenvolvedor · doc RNTRC", "https://portaldodesenvolvedor.antt.gov.br/page/documentacao-RNTRC",
      "Documentação da API RNTRC. Existência confirmada; se é aberta ou credenciada e a URL base: a confirmar (abrir no navegador). Provável exigência de token/gov.br."),
]}

dados = {"name": "Dados Abertos (CKAN)", "description":
        "Portal de dados abertos da ANTT (CKAN). Dataset RNTRC com CSVs mensais. Útil para carga analítica/cadastral "
        "em lote, não para consulta transacional em tempo real. API CKAN padrão (action API); Datastore por recurso a confirmar.",
        "item": [
  get("CKAN · pacote do dataset RNTRC", "https://dados.antt.gov.br/api/3/action/package_show?id=rntrc",
      "Metadados e lista de recursos (CSVs) do dataset RNTRC via API CKAN action."),
  get("CKAN · listar datasets da ANTT", "https://dados.antt.gov.br/api/3/action/package_list",
      "Lista todos os datasets publicados. API CKAN padrão, pública."),
]}

variaveis = [
  {"key": "cnpj", "value": "", "description": "CNPJ do emitente/contratante"},
  {"key": "cpfCnpjTransportador", "value": "", "description": "CPF/CNPJ do transportador (TAC/ETC)"},
  {"key": "rntrc", "value": "", "description": "RNTRC do transportador"},
  {"key": "ciot", "value": "", "description": "código do CIOT"},
  {"key": "ano", "value": "2026", "description": "ano da declaração"},
  {"key": "idOperacao", "value": "", "description": "id interno da operação"},
  {"key": "tipoOperacao", "value": "", "description": "tipo da operação (ver doc ANTT)"},
  {"key": "valorFrete", "value": "", "description": "valor do frete (respeitar piso)"},
  {"key": "dataISO", "value": "", "description": "data da declaração (ISO 8601)"},
  {"key": "placa", "value": "", "description": "placa do veículo"},
  {"key": "eixos", "value": "", "description": "número de eixos"},
  {"key": "ibgeOrigem", "value": "", "description": "IBGE origem"},
  {"key": "ibgeDestino", "value": "", "description": "IBGE destino"},
  {"key": "km", "value": "", "description": "distância km"},
  {"key": "naturezaCarga", "value": "", "description": "natureza da carga"},
  {"key": "peso", "value": "", "description": "peso total"},
  {"key": "pix", "value": "", "description": "chave Pix do frete"},
  {"key": "motivo", "value": "", "description": "motivo do cancelamento"},
]

descricao = (
  "Webservices e serviços eletrônicos da ANTT. Diferente da SEFAZ, a ANTT NÃO tem um webservice único "
  "para tudo: o núcleo transacional é a API pefServices (CIOT), que a ANTT abriu em 2026 (Portaria SUROC "
  "6/2026); RNTRC e dados abertos são superfícies separadas.\n\n"
  "## Autenticação\n"
  "pefServices (CIOT): mTLS com certificado e-CNPJ ICP-Brasil (o MESMO da SEFAZ). Configure em "
  "Settings > Certificates. RNTRC/dados abertos: consulta pública/CKAN, sem certificado.\n\n"
  "## Testado\n"
  "Gerar CIOT em homologação com um e-CNPJ A1 real: HTTP 200, CIOT 560000554432 (12/09/2026).\n\n"
  "## Honestidade\n"
  "Endpoints do CIOT vêm do guia FlexDocs e dos paths reais da API; confirmar campos no Swagger oficial "
  "do Portal do Desenvolvedor antes de produção. Itens [a confirmar] não têm spec pública fechada. "
  "A API RNTRC do Portal do Desenvolvedor pode exigir credenciamento (portal SPA, não verificável por fetch).\n\n"
  "Ref: Lei 11.442/2007, MP 1.343/2026, Res. ANTT 6.078/2026, Portaria SUROC 6/2026."
)

col = {"info": {"name": "ANTT · Webservices (CIOT · RNTRC · Dados Abertos)",
                "description": descricao,
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
       "variable": variaveis, "item": [ciot, rntrc, dados]}
json.dump(col, open("postman/ANTT-Webservices.postman_collection.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print(f"OK: {len(col['item'])} pastas, {sum(len(f['item']) for f in col['item'])} itens")
