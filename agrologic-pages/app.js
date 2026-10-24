const API_URL = 'http://127.0.0.1:5000'
const emptyForm = { raca: '', categoria: '', peso_kg: '', idade_meses: '', valor_arroba: '' }
const currency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))
let view = getView()
let refreshKey = 0

function getView() {
  const path = window.location.pathname
  return path === '/negociar' ? 'calculator' : path === '/listar' ? 'records' : path === '/resumo' ? 'summary' : 'dashboard'
}

async function api(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  const data = response.status === 204 ? null : await response.json()
  if (!response.ok) throw new Error((data && data.erro) || 'Não foi possível concluir a operação.')
  return data
}

function navigate(next) {
  const paths = { dashboard: '/', calculator: '/negociar', records: '/listar', summary: '/resumo' }
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
  return `<main class="dashboard"><section class="hero"><div><p class="eyebrow">Gestão pecuária conectada ao backend</p><h1>Agrologic para decisões melhores.</h1><p>Calcule, salve, consulte e acompanhe as avaliações reais do seu gado em um só lugar.</p><button class="primary" data-view="calculator">Calcular valor do boi</button></div></section><section class="feature-grid"><article><span>01</span><h2>Calcule</h2><p>Use peso e valor da arroba para obter uma estimativa imediata.</p><button data-view="calculator">Abrir calculadora →</button></article><article><span>02</span><h2>Gerencie</h2><p>Cadastre, edite, consulte e exclua avaliações persistidas no banco.</p><button data-view="records">Ver avaliações →</button></article><article><span>03</span><h2>Entenda</h2><p>Leia médias, mínimos, máximos e agrupamentos por raça e categoria.</p><button data-view="summary">Ver resumo →</button></article></section></main>`
}

function field(label, name, value, type = 'text', step = '') {
  return `<label class="field"><span>${label}</span><input name="${name}" type="${type}" ${step ? `step="${step}"` : ''} value="${value ?? ''}" required></label>`
}

function formFields(form) {
  return `<div class="form-grid">${field('Raça', 'raca', form.raca)}${field('Categoria', 'categoria', form.categoria)}${field('Peso (kg)', 'peso_kg', form.peso_kg, 'number')}${field('Idade (meses)', 'idade_meses', form.idade_meses, 'number')}${field('Valor da arroba', 'valor_arroba', form.valor_arroba, 'number', '0.01')}</div>`
}

function readForm(formElement) {
  return Object.fromEntries(new FormData(formElement).entries())
}

function calculator() {
  const form = { raca: 'Nelore', categoria: 'Boi Gordo', peso_kg: '480', idade_meses: '36', valor_arroba: '300' }
  return `<main class="page"><section class="panel calculator-panel"><p class="eyebrow">POST /bois/calcular</p><h1>Calcular valor do boi</h1><p class="intro">A fórmula do backend converte o peso em arrobas e multiplica pelo valor informado.</p><form id="calculator-form">${formFields(form)}<div class="actions"><button class="primary">Calcular estimativa</button></div></form><div id="calculator-feedback"></div><div id="calculator-result"></div></section></main>`
}

function records() {
  return `<main class="page records-page"><section class="panel"><div class="panel-title"><div><p class="eyebrow">CRUD completo</p><h1>Avaliações cadastradas</h1></div><span class="endpoint">GET /bois</span></div><form id="filter-form" class="filter-grid"><input name="raca" placeholder="Filtrar por raça"><input name="categoria" placeholder="Filtrar por categoria"><input name="peso_min" type="number" placeholder="Peso mínimo"><input name="peso_max" type="number" placeholder="Peso máximo"><button class="primary">Filtrar</button><button type="button" class="secondary" id="clear-filters">Limpar</button></form><form id="lookup-form" class="lookup"><input name="id" type="number" placeholder="Consultar pelo ID"><button class="secondary">Consultar</button></form><div id="records-feedback"></div><div id="records-table"><p class="empty">Carregando...</p></div></section><div id="edit-area"></div></main>`
}

function summary() {
  return `<main class="page"><section class="panel"><div class="panel-title"><div><p class="eyebrow">GET /bois/resumo</p><h1>Resumo das avaliações</h1></div></div><div id="summary-content"><p class="empty">Carregando resumo...</p></div></section></main>`
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

async function loadRecords(path = '/bois') {
  try {
    const data = await api(path)
    const items = Array.isArray(data) ? data : data && data.resultados ? data.resultados : data ? [data] : []
    const container = document.querySelector('#records-table')
    container.innerHTML = items.length ? `<div class="table-wrap"><table><thead><tr><th>ID</th><th>Raça</th><th>Categoria</th><th>Peso</th><th>Idade</th><th>Preço estimado</th><th>Ações</th></tr></thead><tbody>${items.map(recordRow).join('')}</tbody></table></div>` : '<p class="empty">Nenhuma avaliação encontrada.</p>'
    container.querySelectorAll('[data-edit]').forEach((button) => button.addEventListener('click', () => editRecord(items.find((item) => item.id === Number(button.dataset.edit)))))
    container.querySelectorAll('[data-delete]').forEach((button) => button.addEventListener('click', () => deleteRecord(Number(button.dataset.delete))))
  } catch (error) { feedback('#records-feedback', error.message) }
}

function recordRow(item) {
  return `<tr><td>#${item.id}</td><td>${item.raca}</td><td>${item.categoria}</td><td>${item.peso_kg} kg</td><td>${item.idade_meses} meses</td><td>${currency(item.preco_estimado)}</td><td><button class="table-action" data-edit="${item.id}">Editar</button><button class="table-action danger" data-delete="${item.id}">Excluir</button></td></tr>`
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
  document.querySelector('#clear-filters').addEventListener('click', () => { document.querySelector('#filter-form').reset(); loadRecords() })
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
  return items.length ? items.map((item) => `<div class="summary-row"><div><strong>${item[name]}</strong><span>${item.quantidade} avaliações · ${item.peso_medio} kg médios</span></div><strong>${currency(item.preco_medio)}</strong></div>`).join('') : '<p class="empty">Sem dados.</p>'
}

window.addEventListener('popstate', () => { view = getView(); render() })
render()
