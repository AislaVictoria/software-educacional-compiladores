const codeInput = document.querySelector('#code-input');
const exampleSelect = document.querySelector('#example-select');
const analyzeButton = document.querySelector('#analyze-button');
const resultArea = document.querySelector('#result-area');
const codeInfo = document.querySelector('#code-info');
const tokenPanel = document.querySelector('#token-panel');
const tokenCount = document.querySelector('#token-count');
const tokenSummary = document.querySelector('#token-summary');
const tokenTableBody = document.querySelector('#token-table-body');
const lexicalErrors = document.querySelector('#lexical-errors');
const errorList = document.querySelector('#error-list');

function atualizarInformacoes() {
  const linhas = codeInput.value ? codeInput.value.split('\n').length : 0;
  codeInfo.textContent = `${linhas} ${linhas === 1 ? 'linha' : 'linhas'}`;
}

function mostrarResultado(tipo, titulo, mensagem) {
  resultArea.className = `result-area ${tipo}`;
  resultArea.replaceChildren();
  const icon = document.createElement('div');
  icon.className = 'result-icon';
  icon.setAttribute('aria-hidden', 'true');
  icon.textContent = tipo === 'success' ? '✓' : '!';
  const content = document.createElement('div');
  const strong = document.createElement('strong');
  strong.textContent = titulo;
  const paragraph = document.createElement('p');
  paragraph.textContent = mensagem;
  content.append(strong, paragraph);
  resultArea.append(icon, content);
}

function limparAnalise() {
  tokenPanel.hidden = true;
  tokenTableBody.replaceChildren();
  tokenSummary.replaceChildren();
  errorList.replaceChildren();
  lexicalErrors.hidden = true;
}

function adicionarCelula(linha, valor, classe = '') {
  const celula = document.createElement('td');
  celula.textContent = valor;
  if (classe) celula.className = classe;
  linha.appendChild(celula);
}

function mostrarAnalise(dados) {
  tokenPanel.hidden = false;
  tokenCount.textContent = `${dados.tokens.length} ${dados.tokens.length === 1 ? 'token' : 'tokens'}`;
  const contagens = dados.tokens.reduce((mapa, token) => {
    mapa[token.tipo] = (mapa[token.tipo] || 0) + 1;
    return mapa;
  }, {});
  Object.entries(contagens).forEach(([tipo, quantidade]) => {
    const item = document.createElement('span');
    item.className = 'summary-chip';
    item.textContent = `${tipo.replaceAll('_', ' ')}: ${quantidade}`;
    tokenSummary.appendChild(item);
  });
  dados.tokens.forEach((token) => {
    const linha = document.createElement('tr');
    adicionarCelula(linha, token.tipo, 'token-type');
    adicionarCelula(linha, token.lexema, 'token-lexeme');
    adicionarCelula(linha, token.linha);
    adicionarCelula(linha, token.coluna);
    tokenTableBody.appendChild(linha);
  });
  if (dados.erros.length) {
    lexicalErrors.hidden = false;
    dados.erros.forEach((erro) => {
      const item = document.createElement('li');
      item.textContent = erro.mensagem;
      errorList.appendChild(item);
    });
  }
}

async function solicitarAnalise() {
  const mensagemErro = window.AppCore.validarCodigo(codeInput.value);
  if (mensagemErro) {
    mostrarResultado('warning', 'Código não informado', mensagemErro);
    limparAnalise();
    codeInput.focus();
    return;
  }

  limparAnalise();
  analyzeButton.disabled = true;
  analyzeButton.textContent = 'Analisando...';

  try {
    const resposta = await fetch('/api/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo: codeInput.value })
    });
    const dados = await resposta.json();

    if (!resposta.ok) {
      mostrarResultado('warning', 'Não foi possível processar', dados.message);
      return;
    }

    const { caracteres, linhas } = dados.estatisticas;
    const temErros = dados.erros.length > 0;
    mostrarResultado(temErros ? 'warning' : 'success', temErros ? 'Análise concluída com atenção' : 'Análise léxica concluída', `${dados.message} Foram percorridos ${caracteres} caracteres em ${linhas} ${linhas === 1 ? 'linha' : 'linhas'}.`);
    mostrarAnalise(dados);
  } catch (_erro) {
    mostrarResultado('error', 'Falha de comunicação', 'Não foi possível comunicar com o servidor. Verifique a conexão e tente novamente.');
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.innerHTML = 'Solicitar análise <span aria-hidden="true">→</span>';
  }
}

exampleSelect.addEventListener('change', () => {
  const exemplo = window.AppCore.EXEMPLOS[exampleSelect.value];
  if (!exemplo) return;
  codeInput.value = exemplo.codigo;
  atualizarInformacoes();
  limparAnalise();
  mostrarResultado('info', exemplo.titulo, exemplo.descricao);
  codeInput.focus();
});

codeInput.addEventListener('input', atualizarInformacoes);
analyzeButton.addEventListener('click', solicitarAnalise);
limparAnalise();
atualizarInformacoes();
