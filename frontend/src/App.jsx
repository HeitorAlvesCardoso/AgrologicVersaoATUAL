import { useEffect, useState } from 'react'
import './App.css'

const API_URL = ''
const emptyForm = { raca: '', categoria: '', peso_kg: '', idade_meses: '', valor_arroba: '' }
const currency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))

async function api(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options })
  const data = response.status === 204 ? null : await response.json()
  if (!response.ok) throw new Error(data?.erro || 'Não foi possível concluir a operação.')
  return data
}

function Header({ view, setView }) {
  const links = [['dashboard', 'Início'], ['calculator', 'Calcular'], ['records', 'Avaliações'], ['summary', 'Resumo']]
  return <header className="topbar"><button className="brand" onClick={() => setView('dashboard')}><span className="brand-mark">✦</span> Agro<span>logic</span></button><nav>{links.map(([key, label]) => <button key={key} className={view === key ? 'nav-btn active' : 'nav-btn'} onClick={() => setView(key)}>{label}</button>)}</nav></header>
}

function Field({ label, name, form, setForm, type = 'text', step }) {
  return <label className="field"><span>{label}</span><input type={type} step={step} value={form[name]} onChange={(event) => setForm({ ...form, [name]: event.target.value })} required /></label>
}

function FormFields({ form, setForm }) {
  return <div className="form-grid"><Field label="Raça" name="raca" form={form} setForm={setForm} /><Field label="Categoria" name="categoria" form={form} setForm={setForm} /><Field label="Peso (kg)" name="peso_kg" form={form} setForm={setForm} type="number" /><Field label="Idade (meses)" name="idade_meses" form={form} setForm={setForm} type="number" /><Field label="Valor da arroba" name="valor_arroba" form={form} setForm={setForm} type="number" step="0.01" /></div>
}

function Dashboard({ setView }) {
  return <main className="dashboard"><section className="hero"><div><p className="eyebrow">Gestão pecuária conectada ao backend</p><h1>Agrologic para decisões melhores.</h1><p>Calcule, salve, consulte e acompanhe as avaliações reais do seu gado em um só lugar.</p><button className="primary" onClick={() => setView('calculator')}>Calcular valor do boi</button></div></section><section className="feature-grid"><article><span>01</span><h2>Calcule</h2><p>Use peso e valor da arroba para obter uma estimativa imediata.</p><button onClick={() => setView('calculator')}>Abrir calculadora →</button></article><article><span>02</span><h2>Gerencie</h2><p>Cadastre, edite, consulte e exclua avaliações persistidas no banco.</p><button onClick={() => setView('records')}>Ver avaliações →</button></article><article><span>03</span><h2>Entenda</h2><p>Leia médias, mínimos, máximos e agrupamentos por raça e categoria.</p><button onClick={() => setView('summary')}>Ver resumo →</button></article></section></main>
}

function Calculator({ onSaved }) {
  const [form, setForm] = useState({ ...emptyForm, raca: 'Nelore', categoria: 'Boi Gordo', peso_kg: '480', idade_meses: '36', valor_arroba: '300' })
  const [result, setResult] = useState(null); const [message, setMessage] = useState(''); const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const calculate = async (event) => { event.preventDefault(); setLoading(true); setError(''); setMessage(''); try { setResult(await api('/bois/calcular', { method: 'POST', body: JSON.stringify({ peso_kg: Number(form.peso_kg), valor_arroba: Number(form.valor_arroba) }) })) } catch (err) { setError(err.message) } finally { setLoading(false) } }
  const save = async () => { setLoading(true); setError(''); setMessage(''); try { const saved = await api('/bois', { method: 'POST', body: JSON.stringify({ ...form, peso_kg: Number(form.peso_kg), idade_meses: Number(form.idade_meses), valor_arroba: Number(form.valor_arroba) }) }); setMessage(`Avaliação #${saved.id} salva com sucesso.`); onSaved() } catch (err) { setError(err.message) } finally { setLoading(false) } }
  return <main className="page"><section className="panel calculator-panel"><p className="eyebrow">POST /bois/calcular</p><h1>Calcular valor do boi</h1><p className="intro">A fórmula do backend converte o peso em arrobas e multiplica pelo valor informado.</p><form onSubmit={calculate}><FormFields form={form} setForm={setForm} /><div className="actions"><button className="primary" disabled={loading}>{loading ? 'Processando...' : 'Calcular estimativa'}</button>{result && <button type="button" className="secondary" onClick={save} disabled={loading}>Salvar avaliação</button>}</div></form>{error && <p className="error">{error}</p>}{message && <p className="success">{message}</p>}{result && <div className="result-box"><div><span>Peso</span><strong>{result.peso_kg} kg</strong></div><div><span>Arroba</span><strong>{currency(result.valor_arroba)}</strong></div><div><span>Estimativa</span><strong>{currency(result.preco_estimado)}</strong></div></div>}</section></main>
}

function Records({ refreshKey }) {
  const [items, setItems] = useState([]); const [selected, setSelected] = useState(null); const [form, setForm] = useState(emptyForm); const [filters, setFilters] = useState({ raca: '', categoria: '', peso_min: '', peso_max: '' }); const [id, setId] = useState(''); const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const load = async (path = '/bois') => { setLoading(true); setError(''); try { const data = await api(path); const list = Array.isArray(data) ? data : data?.resultados ? data.resultados : data ? [data] : []; setItems(list) } catch (err) { setError(err.message) } finally { setLoading(false) } }
  useEffect(() => { load() }, [refreshKey])
  const filter = (event) => { event.preventDefault(); let path = '/bois'; if (filters.raca) path = `/bois/filtrar/raca?raca=${encodeURIComponent(filters.raca)}`; else if (filters.categoria) path = `/bois/filtrar/categoria?categoria=${encodeURIComponent(filters.categoria)}`; else if (filters.peso_min || filters.peso_max) { const params = new URLSearchParams(); if (filters.peso_min) params.set('peso_min', filters.peso_min); if (filters.peso_max) params.set('peso_max', filters.peso_max); path = `/bois/filtrar/peso?${params}` } load(path) }
  const findById = (event) => { event.preventDefault(); if (id) load(`/bois/${id}`) }
  const edit = (item) => { setSelected(item.id); setForm({ raca: item.raca, categoria: item.categoria, peso_kg: item.peso_kg, idade_meses: item.idade_meses, valor_arroba: item.valor_arroba }) }
  const update = async (event) => { event.preventDefault(); try { await api(`/bois/${selected}`, { method: 'PUT', body: JSON.stringify({ ...form, peso_kg: Number(form.peso_kg), idade_meses: Number(form.idade_meses), valor_arroba: Number(form.valor_arroba) }) }); setSelected(null); setForm(emptyForm); load() } catch (err) { setError(err.message) } }
  const remove = async (itemId) => { if (!window.confirm(`Excluir a avaliação #${itemId}?`)) return; try { await api(`/bois/${itemId}`, { method: 'DELETE' }); load() } catch (err) { setError(err.message) } }
  return <main className="page records-page"><section className="panel"><div className="panel-title"><div><p className="eyebrow">CRUD completo</p><h1>Avaliações cadastradas</h1></div><span className="endpoint">GET /bois</span></div><form className="filter-grid" onSubmit={filter}><input placeholder="Filtrar por raça" value={filters.raca} onChange={(e) => setFilters({ ...filters, raca: e.target.value })} /><input placeholder="Filtrar por categoria" value={filters.categoria} onChange={(e) => setFilters({ ...filters, categoria: e.target.value })} /><input type="number" placeholder="Peso mínimo" value={filters.peso_min} onChange={(e) => setFilters({ ...filters, peso_min: e.target.value })} /><input type="number" placeholder="Peso máximo" value={filters.peso_max} onChange={(e) => setFilters({ ...filters, peso_max: e.target.value })} /><button className="primary">Filtrar</button><button type="button" className="secondary" onClick={() => { setFilters({ raca: '', categoria: '', peso_min: '', peso_max: '' }); load() }}>Limpar</button></form><form className="lookup" onSubmit={findById}><input type="number" placeholder="Consultar pelo ID" value={id} onChange={(e) => setId(e.target.value)} /><button className="secondary">Consultar</button></form>{error && <p className="error">{error}</p>}{loading ? <p className="empty">Carregando...</p> : items.length === 0 ? <p className="empty">Nenhuma avaliação encontrada.</p> : <div className="table-wrap"><table><thead><tr><th>ID</th><th>Raça</th><th>Categoria</th><th>Peso</th><th>Idade</th><th>Preço estimado</th><th>Ações</th></tr></thead><tbody>{items.map((item) => <tr key={item.id}><td>#{item.id}</td><td>{item.raca}</td><td>{item.categoria}</td><td>{item.peso_kg} kg</td><td>{item.idade_meses} meses</td><td>{currency(item.preco_estimado)}</td><td><button className="table-action" onClick={() => edit(item)}>Editar</button><button className="table-action danger" onClick={() => remove(item.id)}>Excluir</button></td></tr>)}</tbody></table></div>}</section>{selected && <section className="panel edit-panel"><div className="panel-title"><h2>Editar avaliação #{selected}</h2><button className="close" onClick={() => setSelected(null)}>×</button></div><form onSubmit={update}><FormFields form={form} setForm={setForm} /><div className="actions"><button className="primary">Atualizar e recalcular</button><button type="button" className="secondary" onClick={() => setSelected(null)}>Cancelar</button></div></form></section>}</main>
}

function Summary() {
  const [data, setData] = useState(null); const [error, setError] = useState('')
  useEffect(() => { api('/bois/resumo').then(setData).catch((err) => setError(err.message)) }, [])
  if (error) return <main className="page"><section className="panel"><p className="error">{error}</p></section></main>
  if (!data) return <main className="page"><section className="panel"><p className="empty">Carregando resumo...</p></section></main>
  const stats = [['Avaliações', data.total_avaliacoes], ['Peso médio', `${data.peso_medio} kg`], ['Arroba média', currency(data.valor_arroba_medio)], ['Preço médio', currency(data.preco_medio)], ['Menor preço', currency(data.menor_preco)], ['Maior preço', currency(data.maior_preco)], ['Valor total', currency(data.valor_total)]]
  return <main className="page"><section className="panel"><div className="panel-title"><div><p className="eyebrow">GET /bois/resumo</p><h1>Resumo das avaliações</h1></div></div><div className="stats">{stats.map(([label, value]) => <div className="stat" key={label}><span>{label}</span><strong>{value}</strong></div>)}</div><div className="summary-columns"><SummaryList title="Por categoria" items={data.por_categoria || []} name="categoria" /><SummaryList title="Por raça" items={data.por_raca || []} name="raca" /></div></section></main>
}

function SummaryList({ title, items, name }) { return <div className="summary-list"><h2>{title}</h2>{items.length === 0 ? <p className="empty">Sem dados.</p> : items.map((item) => <div className="summary-row" key={item[name]}><div><strong>{item[name]}</strong><span>{item.quantidade} avaliações · {item.peso_medio} kg médios</span></div><strong>{currency(item.preco_medio)}</strong></div>)}</div> }

export default function App() {
  const route = window.location.pathname; const initialView = route === '/negociar' ? 'calculator' : route === '/resumo' ? 'summary' : route === '/listar' ? 'records' : 'dashboard'; const [view, setView] = useState(initialView); const [refreshKey, setRefreshKey] = useState(0)
  useEffect(() => { const onPop = () => { const path = window.location.pathname; setView(path === '/negociar' ? 'calculator' : path === '/resumo' ? 'summary' : path === '/listar' ? 'records' : 'dashboard') }; window.addEventListener('popstate', onPop); return () => window.removeEventListener('popstate', onPop) }, [])
  const navigate = (next) => { const paths = { dashboard: '/', calculator: '/negociar', records: '/listar', summary: '/resumo' }; window.history.pushState({}, '', paths[next]); setView(next) }
  return <div className="app-shell"><Header view={view} setView={navigate} />{view === 'dashboard' && <Dashboard setView={navigate} />}{view === 'calculator' && <Calculator onSaved={() => setRefreshKey((key) => key + 1)} />}{view === 'records' && <Records refreshKey={refreshKey} />}{view === 'summary' && <Summary />}</div>
}