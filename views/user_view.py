import os
from typing import Any, Dict, List, Optional
from fastapi import Request
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

try:
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
    HAS_JINJA = True
except Exception:
    HAS_JINJA = False
    templates = None


class UserView:
    """
    UserView — MVC Mimarisi View Katmanı (View Layer).
    Kullanıcı verilerinin HTML arayüz olarak sunulmasından ve şablon (template)
    giydirilmesinden sorumludur. İş mantığı içermez.
    """

    @staticmethod
    def render_list(
        request: Request,
        users: List[Dict[str, Any]],
        message: Optional[str] = None,
        status_code: int = 200,
    ) -> HTMLResponse:
        """
        Kullanıcı listesini ve oluşturma formunu içeren HTML görünümünü render eder.
        GET .../users (listing - R) ve POST .../users (creating - C) için sunum sağlar.
        """
        if HAS_JINJA and templates:
            return templates.TemplateResponse(
                request,
                "users.html",
                {
                    "users": users,
                    "message": message,
                },
                status_code=status_code,
            )

        # Jinja2 yüklü olmadığında güvenli HTML fallback render
        template_file = os.path.join(TEMPLATES_DIR, "users.html")
        if os.path.exists(template_file):
            with open(template_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "<h1>Mezun Listesi</h1>"

        # Şablonu temel Python metin değişimiyle hazırla
        msg_html = f'<div class="alert-success"><span>✅</span><span>{message}</span></div>' if message else ""
        content = content.replace("{% if message %}", "").replace("{% endif %}", "")
        content = content.replace("{{ message }}", msg_html)

        cards = []
        for u in users:
            cards.append(f"""
            <div class="user-card">
                <div class="user-name">{u.get('first_name', '')} {u.get('last_name', '')}</div>
                <div class="user-badge">🎓 Mezuniyet: {u.get('graduation_year', '-')}</div>
                <div class="user-info"><strong>Bölüm:</strong> {u.get('department', '-')}</div>
                <div class="user-info"><strong>E-Posta:</strong> {u.get('email', '-')}</div>
                <div class="user-info"><strong>ID:</strong> #{u.get('id', '-')}</div>
            </div>
            """)
        cards_html = "".join(cards) if cards else '<div class="empty-state">Henüz kayıtlı mezun bulunmuyor.</div>'
        
        # Basit Jinja for döngüsünü temizle ve kartları yerleştir
        import re
        content = re.sub(r'\{%\s*for\s+u\s+in\s+users\s*%\}.*?\{%\s*endfor\s*%\}', cards_html, content, flags=re.DOTALL)
        content = re.sub(r'\{%\s*if\s+users\s+and\s+users\|length\s*>\s*0\s*%\}(.*?)\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}', r'\1' if users else r'\2', content, flags=re.DOTALL)

        return HTMLResponse(content=content, status_code=status_code)
