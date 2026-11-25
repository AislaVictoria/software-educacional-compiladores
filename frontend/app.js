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
const astPanel = document.querySelector('#ast-panel');
const astTree = document.querySelector('#ast-tree');
const astToggle = document.querySelector('#ast-toggle');
const syntaxErrors = document.querySelector('#syntax-errors');
const syntaxErrorList = document.querySelector('#syntax-error-list');

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

  astPanel.hidden = true;
  syntaxErrors.hidden = true;

  astTree.replaceChildren();
  syntaxErrorList.replaceChildren();

  astTree.hidden = false;
  astToggle.textContent = 'Recolher árvore';
  astToggle.setAttribute('aria-expanded', 'true');
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


function criarNoAst(no) {
  const item = document.createElement('li');

  const cabecalho = document.createElement('button');
  cabecalho.type = 'button';
  cabecalho.className = 'ast-node';

  const atributos = no.atributos || {};

  const nome =
    atributos.nome ??
    atributos.valor ??
    atributos.operador ??
    '';

  const inicio = `L${no.linha}:C${no.coluna}`;

  const fim =
    no.linhaFinal != null && no.colunaFinal != null
      ? ` - L${no.linhaFinal}:C${no.colunaFinal}`
      : '';

  cabecalho.textContent =
    `${no.tipo}${nome !== '' ? ` · ${nome}` : ''} (${inicio}${fim})`;

  item.appendChild(cabecalho);

  if (atributos.regra) {
    const regra = document.createElement('small');

    regra.className = 'ast-rule';
    regra.textContent = `Regra: ${atributos.regra}`;

    item.appendChild(regra);
  }

  if (no.filhos && no.filhos.length) {
    const filhos = document.createElement('ul');

    no.filhos.forEach((filho) => {
      filhos.appendChild(criarNoAst(filho));
    });

    item.appendChild(filhos);

    cabecalho.setAttribute('aria-expanded', 'true');

    cabecalho.addEventListener('click', () => {
      filhos.hidden = !filhos.hidden;

      cabecalho.setAttribute(
        'aria-expanded',
        String(!filhos.hidden)
      );
    });
  } else {
    cabecalho.disabled = true;
  }

  return item;
}

function mostrarSintatico(dados) {
  if (dados.sintatico.sucesso && dados.sintatico.ast) {
    astPanel.hidden = false;
    astTree.replaceChildren(criarNoAst(dados.sintatico.ast));
  }
  if (dados.sintatico.erros.length) {
    syntaxErrors.hidden = false;
    dados.sintatico.erros.forEach((erro) => {
      const item = document.createElement('li');
      item.textContent = erro.mensagem;
      syntaxErrorList.appendChild(item);
    });
  }
}

async function solicitarAnalise() {
  const mensagemErro = window.AppCore.validarCodigo(codeInput.value);
  if (mensagemErro) {
    mostrarResultado('warning', 'Entrada inválida', mensagemErro);
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

    const temErrosLexicos = dados.erros.length > 0;
    const temErrosSintaticos = dados.erros_sintaticos.length > 0;

    const resumo = `Foram percorridos ${caracteres} caracteres em ${linhas} ${linhas === 1 ? 'linha' : 'linhas'}.`;

    if (temErrosLexicos) {
      mostrarResultado(
        'warning',
        'Erro na análise léxica',
        `${dados.message} A análise sintática não foi executada. ${resumo}`
      );

    } else if (temErrosSintaticos) {
      mostrarResultado(
        'error',
        'Erro na análise sintática',
        `${dados.message} Os tokens foram reconhecidos, mas a estrutura do código é inválida. ${resumo}`
      );

    } else {
      mostrarResultado(
        'success',
        'Análises léxica e sintática concluídas',
        `${dados.message} ${resumo}`
      );
    }

    mostrarAnalise(dados);
    mostrarSintatico(dados);

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

astToggle.addEventListener('click', () => {
  astTree.hidden = !astTree.hidden;

  astToggle.textContent = astTree.hidden
    ? 'Expandir árvore'
    : 'Recolher árvore';

  astToggle.setAttribute(
    'aria-expanded',
    String(!astTree.hidden)
  );
});

limparAnalise();
atualizarInformacoes();
