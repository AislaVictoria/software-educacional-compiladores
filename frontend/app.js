const codeInput = document.querySelector('#code-input');
const exampleSelect = document.querySelector('#example-select');
const analyzeButton = document.querySelector('#analyze-button');
const resultArea = document.querySelector('#result-area');
const codeInfo = document.querySelector('#code-info');

function atualizarInformacoes() {
  const linhas = codeInput.value ? codeInput.value.split('\n').length : 0;
  codeInfo.textContent = `${linhas} ${linhas === 1 ? 'linha' : 'linhas'}`;
}

function mostrarResultado(tipo, titulo, mensagem) {
  resultArea.className = `result-area ${tipo}`;
  resultArea.innerHTML = `
    <div class="result-icon" aria-hidden="true">${tipo === 'success' ? '✓' : '!'}</div>
    <div><strong>${titulo}</strong><p>${mensagem}</p></div>
  `;
}

async function solicitarAnalise() {
  const mensagemErro = window.AppCore.validarCodigo(codeInput.value);
  if (mensagemErro) {
    mostrarResultado('warning', 'Código não informado', mensagemErro);
    codeInput.focus();
    return;
  }

  analyzeButton.disabled = true;
  analyzeButton.textContent = 'Enviando...';

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
    mostrarResultado('success', 'Código recebido com sucesso', `${dados.message} Foram recebidos ${caracteres} caracteres em ${linhas} ${linhas === 1 ? 'linha' : 'linhas'}.`);
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
  mostrarResultado('info', exemplo.titulo, exemplo.descricao);
  codeInput.focus();
});

codeInput.addEventListener('input', atualizarInformacoes);
analyzeButton.addEventListener('click', solicitarAnalise);
atualizarInformacoes();
