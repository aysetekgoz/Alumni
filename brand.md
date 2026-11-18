# Brand Guidelines — İÜ YBS Mezun Takip Sistemi

**İstanbul Üniversitesi — Yönetim Bilişim Sistemleri (YBS / MIS)** bölümü mezun takip ve kariyer ekosistemi için hazırlanmış premium, veri odaklı ve kurumsal tasarım rehberidir.

> **Tasarım Felsefesi — "Academic Prestige meets Modern MIS Precision"**  
> 1453'ten gelen İstanbul Üniversitesi akademik mirasını, Yönetim Bilişim Sistemleri'nin analitik, stratejik ve teknoloji lideri kimliğiyle birleştirir. Gösterişli neon efektler yerine **yüksek kontrastlı koyu yüzeyler, ölçülü altın/bordo kurumsal dokunuşlar ve net veri hiyerarşisi** esas alınır.

---

## 1. Marka Kimliği ve Konumlandırma

* **Kurum:** İstanbul Üniversitesi • İşletme / Siyasal / İktisat eksenli **Yönetim Bilişim Sistemleri (MIS)** Ekosistemi
* **Platform Adı:** **İÜ YBS Alumni** — *Mezun Takip ve Kariyer Platformu*
* **Logo & Amblem Konsepti:**
  * Minimalist akademik kep + bağlantılı veri düğümü (network node) silüeti.
  * `38px × 38px` yuvarlatılmış kare (`border-radius: 10px`), derin lacivert zemin (`#0F172A`) üzerinde **Imperial Gold (`#D4AF37`)** ince çerçeve ve monogram (`YBS` / `🎓`).
* **Ses Tonu (Tone of Voice):**
  * **Profesyonel, vizyoner ve veri odaklı:** Gereksiz süslü ifadelerden kaçınan, mezunlara ve iş dünyasına güven veren net Türkçe ifadeler.
  * **Örnek Başlık:** *"İstanbul Üniversitesi YBS Mezun Ağı ve Kariyer Ekosistemi"*
  * **Örnek Alt Metin:** *"Mezunlarımızın küresel kariyer yolculuklarını, sektörel etkilerini ve yeni nesil yeteneklerle kurduğu bağı tek bir akıllı merkezden yönetin."*

---

## 2. Kurumsal Renk Paleti — *Bosphorus Night & Imperial Gold*

İstanbul Üniversitesi'nin köklü **bordo-altın** mirası ile Yönetim Bilişim Sistemleri'nin **safir-mavi dijital** kimliğini dengeleyen özel palet:

### Zemin ve Yüzey Katmanları (Dark Executive Surfaces)

| Token | Değer | Kullanım Alanı |
| :--- | :--- | :--- |
| `--bg-canvas` | `#070B14` | Ana sayfa zemini (Bosphorus Obsidian) |
| `--bg-gradient` | `radial-gradient(circle at 15% 15%, #131C31 0%, #070B14 55%)` | Derinlikli arka plan geçişi |
| `--surface-card` | `rgba(17, 25, 40, 0.72)` (`backdrop-filter: blur(16px)`) | Ana kartlar, Bento panelleri |
| `--surface-elevated` | `rgba(26, 36, 58, 0.85)` | Hover durumu, açılır menüler, modal yüzeyler |
| `--surface-input` | `rgba(7, 11, 20, 0.75)` | Form alanları ve tablo satırları |
| `--border-subtle` | `rgba(148, 163, 184, 0.14)` | Standart `1px` hairline kart kenarlıkları |
| `--border-gold` | `rgba(212, 175, 55, 0.35)` | Öne çıkan kurumsal/prestij kart çerçeveleri |

### Marka ve Vurgu Renkleri

| Token | Hex | Kullanım Alanı |
| :--- | :--- | :--- |
| `--brand-sapphire` | `#2563EB` | Birincil CTA butonları, aktif bağlantılar, focus halkaları |
| `--brand-sapphire-glow` | `#38BDF8` | Veri grafikleri, ince link vurguları, ikincil ikon parlamaları |
| `--iu-crimson` | `#8B1E3F` | İstanbul Üniversitesi kurumsal rozetleri ve ince vurgu şeritleri |
| `--iu-gold` | `#D4AF37` | Mezuniyet yılı rozetleri, üst düzey KPI vurguları, premium detaylar |
| `--iu-gold-soft` | `rgba(212, 175, 55, 0.14)` | Altın rozet arka planları |

### Metin ve Semantik Renkler

| Token | Hex | Kullanım Alanı |
| :--- | :--- | :--- |
| `--text-primary` | `#F8FAFC` | Ana başlıklar ve yüksek öncelikli metinler |
| `--text-secondary` | `#CBD5E1` | Kart açıklamaları ve tablo içerikleri |
| `--text-muted` | `#64748B` | Yardımcı etiketler, tarih ve meta veriler |
| `--status-success` | `#10B981` | Aktif sistem/ilan durumu, olumlu trendler |
| `--status-warning` | `#F59E0B` | İnceleme bekleyen başvurular |
| `--status-danger` | `#F43F5E` | Hata durumları (`404` / `500` Guardian) |

---

## 3. Tipografi Sistemi

YBS'nin analitik yapısını yansıtmak için **geometrik okunabilirlik** ve **sayısal hizalama (`tabular-nums`)** ön plandadır:

* **Display & Başlıklar:** `'Plus Jakarta Sans', system-ui, sans-serif` (Ağırlık: `700`, `800`, sıkı harf aralığı `-0.025em`)
* **Gövde Metni:** `'Inter', 'Plus Jakarta Sans', sans-serif` (Ağırlık: `400`, `500`, `600`, satır yüksekliği `1.65`)
* **Teknik & Sayısal Veriler (KPI, API, Mezuniyet Yılı):** `'JetBrains Mono', monospace` (`font-variant-numeric: tabular-nums`)

| Seviye | Boyut | Ağırlık | Kullanım |
| :--- | :--- | :--- | :--- |
| `Hero Display` | `clamp(2.25rem, 4.5vw, 3.5rem)` | `800` | Ana sayfa manşet başlığı |
| `Section H2` | `1.5rem` (`24px`) | `700` | Bölüm başlıkları |
| `Card H3` | `1.125rem` (`18px`) | `700` | Modül ve ilan kart başlıkları |
| `KPI Metric` | `2rem` (`32px`) | `800` | Mezun/İlan sayaçları (`tabular-nums`) |
| `Body` | `0.95rem` (`15.2px`) | `400`–`500` | Açıklamalar ve içerik |
| `Micro / Badge` | `0.75rem` (`12px`) | `700` | Durum rozetleri, üst etiketler (`uppercase`, `letter-spacing: 0.06em`) |

---

## 4. YBS Odaklı Bileşen ve Düzen Standartları

### A. Bento Grid Modül & KPI Yapısı
* Dashboard ve ana sayfada simetrik **Bento Grid** düzeni (`gap: 1.25rem`, `border-radius: 16px`).
* Her KPI kartı sol üstte küçük bir kategori ikonu, ortada `JetBrains Mono` / `tabular-nums` formatında net sayı ve altta kısa açıklama içerir.

### B. Buton Hiyerarşisi
1. **Primary Action (Sapphire):** `#2563EB` → hover `#1D4ED8`, `border-radius: 10px`, yumuşak gölge (`0 8px 20px rgba(37, 99, 235, 0.3)`).
2. **Institutional Prestige (Gold Outline):** `rgba(212, 175, 55, 0.08)` zemin, `1px solid rgba(212, 175, 55, 0.4)` kenarlık, `#FDE68A` metin — öne çıkan mezuniyet veya kariyer aksiyonları için.
3. **Ghost / Secondary:** `rgba(255, 255, 255, 0.05)` zemin, `1px solid var(--border-subtle)`.

### C. Kurumsal Üst Bilgi & Gezinme (`_navbar.html`)
* Sticky `backdrop-filter: blur(16px)` üst bar, alt kenarda `1px solid rgba(212, 175, 55, 0.18)` ince altın-füme ayırıcı çizgi.
* Aktif sayfa bağlantısı alt çizgi veya yumuşak safir hap (`rgba(37, 99, 235, 0.18)`) ile vurgulanır.

### D. İkonografi
* Tüm arayüzde tutarlı `1.5px` stroke kalınlığına sahip minimal vektör ikonlar (Lucide / Heroicons stili) tercih edilir; emojiler yalnızca hızlı prototipleme veya durum göstergesi olarak sınırlı tutulur.

---

## 5. Hazır CSS Design Tokens (`:root`)

Şablonlarda (`views/templates/*.html`) doğrudan kullanılabilecek referans değişken bloğu:

```css
:root {
    /* Surfaces */
    --bg-canvas: #070b14;
    --bg-gradient: radial-gradient(circle at 15% 15%, #131c31 0%, #070b14 55%);
    --surface-card: rgba(17, 25, 40, 0.72);
    --surface-elevated: rgba(26, 36, 58, 0.85);
    --surface-input: rgba(7, 11, 20, 0.75);
    --border-subtle: rgba(148, 163, 184, 0.14);
    --border-gold: rgba(212, 175, 55, 0.35);

    /* Brand */
    --brand-sapphire: #2563eb;
    --brand-sapphire-hover: #1d4ed8;
    --brand-cyan: #38bdf8;
    --iu-crimson: #8b1e3f;
    --iu-gold: #d4af37;
    --iu-gold-soft: rgba(212, 175, 55, 0.14);

    /* Typography */
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --font-sans: 'Plus Jakarta Sans', 'Inter', system-ui, -apple-system, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, monospace;

    /* Status */
    --status-success: #10b981;
    --status-warning: #f59e0b;
    --status-danger: #f43f5e;
}
```
