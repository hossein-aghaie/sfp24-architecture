"""Generate the editable, bilingual source for the presentation guide (no live data)."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'public' / 'guides'
OUT.mkdir(parents=True, exist_ok=True)

COPY = {
 'fa': {
 'title':'از تعریف کارخانه تا استفاده از داده', 'sub':'نقشهٔ راه نرم‌افزار پویشگر · ساختار محصول و مسیر داده',
 'legend':'خط پیوسته: مسیر جاری داده     ·     خط‌چین: توسعهٔ آینده     ·     مراحل تنظیمات، ترتیب پیشنهادی‌اند',
 'rows':[
 ('آماده‌سازی شرکت','تعریف محیط، دارایی‌ها و معنای داده؛ مستقل از شروع دریافت.',[
 ('ساختار و محل‌ها','کارخانه، سالن‌ها و محل استقرار','building','blue'),
 ('تجهیزات و ساختار تولید','ماشین، خط، ایستگاه و حسگر','gear','blue'),
 ('تعریف پارامترها','نام، نوع، واحد و موضوع داده','database','purple'),
 ('چیدمان کارخانه','جانمایی فیزیکی تجهیزات در صحنه','map','teal')],
 'سالن یک محل فیزیکی است؛ محدودهٔ خط، عملیات و شاخص‌ها جدا تعریف می‌شود.'),
 ('فرستنده‌های داده','داده می‌تواند از تجهیزات و سامانه‌های متفاوت برسد.',[
 ('EdgeBox پویشگر','ورودی‌های دیجیتال و شمارش دستگاه','box','blue'),
 ('تجهیزات شرکت','کنترلر، PLC یا EdgeBox دیگر','box','teal'),
 ('SCADA و نرم‌افزارها','سامانه‌های صنعتی و API','server','purple'),
 ('فایل و حسگرها','فایل داده یا درگاه حسگر هوشمند','file','amber')],
 'الگوی توسعه: هر دستگاه می‌تواند چند مسیر ارتباط و چند کانال داشته باشد؛ امروز هر منبع یک مسیر مستقل است.'),
 ('روش‌های ارتباط','در هاب، منبع و روش ارتباط متناسب با فرستنده تعریف می‌شود.',[
 ('HTTP / POST','مسیر تست‌شدهٔ EdgeBox','network','teal'),
 ('MQTT','قابل توسعه با آداپتور اجرایی','network','purple'),
 ('OPC UA / API','نیازمند آداپتور متناسب','network','blue'),
 ('ورود فایل','بسته به قالب و آداپتور ورودی','file','amber')],
 'مسیر واقعی این پایلوت: HTTP شمارش و وضعیت؛ نمایش یک پروتکل به معنی آماده‌بودن دریافت آن نیست.'),
 ('هاب داده','دریافت، نگهداری و تشخیص؛ بدون وابستگی به فرم‌های تولید.',[
 ('دریافت مجاز','شناسایی شرکت، منبع و کلید','shield','blue'),
 ('ذخیرهٔ پایدار پیام خام','پیش از پردازش سطرها؛ سپس تأیید دریافت','database','purple'),
 ('بررسی و استخراج','اعتبار، تکرار، تعارض و زمان رخداد','filter','red'),
 ('مقدار معتبر تگ','کانال ورودی ← تگ فنی + واحد و زمان','tag','teal')],
 'دادهٔ خراب با علت نگه داشته می‌شود؛ صفر معتبر است؛ نبود داده نه صفر است و نه اثبات خاموشی دستگاه.'),
 ('ذخیره و مصرف داده','هاب و برنامه مرز مسئولیت دارند؛ امروز مخزن مشترک است.',[
 ('دیتابیس همان شرکت','پیام خام و تشخیص‌ها | مقادیر معتبر تگ','database','blue'),
 ('پارامتر در برنامه','ورود دستی یا اتصال تگ با تبدیل / فرمول','gear','purple'),
 ('مصرف‌کننده‌های متعدد','یک تگ می‌تواند چند مصرف‌کننده داشته باشد','branch','teal'),
 ('مخزن خام مستقل · آینده','با آداپتور ذخیره و مهاجرت؛ هنوز فعال نیست','database','amber')],
 'اتصال تگ به پارامتر در «تعریف داده‌ها» است، بیرون هاب؛ تعریف تگ به‌تنهایی اتصال کاربردی نمی‌سازد.'),
 ('کاربردهای نرم‌افزار','مصرف‌کننده‌های موازی؛ اتصال عمومی پارامترها به ماژول‌ها مرحله‌به‌مرحله تکمیل می‌شود.',[
 ('ثبت و گزارش تولید','ورودی‌های مرتبط با ماشین و عملیات','file','blue'),
 ('پایش و OEE','زمان برنامه، کارکرد، شمارش و کیفیت','chart','teal'),
 ('هشدار و وضعیت','قواعد، کیفیت داده و تازگی ارتباط','bell','amber'),
 ('تحلیل و داشبورد','بازه، محدوده و منشأ دادهٔ مشخص','chart','purple')],
 'این ردیف نقشهٔ محصول است؛ وجود هر ماژول به معنی اتصال آمادهٔ آن به پارامتر یا دادهٔ زنده نیست.')],
 'return':'مسیر خروجی · توسعهٔ آینده',
 'returnBody':'برنامهٔ مجاز → فرمان MQTT → خروجی دستگاه → تأیید اجرا و وضعیت گزارش‌شده؛ دریافت بروکر به معنی اجرای فرمان نیست.',
 'foot':'راهنمای ارائه · تصویر شماتیک، بدون دادهٔ زنده · ساختار جاری و مسیر توسعهٔ مصوب | ۲۰۲۶/۱۰/۲۴',
 },
 'en': {
 'title':'From factory setup to useful data','sub':'Pouyeshgar software roadmap · Product structure and data flow',
 'legend':'Solid: current data path     ·     Dashed: future development     ·     Setup order is recommended',
 'rows':[
 ('Company setup','Define locations, assets and data meaning independently of reception.',[
 ('Structure & locations','Factory, halls and equipment location','building','blue'),('Equipment & production','Machines, lines, stations and sensors','gear','blue'),('Parameter definitions','Name, type, unit and data subject','database','purple'),('Factory layout','Physical placement in the scene','map','teal')],
 'A hall is a physical location. Production lines, operations and metric scopes are defined separately.'),
 ('Data senders','Observations may come from different devices and systems.',[
 ('Pouyeshgar EdgeBox','Digital inputs and equipment counts','box','blue'),('Company equipment','Controllers, PLCs or another EdgeBox','box','teal'),('SCADA & applications','Industrial systems and APIs','server','purple'),('Files & sensors','Data files or smart sensor gateways','file','amber')],
 'Target model: multiple connections and channels per device. Today, each source represents one independent connection.'),
 ('Connection methods','Register a source and the transport appropriate to its sender.',[
 ('HTTP / POST','Tested EdgeBox receiver path','network','teal'),('MQTT','Requires its runtime adapter','network','purple'),('OPC UA / API','Requires a matching adapter','network','blue'),('File import','Depends on format and input adapter','file','amber')],
 'This pilot receives EdgeBox counts and status over HTTP. A listed protocol does not imply a working receiver.'),
 ('Data Hub','Reception, durable custody and diagnostics, independent of production forms.',[
 ('Authorized reception','Identify company, source and key','shield','blue'),('Durable raw inbox','Persist packet before processing; then ACK','database','purple'),('Validate & extract','Validity, duplicates, conflicts and event time','filter','red'),('Valid tag values','Input channel → technical tag, unit and time','tag','teal')],
 'Invalid rows retain a reason. Zero is valid. Missing data is neither zero nor proof of equipment power-off.'),
 ('Storage & consumption','Hub and application have distinct responsibilities; storage is shared today.',[
 ('Company database','Raw packets + diagnostics | valid tag samples','database','blue'),('Application parameters','Manual entry or tag + conversion / formula','gear','purple'),('Multiple consumers','One tag can serve several consumers','branch','teal'),('Separate raw store · future','Needs storage adapter and migration','database','amber')],
 'Tag-to-parameter connections belong in Data definitions, outside the Hub. Defining a tag alone does not connect a consumer.'),
 ('Application uses','Parallel consumers; general parameter integration is completed module by module.',[
 ('Production & reports','Relevant equipment and operation inputs','file','blue'),('Monitoring & OEE','Planned time, runtime, counts and quality','chart','teal'),('Alarms & state','Rules, data quality and connection freshness','bell','amber'),('Analytics & dashboards','Explicit period, scope and provenance','chart','purple')],
 'Product roadmap: a module appearing here does not imply ready parameter integration or live telemetry.')],
 'return':'Output path · future development','returnBody':'Authorized application → MQTT command → device output → execution acknowledgement and reported state. Broker receipt is not execution.',
 'foot':'Presentation guide · Schematic, no live data · Current structure and approved direction | 2026-10-24',
 }}

PATHS = {
 'building':'M5 21V3h14v18M9 7h2m2 0h2M9 11h2m2 0h2M9 15h2m2 0h2M10 21v-3h4v3',
 'gear':'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8M9 3h6l1 3 3 1 2 5-2 5-3 1-1 3H9l-1-3-3-1-2-5 2-5 3-1Z',
 'database':'M4 6c0-5 16-5 16 0s-16 5-16 0v12c0 5 16 5 16 0V6M4 12c0 5 16 5 16 0',
 'map':'m3 5 6-2 6 2 6-2v16l-6 2-6-2-6 2ZM9 3v16M15 5v16',
 'box':'m3 7 9-4 9 4v10l-9 4-9-4Zm0 0 9 4 9-4M12 11v10',
 'server':'M4 3h16v7H4ZM4 14h16v7H4ZM7 6h1m-1 11h1M12 6h5m-5 11h5',
 'file':'M5 2h9l5 5v15H5ZM14 2v6h5M8 12h8m-8 4h8',
 'network':'M5 9a10 10 0 0 1 14 0M8 12a6 6 0 0 1 8 0m-5 4h2M12 19v1',
 'shield':'m12 2 9 4v6c0 5-9 10-9 10S3 17 3 12V6ZM8 12l3 3 5-6',
 'filter':'M3 3h18l-7 9v8l-4 2V12Z',
 'tag':'M3 3h9l9 9-9 9-9-9ZM7 7h1',
 'branch':'M5 3v18m0-9h9a5 5 0 0 0 5-5V3m-5 9a5 5 0 0 1 5 5v4',
 'chart':'M3 3v18h18M7 17v-5m5 5V6m5 11V9',
 'bell':'M6 16V9a6 6 0 0 1 12 0v7l3 3H3Zm4 6h4',
}

STYLE = '''
@font-face{font-family:Vazir;src:url('/fonts/Vazirmatn.woff2')}*{box-sizing:border-box}body{margin:0;background:#031421;color:#e6f4ff;font-family:Vazir,Arial,sans-serif}main{width:1840px;padding:24px 28px;background:radial-gradient(ellipse at 65% 0,#0c334b99,transparent 65%),#031421}header{display:flex;justify-content:space-between;align-items:center;margin-bottom:17px}h1{margin:0;font-size:29px}header p{margin:4px 0;color:#9dbdd3;font-size:14px}.brand{color:#5cd5ee;letter-spacing:3px;font-size:14px}section{display:grid;grid-template-columns:262px 1fr;gap:22px;padding:17px 20px;margin-bottom:11px;border:1px solid #24506a;border-radius:15px;background:linear-gradient(110deg,#092236b3,#061d2e)}.heading h2{font-size:21px;margin:2px 0 9px}.heading p{color:#a3c3d9;font-size:13px;line-height:1.85;margin:0}.num{display:inline-grid;place-items:center;width:31px;height:31px;border:1px solid #26bbef;background:#0576b536;border-radius:50%;color:#6cddff;margin-inline-end:8px}.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px}.card{--c:#4ab4ff;position:relative;border:1px solid var(--c);background:linear-gradient(135deg,color-mix(in srgb,var(--c) 13%,#082035),#071a2b);border-radius:11px;padding:15px 13px;display:flex;align-items:center;gap:13px;min-height:96px;box-shadow:inset 0 0 20px color-mix(in srgb,var(--c) 7%,transparent)}.card strong{font-size:16px;display:block;margin-bottom:5px}.card small{font-size:12px;color:#a8c9df;display:block;line-height:1.7}.icon{width:43px;height:43px;display:grid;place-items:center;flex-shrink:0;border:1px solid color-mix(in srgb,var(--c) 65%,transparent);border-radius:13px;background:color-mix(in srgb,var(--c) 17%,transparent);box-shadow:0 0 18px color-mix(in srgb,var(--c) 15%,transparent);color:var(--c)}svg{width:26px;height:26px}.purple{--c:#a182ff}.teal{--c:#20d4bd}.amber{--c:#eabb4f}.red{--c:#f37d91}.note{margin:10px 0 0;color:#a4c3d7;font-size:12px;line-height:1.8}.pipeline .card:not(:last-child):after{content:'←';position:absolute;inset-inline-end:-20px;top:34px;color:#51c5fa;font-size:23px}.en .pipeline .card:not(:last-child):after{content:'→'}.future{border-style:dashed;opacity:.9}.uses .card{border-style:dashed}.return{display:flex;gap:18px;align-items:center;border:1px dashed #6b739c;background:#111f35;border-radius:11px;padding:12px 18px;margin-top:5px}.return b{color:#b9a3ff;font-size:14px;white-space:nowrap}.return span{font-size:12px;color:#adc4dc}footer{display:flex;justify-content:space-between;color:#6f99b4;font-size:11px;margin-top:13px}.legend{color:#94bfce;font-size:12px} .flow-arrow{text-align:center;color:#39bdec;height:9px;line-height:9px;margin-top:-7px;margin-bottom:8px}.en .card strong{font-size:15px}.en .heading h2{font-size:20px}
'''

for lang, c in COPY.items():
    sections=[]
    for i,(title,desc,cards,note) in enumerate(c['rows']):
        tiles=[]
        for j,(name,detail,icon,color) in enumerate(cards):
            future = ' future' if (i==2 and j>0) or (i==4 and j==3) else ''
            tiles.append(f'<div class="card {color}{future}"><span class="icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="{PATHS[icon]}"/></svg></span><div><strong>{escape(name)}</strong><small>{escape(detail)}</small></div></div>')
        cls='pipeline' if i==3 else 'uses' if i==5 else ''
        sections.append(f'<section class="{cls}"><div class="heading"><h2><span class="num">{i+1}</span>{title}</h2><p>{desc}</p></div><div><div class="cards">{"".join(tiles)}</div><p class="note">{note}</p></div></section>')
        if i in (1,2,3): sections.append('<div class="flow-arrow">↓</div>')
    text=f'<!doctype html><html lang="{lang}" dir="{"rtl" if lang=="fa" else "ltr"}"><meta charset="utf-8"><title>{c["title"]}</title><style>{STYLE}</style><body class="{lang}"><main><header><div><h1>{c["title"]}</h1><p>{c["sub"]}</p></div><div class="brand">POUYESHGAR<br>SMART FACTORY</div></header>{"".join(sections)}<div class="return"><b>{c["return"]}</b><span>{c["returnBody"]}</span></div><footer><span>{c["foot"]}</span></footer><p class="legend">{c["legend"]}</p></main></body></html>'
    (OUT / f'product-flow-{lang}.html').write_text(text,encoding='utf8')
