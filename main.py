from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Alumni Tracking System")

LANDING_PAGE_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Alumni Tracking System - Mezun Takip Sistemi</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --badge-bg: rgba(99, 102, 241, 0.2);
            --badge-border: rgba(99, 102, 241, 0.4);
            --badge-text: #a5b4fc;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow-x: hidden;
        }

        .glow-1 {
            position: absolute;
            top: 10%;
            left: 20%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
            z-index: 0;
            pointer-events: none;
        }

        .glow-2 {
            position: absolute;
            bottom: 15%;
            right: 15%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 70%);
            z-index: 0;
            pointer-events: none;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
            position: relative;
            z-index: 1;
            width: 100%;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 2rem;
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--card-border);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            text-decoration: none;
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #6366f1, #38bdf8);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }

        .nav-links {
            display: flex;
            gap: 1rem;
            align-items: center;
        }

        .nav-btn {
            padding: 0.5rem 1.1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .nav-btn-link {
            color: var(--text-muted);
        }

        .nav-btn-link:hover {
            color: #ffffff;
        }

        .nav-btn-docs {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid var(--card-border);
        }

        .nav-btn-docs:hover {
            background: rgba(255, 255, 255, 0.18);
            transform: translateY(-1px);
        }

        .hero {
            text-align: center;
            padding: 3.5rem 1rem 2.5rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            background: var(--badge-bg);
            border: 1px solid var(--badge-border);
            color: var(--badge-text);
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #22c55e;
            border-radius: 50%;
            box-shadow: 0 0 8px #22c55e;
        }

        .hero h1 {
            font-size: 2.8rem;
            font-weight: 800;
            line-height: 1.2;
            margin-bottom: 1.2rem;
            background: linear-gradient(to right, #ffffff, #cbd5e1, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .hero p {
            font-size: 1.15rem;
            color: var(--text-muted);
            max-width: 650px;
            margin: 0 auto 2.5rem;
            line-height: 1.7;
        }

        .cta-group {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.85rem 1.8rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            color: #ffffff;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(79, 70, 229, 0.6);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid var(--card-border);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        .endpoints-section {
            margin-top: 1.5rem;
        }

        .endpoints-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            padding: 1.75rem;
            backdrop-filter: blur(16px);
        }

        .endpoints-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--card-border);
        }

        .endpoints-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
        }

        .endpoints-list {
            display: grid;
            gap: 0.75rem;
        }

        .endpoint-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 1.1rem;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: inherit;
        }

        .endpoint-item:hover {
            border-color: rgba(99, 102, 241, 0.4);
            background: rgba(30, 41, 59, 0.8);
            transform: translateX(4px);
        }

        .endpoint-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .method-badge {
            background: #10b981;
            color: #ffffff;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 0.25rem 0.55rem;
            border-radius: 6px;
        }

        .endpoint-path {
            font-family: monospace;
            font-size: 0.95rem;
            color: #e2e8f0;
        }

        .endpoint-desc {
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .endpoint-action {
            color: var(--accent);
            font-size: 0.85rem;
            font-weight: 600;
        }

        footer {
            text-align: center;
            padding: 2rem 1rem;
            border-top: 1px solid var(--card-border);
            color: var(--text-muted);
            font-size: 0.875rem;
            background: rgba(15, 23, 42, 0.5);
            margin-top: 2rem;
        }

        @media (max-width: 640px) {
            .hero h1 {
                font-size: 2.1rem;
            }
            .endpoint-item {
                flex-direction: column;
                align-items: flex-start;
                gap: 0.5rem;
            }
            .endpoint-action {
                align-self: flex-end;
            }
        }
    </style>
</head>
<body>
    <div class="glow-1"></div>
    <div class="glow-2"></div>

    <nav>
        <a href="/" class="logo">
            <div class="logo-icon">🎓</div>
            <span>Alumni Tracking System</span>
        </a>
        <div class="nav-links">
            <a href="/about" class="nav-btn nav-btn-link">Hakkında</a>
            <a href="/docs" target="_blank" class="nav-btn nav-btn-docs">Swagger UI (/docs)</a>
        </div>
    </nav>

    <div class="container">
        <section class="hero">
            <div class="badge">
                <span class="pulse-dot"></span>
                Geçici Ana Sayfa • Temporary Main Page
            </div>
            <h1>İstanbul Üniversitesi<br>Mezun Takip Sistemi</h1>
            <p>Web Programlama dersi kapsamında geliştirilen FastAPI tabanlı mezun takip ve yönetim platformu. Backend servislerimiz aktif olarak çalışmaktadır.</p>
            <div class="cta-group">
                <a href="/docs" target="_blank" class="btn btn-primary">
                    <span>📖 API Dökümantasyonunu Aç</span>
                </a>
                <a href="/about" class="btn btn-secondary">
                    <span>ℹ️ Proje Hakkında</span>
                </a>
            </div>
        </section>

        <section class="endpoints-section">
            <div class="endpoints-card">
                <div class="endpoints-header">
                    <span class="endpoints-title">Aktif API Uç Noktaları (Routes)</span>
                    <span style="color: #10b981; font-size: 0.85rem; font-weight: 600;">● Sistem Aktif</span>
                </div>
                <div class="endpoints-list">
                    <a href="/" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge">GET</span>
                            <span class="endpoint-path">/</span>
                            <span class="endpoint-desc">- Geçici Ana Sayfa (Landing Page)</span>
                        </div>
                        <span class="endpoint-action">Mevcut Sayfa</span>
                    </a>
                    <a href="/about" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge">GET</span>
                            <span class="endpoint-path">/about</span>
                            <span class="endpoint-desc">- Geçici Hakkında Sayfası (About Page)</span>
                        </div>
                        <span class="endpoint-action">Git ↗</span>
                    </a>
                    <a href="/hello" target="_blank" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge">GET</span>
                            <span class="endpoint-path">/hello</span>
                            <span class="endpoint-desc">- "Hello World!" mesajı döner</span>
                        </div>
                        <span class="endpoint-action">Dene ↗</span>
                    </a>
                    <a href="/hello/ayse" target="_blank" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge">GET</span>
                            <span class="endpoint-path">/hello/{name}</span>
                            <span class="endpoint-desc">- İsme özel dinamik selamlama</span>
                        </div>
                        <span class="endpoint-action">Dene ↗</span>
                    </a>
                    <a href="/sum/15/25" target="_blank" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge">GET</span>
                            <span class="endpoint-path">/sum/{number1}/{number2}</span>
                            <span class="endpoint-desc">- İki sayının toplamını hesaplar</span>
                        </div>
                        <span class="endpoint-action">Dene ↗</span>
                    </a>
                    <a href="/docs" target="_blank" class="endpoint-item">
                        <div class="endpoint-info">
                            <span class="method-badge" style="background: #6366f1;">DOCS</span>
                            <span class="endpoint-path">/docs</span>
                            <span class="endpoint-desc">- Swagger arayüzü ve API test alanı</span>
                        </div>
                        <span class="endpoint-action">Aç ↗</span>
                    </a>
                </div>
            </div>
        </section>
    </div>

    <footer>
        <p>İstanbul Üniversitesi • Web Programlama Dersi • Alumni Tracking System</p>
    </footer>
</body>
</html>
"""

ABOUT_PAGE_HTML = """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hakkında - Alumni Tracking System</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
            --card-bg: rgba(255, 255, 255, 0.05);
            --card-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #38bdf8;
            --badge-bg: rgba(99, 102, 241, 0.2);
            --badge-border: rgba(99, 102, 241, 0.4);
            --badge-text: #a5b4fc;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
            background: var(--bg-gradient);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow-x: hidden;
        }

        .glow-1 {
            position: absolute;
            top: 10%;
            left: 15%;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
            z-index: 0;
            pointer-events: none;
        }

        .glow-2 {
            position: absolute;
            bottom: 20%;
            right: 15%;
            width: 450px;
            height: 450px;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.12) 0%, transparent 70%);
            z-index: 0;
            pointer-events: none;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
            position: relative;
            z-index: 1;
            width: 100%;
        }

        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.2rem 2rem;
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--card-border);
            position: sticky;
            top: 0;
            z-index: 10;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            text-decoration: none;
        }

        .logo-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #6366f1, #38bdf8);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
        }

        .nav-links {
            display: flex;
            gap: 1.25rem;
            align-items: center;
        }

        .nav-btn {
            padding: 0.5rem 1.1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
        }

        .nav-btn-link {
            color: var(--text-muted);
        }

        .nav-btn-link:hover {
            color: #ffffff;
        }

        .nav-btn-docs {
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            border: 1px solid var(--card-border);
        }

        .nav-btn-docs:hover {
            background: rgba(255, 255, 255, 0.18);
        }

        .about-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2.5rem;
            backdrop-filter: blur(16px);
            margin-top: 1rem;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.4rem 1rem;
            border-radius: 9999px;
            background: var(--badge-bg);
            border: 1px solid var(--badge-border);
            color: var(--badge-text);
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #38bdf8;
            border-radius: 50%;
            box-shadow: 0 0 8px #38bdf8;
        }

        h1 {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 1rem;
            background: linear-gradient(to right, #ffffff, #cbd5e1, #a5b4fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .lead {
            font-size: 1.15rem;
            color: var(--text-muted);
            line-height: 1.7;
            margin-bottom: 2rem;
        }

        .grid-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.25rem;
            margin-bottom: 2.5rem;
        }

        .feature-box {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.2s ease;
        }

        .feature-box:hover {
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
        }

        .feature-icon {
            font-size: 1.8rem;
            margin-bottom: 0.75rem;
        }

        .feature-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.5rem;
        }

        .feature-text {
            color: var(--text-muted);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.85rem 1.8rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1rem;
            text-decoration: none;
            transition: all 0.25s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            color: #ffffff;
            box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(79, 70, 229, 0.6);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid var(--card-border);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
            transform: translateY(-2px);
        }

        .actions-group {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        footer {
            text-align: center;
            padding: 2rem 1rem;
            border-top: 1px solid var(--card-border);
            color: var(--text-muted);
            font-size: 0.875rem;
            background: rgba(15, 23, 42, 0.5);
        }
    </style>
</head>
<body>
    <div class="glow-1"></div>
    <div class="glow-2"></div>

    <nav>
        <a href="/" class="logo">
            <div class="logo-icon">🎓</div>
            <span>Alumni Tracking System</span>
        </a>
        <div class="nav-links">
            <a href="/" class="nav-btn nav-btn-link">Ana Sayfa</a>
            <a href="/about" class="nav-btn nav-btn-link" style="color: #ffffff; font-weight: 700;">Hakkında</a>
            <a href="/docs" target="_blank" class="nav-btn nav-btn-docs">Swagger UI (/docs)</a>
        </div>
    </nav>

    <div class="container">
        <div class="about-card">
            <div class="badge">
                <span class="pulse-dot"></span>
                Geçici Hakkında Sayfası • Temporary About Page
            </div>
            <h1>Proje Hakkında</h1>
            <p class="lead">
                Bu platform, <strong>İstanbul Üniversitesi Web Programlama</strong> dersi kapsamında geliştirilen bir <strong>Mezun Takip Sistemi (Alumni Tracking System)</strong> projesidir. Üniversitemiz mezunlarının kariyer yolculuklarını izlemek, mezunlar ve öğrenciler arasında güçlü bir bağ kurmak amacıyla tasarlanmaktadır.
            </p>

            <div class="grid-features">
                <div class="feature-box">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">Projenin Amacı</div>
                    <div class="feature-text">Mezunlarımızın kariyer durumlarını, sektör tercihlerini ve başarılarını tek bir merkezden izlemek ve güçlü bir iletişim ağı oluşturmak.</div>
                </div>

                <div class="feature-box">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Teknoloji Altyapısı</div>
                    <div class="feature-text">Backend tarafında FastAPI (Python), veri yönetiminde PostgreSQL ve SQLAlchemy ORM, dağıtımda Docker konteynerleri kullanılmaktadır.</div>
                </div>

                <div class="feature-box">
                    <div class="feature-icon">🏗️</div>
                    <div class="feature-title">Katmanlı Mimari</div>
                    <div class="feature-text">API, iş mantığı (business logic) ve veri erişim katmanları birbirinden ayrı sorumluluklarla kademeli olarak geliştirilmektedir.</div>
                </div>
            </div>

            <div class="actions-group">
                <a href="/" class="btn btn-primary">
                    <span>← Ana Sayfaya Dön</span>
                </a>
                <a href="/docs" target="_blank" class="btn btn-secondary">
                    <span>📖 API Dökümantasyonu</span>
                </a>
            </div>
        </div>
    </div>

    <footer>
        <p>İstanbul Üniversitesi • Web Programlama Dersi • Alumni Tracking System</p>
    </footer>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def read_root():
    return LANDING_PAGE_HTML


@app.get("/about", response_class=HTMLResponse)
def read_about():
    return ABOUT_PAGE_HTML


@app.get("/hello")
def hello():
    return "Hello World!"


@app.get("/hello/{name}")
def hello_name(name: str):
    return f"Hello {name}!"


@app.get("/sum/{number1}/{number2}")
def sum_numbers(number1: int, number2: int):
    return number1 + number2


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
