const API_URL = ''
const emptyForm = { nome: '', raca: '', categoria: '', peso_kg: '', idade_meses: '', valor_arroba: '' }
const currency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))
let view = getView()
let refreshKey = 0

function getView() {
  const path = window.location.pathname
  return path === '/calcular' ? 'calculator' : path === '/listar' ? 'records' : path === '/resumo' ? 'summary' : 'dashboard'
}

async function api(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  const data = response.status === 204 ? null : await response.json()
  if (!response.ok) throw new Error((data && data.erro) || 'Não foi possível concluir a operação.')
  return data
}

function navigate(next) {
  const paths = { dashboard: '/', calculator: '/calcular', records: '/listar', summary: '/resumo' }
  window.history.pushState({}, '', paths[next])
  view = next
  render()
}

function header() {
  const links = [['dashboard', 'Início'], ['calculator', 'Calcular'], ['records', 'Avaliações'], ['summary', 'Resumo']]
  return `<header class="topbar"><button class="brand" data-view="dashboard"><span class="brand-mark">✦</span> Agro<span>logic</span></button><nav>${links.map(([key, label]) => `<button class="nav-btn ${view === key ? 'active' : ''}" data-view="${key}">${label}</button>`).join('')}</nav></header>`
}

function layout(content) {
  return `<div class="app-shell">${header()}${content}</div>`
}

function dashboard() {
  return `<main class="dashboard"><section class="hero"><div><p class="eyebrow">Gestão pecuária conectada ao backend</p><h1>Agrologic para decisões melhores.</h1><p>Calcule, salve, consulte e acompanhe as avaliações reais do seu gado em um só lugar.</p><button class="primary" data-view="calculator">Calcular valor do boi</button></div></section><section class="feature-grid"><article><span>01</span><h2>Calcule</h2><p>Use peso e valor da arroba para obter uma estimativa imediata.</p><button data-view="calculator">Abrir calculadora →</button></article><article><span>02</span><h2>Gerencie</h2><p>Cadastre, edite, consulte e exclua avaliações persistidas no banco.</p><button data-view="records">Ver avaliações →</button></article><article><span>03</span><h2>Explore</h2><p>Pesquise por nome, filtre por preço e data, ordene e navegue pelas páginas.</p><button data-view="records">Explorar avaliações →</button></article></section></main>`
}

function escapeHTML(value) {
  return String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  })[character])
}

function field(label, name, value, type = 'text', step = '') {
  return `<label class="field"><span>${label}</span><input name="${name}" type="${type}" ${step ? `step="${step}"` : ''} value="${escapeHTML(value)}" required></label>`
}

function formFields(form) {
  return `<div class="form-grid"><label class="field"><span>Nome (opcional)</span><input name="nome" value="${escapeHTML(form.nome)}"></label>${field('Raça', 'raca', form.raca)}${field('Categoria', 'categoria', form.categoria)}${field('Peso (kg)', 'peso_kg', form.peso_kg, 'number')}${field('Idade (meses)', 'idade_meses', form.idade_meses, 'number')}${field('Valor da arroba', 'valor_arroba', form.valor_arroba, 'number', '0.01')}</div>`
}

function readForm(formElement) {
  return Object.fromEntries(new FormData(formElement).entries())
}

function calculator() {
  const form = { ...emptyForm, raca: 'Nelore', categoria: 'Boi Gordo', peso_kg: '480', idade_meses: '36', valor_arroba: '300' }
  return `<main class="page"><section class="panel calculator-panel"><h1>Calcular valor do boi</h1><p class="intro">A fórmula do backend converte o peso em arrobas e multiplica pelo valor informado.</p><form id="calculator-form">${formFields(form)}<div class="actions"><button class="primary">Calcular estimativa</button></div></form><div id="calculator-feedback"></div><div id="calculator-result"></div></section></main>`
}

function records() {
  return `<main class="page records-page"><section class="panel"><div class="panel-title"><h1>Avaliações cadastradas</h1></div>
    <div class="records-tools">
      <form id="filter-form" class="tool-form"><h2>Raça, categoria e peso</h2><div class="filter-grid"><input name="raca" placeholder="Filtrar por raça"><input name="categoria" placeholder="Filtrar por categoria"><input name="peso_min" type="number" min="0" placeholder="Peso mínimo (kg)"><input name="peso_max" type="number" min="0" placeholder="Peso máximo (kg)"></div><button class="primary">Aplicar filtro</button></form>
      <form id="name-search-form" class="tool-form"><h2>Buscar por nome</h2><div class="filter-grid"><input name="nome" placeholder="Nome do animal" required></div><button class="primary">Buscar</button></form>
      <div class="tool-form"><h2>Filtrar por preço</h2><div class="tool-row"><form id="price-min-form"><label class="field"><span>Preço mínimo</span><input name="preco_min" type="number" min="0" step="0.01" placeholder="R$"></label><button class="secondary">Aplicar</button></form><form id="price-max-form"><label class="field"><span>Preço máximo</span><input name="preco_max" type="number" min="0" step="0.01" placeholder="R$"></label><button class="secondary">Aplicar</button></form></div></div>
      <form id="date-filter-form" class="tool-form"><h2>Filtrar por período</h2><div class="tool-row"><label class="field"><span>Data inicial</span><input name="data_inicio" type="date"></label><label class="field"><span>Data final</span><input name="data_fim" type="date"></label></div><button class="primary">Filtrar período</button></form>
      <form id="recent-form" class="tool-form"><h2>Avaliações recentes</h2><div class="filter-grid"><input name="limite" type="number" min="1" placeholder="Limite (opcional)"></div><button class="secondary">Mostrar recentes</button></form>
      <form id="sort-form" class="tool-form"><h2>Ordenar avaliações</h2><div class="filter-grid"><select name="ordenacao"><option value="">Selecione a ordenação</option><option value="preco-crescente">Preço: menor para maior</option><option value="preco-decrescente">Preço: maior para menor</option><option value="peso-asc">Peso: mais leve primeiro</option><option value="peso-desc">Peso: mais pesado primeiro</option></select></div><button class="secondary">Ordenar</button></form>
      <form id="lookup-form" class="tool-form lookup"><h2>Consultar pelo ID</h2><div class="filter-grid"><input name="id" type="number" min="1" placeholder="ID da avaliação" required></div><button class="secondary">Consultar</button></form>
    </div>
    <div class="records-actions"><button type="button" class="secondary" id="clear-filters">Limpar filtros e voltar à lista</button></div><div id="records-feedback"></div><div id="records-table"><p class="empty">Carregando...</p></div></section><div id="edit-area"></div></main>`
}

function summary() {
  return `<main class="page"><section class="panel"><div class="panel-title"><h1>Resumo das avaliações</h1></div><div id="summary-content"><p class="empty">Carregando resumo...</p></div></section></main>`
}

function render() {
  const content = view === 'calculator' ? calculator() : view === 'records' ? records() : view === 'summary' ? summary() : dashboard()
  document.body.innerHTML = layout(content)
  document.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => navigate(button.dataset.view)))
  if (view === 'calculator') setupCalculator()
  if (view === 'records') setupRecords()
  if (view === 'summary') loadSummary()
}

function feedback(id, message, kind = 'error') {
  document.querySelector(id).innerHTML = message ? `<p class="${kind}">${message}</p>` : ''
}

function setupCalculator() {
  const calculatorForm = document.querySelector('#calculator-form')
  let result = null
  calculatorForm.addEventListener('submit', async (event) => {
    event.preventDefault()
    const data = readForm(calculatorForm)
    const button = calculatorForm.querySelector('button')
    button.disabled = true
    feedback('#calculator-feedback', '')
    try {
      result = await api('/bois/calcular', { method: 'POST', body: JSON.stringify({ peso_kg: Number(data.peso_kg), valor_arroba: Number(data.valor_arroba) }) })
      document.querySelector('#calculator-result').innerHTML = `<div class="result-box"><div><span>Peso</span><strong>${result.peso_kg} kg</strong></div><div><span>Arroba</span><strong>${currency(result.valor_arroba)}</strong></div><div><span>Estimativa</span><strong>${currency(result.preco_estimado)}</strong></div></div><button class="secondary" id="save-evaluation">Salvar avaliação</button>`
      document.querySelector('#save-evaluation').addEventListener('click', async () => {
        try {
          const saved = await api('/bois', { method: 'POST', body: JSON.stringify({ ...data, peso_kg: Number(data.peso_kg), idade_meses: Number(data.idade_meses), valor_arroba: Number(data.valor_arroba) }) })
          feedback('#calculator-feedback', `Avaliação #${saved.id} salva com sucesso.`, 'success')
          refreshKey += 1
        } catch (error) { feedback('#calculator-feedback', error.message) }
      })
    } catch (error) { feedback('#calculator-feedback', error.message) }
    button.disabled = false
  })
}

async function loadRecords(path = '/bois/paginar?pagina=1&por_pagina=10') {
  try {
    const data = await api(path)
    const items = Array.isArray(data) ? data : data && data.resultados ? data.resultados : data ? [data] : []
    const container = document.querySelector('#records-table')
    const table = items.length ? `<div class="table-wrap"><table><thead><tr><th>ID</th><th>Nome</th><th>Raça</th><th>Categoria</th><th>Peso</th><th>Idade</th><th>Preço estimado</th><th>Data</th><th>Ações</th></tr></thead><tbody>${items.map(recordRow).join('')}</tbody></table></div>` : '<p class="empty">Nenhuma avaliação encontrada.</p>'
    const pagination = data && data.pagina !== undefined ? `<div class="pagination"><span>${data.total} avaliação(ões) · Página ${data.pagina} de ${Math.max(data.total_paginas, 1)}</span><label>Por página <select data-page-size><option value="10" ${data.por_pagina === 10 ? 'selected' : ''}>10</option><option value="25" ${data.por_pagina === 25 ? 'selected' : ''}>25</option><option value="50" ${data.por_pagina === 50 ? 'selected' : ''}>50</option><option value="100" ${data.por_pagina === 100 ? 'selected' : ''}>100</option></select></label><div><button class="secondary" data-page="${data.pagina - 1}" ${data.pagina <= 1 ? 'disabled' : ''}>Anterior</button><button class="secondary" data-page="${data.pagina + 1}" ${data.pagina >= data.total_paginas ? 'disabled' : ''}>Próxima</button></div></div>` : ''
    container.innerHTML = table + pagination
    container.querySelectorAll('[data-edit]').forEach((button) => button.addEventListener('click', () => editRecord(items.find((item) => item.id === Number(button.dataset.edit)))))
    container.querySelectorAll('[data-delete]').forEach((button) => button.addEventListener('click', () => deleteRecord(Number(button.dataset.delete))))
    container.querySelectorAll('[data-page]').forEach((button) => button.addEventListener('click', () => {
      if (!button.disabled) loadRecords(`/bois/paginar?pagina=${button.dataset.page}&por_pagina=${container.querySelector('[data-page-size]').value}`)
    }))
    container.querySelector('[data-page-size]')?.addEventListener('change', (event) => loadRecords(`/bois/paginar?pagina=1&por_pagina=${event.target.value}`))
    feedback('#records-feedback', '')
  } catch (error) { feedback('#records-feedback', error.message) }
}

function recordRow(item) {
  const date = item.data_avaliacao ? new Date(item.data_avaliacao).toLocaleDateString('pt-BR') : '—'
  return `<tr><td>#${item.id}</td><td>${escapeHTML(item.nome || '—')}</td><td>${escapeHTML(item.raca)}</td><td>${escapeHTML(item.categoria)}</td><td>${item.peso_kg} kg</td><td>${item.idade_meses} meses</td><td>${currency(item.preco_estimado)}</td><td>${escapeHTML(date)}</td><td><button class="table-action" data-edit="${item.id}">Editar</button><button class="table-action danger" data-delete="${item.id}">Excluir</button></td></tr>`
}

function setupRecords() {
  loadRecords()
  document.querySelector('#filter-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const data = readForm(event.target)
    let path = '/bois'
    if (data.raca) path = `/bois/filtrar/raca?raca=${encodeURIComponent(data.raca)}`
    else if (data.categoria) path = `/bois/filtrar/categoria?categoria=${encodeURIComponent(data.categoria)}`
    else if (data.peso_min || data.peso_max) path = `/bois/filtrar/peso?${new URLSearchParams({ ...(data.peso_min && { peso_min: data.peso_min }), ...(data.peso_max && { peso_max: data.peso_max }) })}`
    loadRecords(path)
  })
  document.querySelector('#name-search-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { nome } = readForm(event.target)
    loadRecords(`/bois/buscar?${new URLSearchParams({ nome })}`)
  })
  document.querySelector('#price-min-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { preco_min } = readForm(event.target)
    if (preco_min === '') return feedback('#records-feedback', 'Informe o preço mínimo para filtrar.')
    loadRecords(`/bois/filtrar/preco-minimo?${new URLSearchParams({ preco_min })}`)
  })
  document.querySelector('#price-max-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { preco_max } = readForm(event.target)
    if (preco_max === '') return feedback('#records-feedback', 'Informe o preço máximo para filtrar.')
    loadRecords(`/bois/filtrar/preco-maximo?${new URLSearchParams({ preco_max })}`)
  })
  document.querySelector('#date-filter-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { data_inicio, data_fim } = readForm(event.target)
    if (!data_inicio && !data_fim) return feedback('#records-feedback', 'Informe pelo menos uma data para filtrar o período.')
    const params = new URLSearchParams()
    if (data_inicio) params.set('data_inicio', data_inicio)
    if (data_fim) params.set('data_fim', data_fim)
    loadRecords(`/bois/filtrar/data?${params}`)
  })
  document.querySelector('#recent-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { limite } = readForm(event.target)
    loadRecords(limite ? `/bois/recentes?${new URLSearchParams({ limite })}` : '/bois/recentes')
  })
  document.querySelector('#sort-form').addEventListener('submit', (event) => {
    event.preventDefault()
    const { ordenacao } = readForm(event.target)
    const paths = {
      'preco-crescente': '/bois/ordenar/preco-crescente',
      'preco-decrescente': '/bois/ordenar/preco-decrescente',
      'peso-asc': '/bois/ordenar/peso?direcao=asc',
      'peso-desc': '/bois/ordenar/peso?direcao=desc',
    }
    if (!paths[ordenacao]) return feedback('#records-feedback', 'Selecione uma ordenação.')
    loadRecords(paths[ordenacao])
  })
  document.querySelector('#clear-filters').addEventListener('click', () => {
    document.querySelectorAll('.records-tools form').forEach((form) => form.reset())
    loadRecords()
  })
  document.querySelector('#lookup-form').addEventListener('submit', (event) => { event.preventDefault(); const id = readForm(event.target).id; if (id) loadRecords(`/bois/${id}`) })
}

function editRecord(item) {
  document.querySelector('#edit-area').innerHTML = `<section class="panel edit-panel"><div class="panel-title"><h2>Editar avaliação #${item.id}</h2><button class="close" id="close-edit">×</button></div><form id="edit-form">${formFields(item)}<div class="actions"><button class="primary">Atualizar e recalcular</button></div></form></section>`
  document.querySelector('#close-edit').addEventListener('click', () => { document.querySelector('#edit-area').innerHTML = '' })
  document.querySelector('#edit-form').addEventListener('submit', async (event) => {
    event.preventDefault()
    const data = readForm(event.target)
    try { await api(`/bois/${item.id}`, { method: 'PUT', body: JSON.stringify({ ...data, peso_kg: Number(data.peso_kg), idade_meses: Number(data.idade_meses), valor_arroba: Number(data.valor_arroba) }) }); document.querySelector('#edit-area').innerHTML = ''; loadRecords() } catch (error) { feedback('#records-feedback', error.message) }
  })
}

async function deleteRecord(id) {
  if (!window.confirm(`Excluir a avaliação #${id}?`)) return
  try { await api(`/bois/${id}`, { method: 'DELETE' }); loadRecords() } catch (error) { feedback('#records-feedback', error.message) }
}

async function loadSummary() {
  try {
    const data = await api('/bois/resumo')
    const stats = [['Avaliações', data.total_avaliacoes], ['Peso médio', `${data.peso_medio} kg`], ['Arroba média', currency(data.valor_arroba_medio)], ['Preço médio', currency(data.preco_medio)], ['Menor preço', currency(data.menor_preco)], ['Maior preço', currency(data.maior_preco)], ['Valor total', currency(data.valor_total)]]
    document.querySelector('#summary-content').innerHTML = `<div class="stats">${stats.map(([label, value]) => `<div class="stat"><span>${label}</span><strong>${value}</strong></div>`).join('')}</div><div class="summary-columns"><div class="summary-list"><h2>Por categoria</h2>${summaryRows(data.por_categoria, 'categoria')}</div><div class="summary-list"><h2>Por raça</h2>${summaryRows(data.por_raca, 'raca')}</div></div>`
  } catch (error) { feedback('#summary-content', error.message) }
}

function summaryRows(items = [], name) {
  return items.length ? items.map((item) => `<div class="summary-row"><div><strong>${escapeHTML(item[name])}</strong><span>${item.quantidade} avaliações · ${item.peso_medio} kg médios</span></div><strong>${currency(item.preco_medio)}</strong></div>`).join('') : '<p class="empty">Sem dados.</p>'
}

window.addEventListener('popstate', () => { view = getView(); render() })
render()
