import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:5000'
const go = (path) => { window.history.pushState({}, '', path); window.dispatchEvent(new PopStateEvent('popstate')) }
const currency = (value) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(Number(value || 0))

function Header() { return <header className="topbar"><a className="brand" href="/" onClick={(e) => { e.preventDefault(); go('/') }}><span className="brand-mark">✦</span> Agro<span>logic</span></a><nav><a href="#">Mercado</a><a href="#">Negócios</a><a href="#">Leilões</a></nav><div className="header-actions"><button className="small-btn light" onClick={() => go('/negociar')}>Calcular</button></div></header> }
function Footer() { return <footer><span>◈ Agrologic</span><span>Mercado</span><span>Negociar</span><span>Leilões</span><span>Relatórios</span><span>Ajuda</span></footer> }
function Shell({ children }) { return <div className="site"><Header />{children}<Footer /></div> }
function Home() {
  return <Shell><main className="home"><section className="hero"><div className="hero-copy"><p className="eyebrow">A tecnologia que conecta o campo</p><h1>Bem-vindo ao <strong>Agrologic!</strong></h1><p>Calcule o valor estimado do seu boi com base no mercado e na arroba atual.</p><button className="primary" onClick={() => go('/negociar')}>✦ CALCULAR PREÇO</button><div className="hero-links"><span>◉ PESO</span><span>▣ ARROBA</span><span>▤ PREÇO</span><span>◫ ANÁLISE</span></div></div></section><section className="feature-grid"><Feature title="Cálculo do boi" text="Estime o valor do animal com base no peso e na arroba." action="IR PARA CALCULADORA" path="/negociar" image="cattle"/><Feature title="Registro" text="Salve avaliações e consulte os resultados no backend." action="VER FUNCIONALIDADE" image="market"/><Feature title="Leilões & Eventos" text="Acompanhe oportunidades do setor pecuário." action="CONSULTAR" image="auction"/></section></main></Shell>
}
function Feature({ title, text, action, path, image }) { return <article className={`feature ${image}`}><div><h2>{title}</h2><p>{text}</p><button onClick={() => path && go(path)}>{action} ↗</button></div></article> }
function Negotiate() {
  const initialForm = { raca: 'Nelore', categoria: 'Boi Gordo', peso_kg: '480', idade_meses: '36', valor_arroba: '300' }
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [saved, setSaved] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (field) => (event) => {
    setForm((current) => ({ ...current, [field]: event.target.value }))
  }

  const handleCalculate = async (event) => {
    event.preventDefault()
    setError('')
    setSaved(null)
    setLoading(true)

    try {
      const payload = {
        raca: form.raca,
        categoria: form.categoria,
        peso_kg: Number(form.peso_kg),
        idade_meses: Number(form.idade_meses),
        valor_arroba: Number(form.valor_arroba),
      }

      const response = await fetch(`${API_URL}/bois/calcular`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.erro || 'Erro ao calcular preço do boi.')
      setResult(data)
    } catch (err) {
      setError(err.message)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    if (!result) return

    try {
      const response = await fetch(`${API_URL}/bois`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          raca: form.raca,
          categoria: form.categoria,
          peso_kg: Number(form.peso_kg),
          idade_meses: Number(form.idade_meses),
          valor_arroba: Number(form.valor_arroba),
        }),
      })

      const data = await response.json()
      if (!response.ok) throw new Error(data.erro || 'Erro ao salvar avaliação.')
      setSaved(data)
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  return <Shell><main className="negotiate"><div className="negotiate-copy"><p className="eyebrow">Mercado em tempo real</p><h1>Negociar <strong>agora</strong></h1><p>Use a calculadora oficial do backend para estimar o valor do seu boi.</p><form className="calculator" onSubmit={handleCalculate}><div className="calculator-header"><h2>Calculadora do boi</h2><p>Estime o valor com base no mercado.</p></div><div className="form-grid"><div className="form-group"><label>Raça</label><input value={form.raca} onChange={handleChange('raca')} /></div><div className="form-group"><label>Categoria</label><input value={form.categoria} onChange={handleChange('categoria')} /></div><div className="form-group"><label>Peso (kg)</label><input type="number" value={form.peso_kg} onChange={handleChange('peso_kg')} /></div><div className="form-group"><label>Idade (meses)</label><input type="number" value={form.idade_meses} onChange={handleChange('idade_meses')} /></div><div className="form-group"><label>Valor da arroba</label><input type="number" step="0.01" value={form.valor_arroba} onChange={handleChange('valor_arroba')} /></div></div><div className="calculator-actions"><button type="submit" className="primary" disabled={loading}>{loading ? 'Calculando...' : 'Calcular preço'}</button></div>{error ? <p className="calculator-error">{error}</p> : null}{result ? <div className="result-box"><div><span>Peso</span><strong>{result.peso_kg} kg</strong></div><div><span>Valor da arroba</span><strong>{currency(result.valor_arroba)}</strong></div><div><span>Preço estimado</span><strong>{currency(result.preco_estimado)}</strong></div></div> : null}{saved ? <p className="calculator-success">Avaliação salva com sucesso: {currency(saved.preco_estimado)}.</p> : null}{result ? <button type="button" className="outline calculator-save" onClick={handleSave}>Salvar avaliação</button> : null}</form></div></main></Shell> }
export default function App() { const [path, setPath] = useState(window.location.pathname); window.onpopstate = () => setPath(window.location.pathname); return path === '/negociar' ? <Negotiate/> : <Home/> }
