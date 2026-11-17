"""Gerado por sdks/contract/generate.py a partir de sdks/contract/openapi.json. Não edite."""

from typing import Any, Dict, Generic, List, Optional, TypedDict, TypeVar

T = TypeVar("T")


class Page(TypedDict, Generic[T]):
    """Página de resultados das rotas de listagem."""

    page: int
    pageSize: int
    total: int
    items: List[T]


class CepCodigoIbgeResponse(TypedDict, total=False):
    municipio: Optional[int]
    estado: Optional[int]
    pais: Optional[int]


class CepItemResponse(TypedDict, total=False):
    cep: Optional[str]
    logradouro: Optional[str]
    localidade: Optional[str]
    idMunicipio: Optional[int]
    nomeMunicipio: Optional[str]
    uf: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    dataAtualizacao: Optional[str]
    codigoIbge: Optional["CepCodigoIbgeResponse"]


class CnaeItemResponse(TypedDict, total=False):
    codigo: Optional[str]
    descricao: Optional[str]


class CnpjConformidadeResponse(TypedDict, total=False):
    cnpj: Optional[str]
    cnpjRaiz: Optional[str]
    consultadoEm: Optional[str]
    sancoes: Optional["ConformidadeSancoes"]
    dividaAtiva: Optional["ConformidadeDividaAtiva"]
    avisos: Optional[List[str]]


class CnpjInscricaoEstadualResponse(TypedDict, total=False):
    cnpj: Optional[str]
    inscricaoEstadual: Optional[str]
    uf: Optional[str]
    situacao: Optional[str]
    cnae: Optional[str]
    municipio: Optional[str]
    dataAtualizacao: Optional[str]


class CnpjItemResponse(TypedDict, total=False):
    cnpj: Optional[str]
    razaoSocial: Optional[str]
    nomeFantasia: Optional[str]
    tipo: Optional[str]
    dataAbertura: Optional[str]
    situacaoCadastral: Optional[str]
    dataSituacaoCadastral: Optional[str]
    motivoSituacaoCadastral: Optional[str]
    porte: Optional[str]
    capitalSocial: Optional[float]
    naturezaJuridica: Optional[str]
    logradouro: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    cep: Optional[str]
    bairro: Optional[str]
    municipio: Optional[str]
    uf: Optional[str]
    email: Optional[str]
    telefone: Optional[str]
    situacaoEspecial: Optional[str]
    dataSituacaoEspecial: Optional[str]
    atividadePrincipal: Optional["CnpjItemResponseCode"]
    atividadeSecundaria: Optional[List["CnpjItemResponseCode"]]
    quadroDeSocios: Optional[List["CnpjItemResponsePartner"]]
    dataAtualizacao: Optional[str]


class CnpjItemResponseCode(TypedDict, total=False):
    codigo: Optional[str]
    descricao: Optional[str]


class CnpjItemResponsePartner(TypedDict, total=False):
    nome: Optional[str]
    qualificacao: Optional[str]
    representanteLegal: Optional[str]
    qualificacaoRepresentanteLegal: Optional[str]
    paisOrigem: Optional[str]


class CnpjRelacionamentoAlvo(TypedDict, total=False):
    cnpj: Optional[str]
    cnpjRaiz: Optional[str]
    razaoSocial: Optional[str]
    nomeFantasia: Optional[str]
    situacaoCadastral: Optional[str]
    capitalSocial: Optional[float]
    uf: Optional[str]
    municipio: Optional[str]


class CnpjRelacionamentoAtividadeResumo(TypedDict, total=False):
    codigo: Optional[str]
    descricao: Optional[str]
    quantidade: Optional[int]


class CnpjRelacionamentoEmpresa(TypedDict, total=False):
    cnpj: Optional[str]
    cnpjRaiz: Optional[str]
    razaoSocial: Optional[str]
    nomeFantasia: Optional[str]
    situacaoCadastral: Optional[str]
    dataAbertura: Optional[str]
    porte: Optional[str]
    capitalSocial: Optional[float]
    uf: Optional[str]
    municipio: Optional[str]
    atividadePrincipal: Optional["CnpjItemResponseCode"]
    sociosEmComum: Optional[List["CnpjRelacionamentoSocioEmComum"]]


class CnpjRelacionamentoGrafo(TypedDict, total=False):
    nodes: Optional[List["CnpjRelacionamentoGrafoNode"]]
    edges: Optional[List["CnpjRelacionamentoGrafoEdge"]]


class CnpjRelacionamentoGrafoEdge(TypedDict, total=False):
    source: Optional[str]
    target: Optional[str]
    papel: Optional[str]


class CnpjRelacionamentoGrafoNode(TypedDict, total=False):
    id: Optional[str]
    tipo: Optional[str]
    label: Optional[str]
    cnpjRaiz: Optional[str]
    hashSocio: Optional[str]
    isAlvo: Optional[bool]
    situacao: Optional[str]


class CnpjRelacionamentoResponse(TypedDict, total=False):
    alvo: Optional["CnpjRelacionamentoAlvo"]
    resumo: Optional["CnpjRelacionamentoResumo"]
    socios: Optional[List["CnpjRelacionamentoSocio"]]
    empresasRelacionadas: Optional["Page[CnpjRelacionamentoEmpresa]"]
    grafo: Optional["CnpjRelacionamentoGrafo"]


class CnpjRelacionamentoResumo(TypedDict, total=False):
    totalSocios: Optional[int]
    totalEmpresasRelacionadas: Optional[int]
    totalEmpresasAtivas: Optional[int]
    totalEmpresasInativas: Optional[int]
    capitalSocialConsolidado: Optional[float]
    ufs: Optional[List[str]]
    atividadesPrincipais: Optional[List["CnpjRelacionamentoAtividadeResumo"]]
    totalSociosVerificaveis: Optional[int]
    vinculosCompletos: Optional[bool]
    avisos: Optional[List[str]]


class CnpjRelacionamentoSocio(TypedDict, total=False):
    hashSocio: Optional[str]
    nome: Optional[str]
    tipo: Optional[str]
    documento: Optional[str]
    qualificacao: Optional[str]
    faixaEtaria: Optional[str]
    totalEmpresas: Optional[int]
    vinculoVerificavel: Optional[bool]


class CnpjRelacionamentoSocioEmComum(TypedDict, total=False):
    hashSocio: Optional[str]
    nome: Optional[str]
    qualificacao: Optional[str]
    dataEntradaSociedade: Optional[str]


class CnpjSimplesResponse(TypedDict, total=False):
    cnpj: Optional[str]
    opcaoPeloSimples: Optional[bool]
    dataOpcaoPeloSimples: Optional[str]
    dataExclusaoDoSimples: Optional[str]
    opcaoPeloMEI: Optional[bool]
    dataOpcaoPeloMEI: Optional[str]
    dataExclusaoDoMEI: Optional[str]
    dataAtualizacao: Optional[str]


class CnpjSimplifiedResponse(TypedDict, total=False):
    cnpj: Optional[str]
    razaoSocial: Optional[str]
    situacaoCadastral: Optional[str]
    uf: Optional[str]


class ConformidadeDividaAtiva(TypedDict, total=False):
    fonte: Optional[str]
    disponivel: Optional[bool]
    referencia: Optional[str]
    consta: Optional[bool]
    total: Optional["ConformidadeSoma"]
    emCobranca: Optional["ConformidadeSoma"]
    regularizada: Optional["ConformidadeSoma"]
    ajuizada: Optional["ConformidadeSoma"]
    origem: Optional["ConformidadeOrigem"]
    corresponsavel: Optional["ConformidadeSoma"]
    inscricaoMaisAntiga: Optional[str]
    inscricaoMaisRecente: Optional[str]


class ConformidadeOrigem(TypedDict, total=False):
    tributaria: Optional["ConformidadeSoma"]
    previdenciaria: Optional["ConformidadeSoma"]
    fgts: Optional["ConformidadeSoma"]


class ConformidadeSancao(TypedDict, total=False):
    cadastro: Optional[str]
    cadastroDescricao: Optional[str]
    cnpj: Optional[str]
    codigo: Optional[str]
    categoria: Optional[str]
    inicio: Optional[str]
    fim: Optional[str]
    vigente: Optional[bool]
    orgao: Optional[str]
    uf: Optional[str]
    esfera: Optional[str]
    abrangencia: Optional[str]
    processo: Optional[str]
    valorMulta: Optional[float]


class ConformidadeSancoes(TypedDict, total=False):
    fonte: Optional[str]
    disponivel: Optional[bool]
    referencia: Optional[str]
    consta: Optional[bool]
    vigente: Optional[bool]
    cadastrosVigentes: Optional[List[str]]
    registros: Optional[List["ConformidadeSancao"]]


class ConformidadeSoma(TypedDict, total=False):
    valor: Optional[float]
    inscricoes: Optional[int]


class EstadoItemResponse(TypedDict, total=False):
    uf: Optional[str]
    nome: Optional[str]
    totalEstabelecimentos: Optional[int]


class ExtraCreditsInfo(TypedDict, total=False):
    remaining: Optional[int]


class IErrorCodeModel(TypedDict, total=False):
    status: Optional[str]
    code: Optional[int]
    message: Optional[str]


class LimitsInfo(TypedDict, total=False):
    requestsPerMinute: Optional[int]
    allowExternalSearch: Optional[bool]
    canLiveSearch: Optional[bool]


class MercadoCnaeMes(TypedDict, total=False):
    mes: Optional[str]
    aberturas: Optional[int]
    baixas: Optional[int]
    saldo: Optional[int]
    parcial: Optional[bool]


class MercadoCnaeMunicipio(TypedDict, total=False):
    id: Optional[int]
    nome: Optional[str]
    uf: Optional[str]
    ativas: Optional[int]
    populacaoEstimada: Optional[int]
    ativasPor10MilHabitantes: Optional[float]


class MercadoCnaeNacional(TypedDict, total=False):
    total: Optional[int]
    ativas: Optional[int]
    ativasMei: Optional[int]
    ativasSimples: Optional[int]
    porte: Optional[List["MercadoCnaePorte"]]


class MercadoCnaePorte(TypedDict, total=False):
    codigo: Optional[str]
    descricao: Optional[str]
    ativas: Optional[int]


class MercadoCnaeResponse(TypedDict, total=False):
    cnae: Optional["CnpjItemResponseCode"]
    disponivel: Optional[bool]
    geradoEm: Optional[str]
    nacional: Optional["MercadoCnaeNacional"]
    ufs: Optional[List["MercadoCnaeUf"]]
    uf: Optional["MercadoCnaeUf"]
    maioresMunicipios: Optional[List["MercadoCnaeMunicipio"]]
    tendencia: Optional[List["MercadoCnaeMes"]]
    avisos: Optional[List[str]]


class MercadoCnaeUf(TypedDict, total=False):
    uf: Optional[str]
    ativas: Optional[int]
    participacaoPercentual: Optional[float]
    posicao: Optional[int]


class MercadoIndicadorPonto(TypedDict, total=False):
    periodo: Optional[str]
    ano: Optional[int]
    mes: Optional[int]
    valor: Optional[float]


class MercadoIndicadorResponse(TypedDict, total=False):
    tipo: Optional[str]
    descricao: Optional[str]
    unidade: Optional[str]
    fonte: Optional[str]
    disponivel: Optional[bool]
    serie: Optional[List["MercadoIndicadorPonto"]]
    avisos: Optional[List[str]]


class MercadoMunicipioDados(TypedDict, total=False):
    id: Optional[int]
    nome: Optional[str]
    uf: Optional[str]
    codigoIbge: Optional[str]
    regiao: Optional[str]
    mesorregiao: Optional[str]
    microrregiao: Optional[str]
    populacaoEstimada: Optional[int]
    areaKm2: Optional[float]
    densidadeDemografica: Optional[float]


class MercadoMunicipioEconomia(TypedDict, total=False):
    pibMilReais: Optional[float]
    pibPerCapitaReais: Optional[float]
    anoPib: Optional[int]
    anoPopulacao: Optional[int]
    atualizadoEm: Optional[str]


class MercadoMunicipioEmpresas(TypedDict, total=False):
    estabelecimentosAtivos: Optional[int]
    ativosPorMilHabitantes: Optional[float]


class MercadoMunicipioResponse(TypedDict, total=False):
    municipio: Optional["MercadoMunicipioDados"]
    economia: Optional["MercadoMunicipioEconomia"]
    empresas: Optional["MercadoMunicipioEmpresas"]
    avisos: Optional[List[str]]


class MunicipioDetalhadoResponse(TypedDict, total=False):
    id: Optional[int]
    descricao: Optional[str]
    uf: Optional[str]
    codigoIbge: Optional[str]
    populacaoEstimada: Optional[int]
    regiao: Optional[str]
    mesorregiao: Optional["MunicipioHierarquiaResponse"]
    microrregiao: Optional["MunicipioHierarquiaResponse"]
    regiaoImediata: Optional["MunicipioHierarquiaResponse"]
    regiaoIntermediaria: Optional["MunicipioHierarquiaResponse"]
    ibgeAtualizadoEm: Optional[str]
    totalEmpresas: Optional[int]


class MunicipioHierarquiaResponse(TypedDict, total=False):
    codigo: Optional[str]
    nome: Optional[str]


class MunicipioItemResponse(TypedDict, total=False):
    id: Optional[int]
    descricao: Optional[str]
    uf: Optional[str]


class PlanCreditsInfo(TypedDict, total=False):
    allocated: Optional[int]
    remaining: Optional[int]


class SocioEmpresaItemResponse(TypedDict, total=False):
    cnpj: Optional[str]
    cnpjRaiz: Optional[str]
    razaoSocial: Optional[str]
    nomeFantasia: Optional[str]
    situacaoCadastral: Optional[str]
    dataAbertura: Optional[str]
    porte: Optional[str]
    capitalSocial: Optional[float]
    uf: Optional[str]
    municipio: Optional[str]
    atividadePrincipal: Optional["CnpjItemResponseCode"]
    qualificacao: Optional[str]
    qualificacaoSocio: Optional[str]
    dataEntradaSociedade: Optional[str]


class SocioEmpresasResponse(TypedDict, total=False):
    socio: Optional["SocioInfoResponse"]
    resumo: Optional["SocioResumoResponse"]
    empresas: Optional["Page[SocioEmpresaItemResponse]"]


class SocioInfoResponse(TypedDict, total=False):
    hashSocio: Optional[str]
    nome: Optional[str]
    documento: Optional[str]
    tipo: Optional[str]
    faixaEtaria: Optional[str]
    vinculoVerificavel: Optional[bool]
    avisos: Optional[List[str]]


class SocioResumoResponse(TypedDict, total=False):
    totalEmpresas: Optional[int]
    totalAtivas: Optional[int]
    totalInativas: Optional[int]
    capitalSocialConsolidado: Optional[float]
    ufs: Optional[List[str]]
    qualificacoes: Optional[List[str]]


class WorkspaceCreditsResponse(TypedDict, total=False):
    workspaceId: Optional[int]
    monthReference: Optional[str]
    planCredits: Optional["PlanCreditsInfo"]
    extraCredits: Optional["ExtraCreditsInfo"]
    totalRemainingCredits: Optional[int]
    limits: Optional["LimitsInfo"]


__all__ = ["Page", "CepCodigoIbgeResponse", "CepItemResponse", "CnaeItemResponse", "CnpjConformidadeResponse", "CnpjInscricaoEstadualResponse", "CnpjItemResponse", "CnpjItemResponseCode", "CnpjItemResponsePartner", "CnpjRelacionamentoAlvo", "CnpjRelacionamentoAtividadeResumo", "CnpjRelacionamentoEmpresa", "CnpjRelacionamentoGrafo", "CnpjRelacionamentoGrafoEdge", "CnpjRelacionamentoGrafoNode", "CnpjRelacionamentoResponse", "CnpjRelacionamentoResumo", "CnpjRelacionamentoSocio", "CnpjRelacionamentoSocioEmComum", "CnpjSimplesResponse", "CnpjSimplifiedResponse", "ConformidadeDividaAtiva", "ConformidadeOrigem", "ConformidadeSancao", "ConformidadeSancoes", "ConformidadeSoma", "EstadoItemResponse", "ExtraCreditsInfo", "IErrorCodeModel", "LimitsInfo", "MercadoCnaeMes", "MercadoCnaeMunicipio", "MercadoCnaeNacional", "MercadoCnaePorte", "MercadoCnaeResponse", "MercadoCnaeUf", "MercadoIndicadorPonto", "MercadoIndicadorResponse", "MercadoMunicipioDados", "MercadoMunicipioEconomia", "MercadoMunicipioEmpresas", "MercadoMunicipioResponse", "MunicipioDetalhadoResponse", "MunicipioHierarquiaResponse", "MunicipioItemResponse", "PlanCreditsInfo", "SocioEmpresaItemResponse", "SocioEmpresasResponse", "SocioInfoResponse", "SocioResumoResponse", "WorkspaceCreditsResponse"]
