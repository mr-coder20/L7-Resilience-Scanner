# L7-Resilience-Scanner 🛡️

[English](#english) | [فارسی](#فارسی)

---

<a name="english"></a>
## 🇬🇧 English: High-Performance L7 Resilience Testing Engine

**L7-Resilience-Scanner** is a professional-grade stress testing tool built with **Python AsyncIO**. It is specifically designed to audit the resilience, load capacity, and network stability of web applications against high-concurrency L7 traffic.

### 🚀 Key Features
* **AsyncIO Core:** Optimized for maximum throughput with minimal resource consumption.
* **Smart Proxy Rotation:** Automatically harvests from 18+ sources and validates proxies in real-time.
* **WAF/CDN Cache-Busting:** Bypasses caching mechanisms by injecting dynamic query strings.
* **SSL/TLS Tunneling:** Full support for HTTPS target auditing.
* **Real-time Analytics:** Monitors Requests-Per-Second (RPS), latency, and success/error rates.

### 🛠 Installation
```bash
git clone [https://github.com/mr-coder20/L7-Resilience-Scanner.git](https://github.com/mr-coder20/L7-Resilience-Scanner.git)
cd L7-Resilience-Scanner
pip install -r requirements.txt
python engine.py
⚠️ Disclaimer
This tool is for educational and authorized security auditing purposes only. Unauthorized use against systems you do not own or have explicit permission to test is illegal.

🇮🇷 فارسی: موتور تست تاب‌آوری لایه ۷ (L7)
L7-Resilience-Scanner یک ابزار حرفه‌ای تست فشار (Stress Testing) است که با استفاده از Python AsyncIO طراحی شده است. این ابزار برای ارزیابی تاب‌آوری، ظرفیت بارگذاری و پایداری وب‌سایت‌ها در برابر ترافیک سنگین لایه ۷ (HTTP/HTTPS) ساخته شده است.

🚀 ویژگی‌های کلیدی
هسته AsyncIO: بهینه‌سازی شده برای حداکثر بازدهی با کمترین مصرف منابع.

مدیریت هوشمند پروکسی: جمع‌آوری خودکار از ۱۸ منبع معتبر و اعتبارسنجی لحظه‌ای.

دور زدن کش (Cache-Busting): عبور از فایروال‌های وب (WAF) و CDNها با استفاده از پارامترهای تصادفی.

پشتیبانی از SSL/TLS: امکان تست و ممیزی سرورهای HTTPS.

مانیتورینگ زنده: مشاهده وضعیت لحظه‌ای RPS، تأخیر (Latency) و نرخ خطا.

🛠 نحوه نصب
Bash
git clone [https://github.com/mr-coder20/L7-Resilience-Scanner.git](https://github.com/mr-coder20/L7-Resilience-Scanner.git)
cd L7-Resilience-Scanner
pip install -r requirements.txt
python engine.py
⚠️ سلب مسئولیت (Disclaimer)
این ابزار صرفاً برای اهداف آموزشی و تست‌های نفوذ قانونی طراحی شده است. استفاده غیرمجاز از این ابزار علیه سیستم‌هایی که مالک آن نیستید یا اجازه تست آن‌ها را ندارید، غیرقانونی است.

🔍 SEO Keywords
L7 Stress Testing, Web Application Resilience, Python AsyncIO Tool, DDoS Simulation, HTTP Flood Engine, Proxy Rotation, WAF Testing, تست فشار وب, امنیت شبکه, ابزار تست نفوذ پایتون


---

### چند نکته طلایی برای سئوی بیشتر (SEO Tips):

1.  **استفاده از GitHub Actions:** اگر فایل `README.md` را در گیت‌هاب قرار می‌دهید، حتماً از بخش **About** در سمت راست مخزن استفاده کنید و کلمات کلیدی مثل `stress-testing`, `security-tool`, `asyncio` را در تگ‌های آن وارد کنید.
2.  **ایجاد Wiki:** اگر پروژه پیچیده است، یک **Wiki** داخل گیت‌هاب بسازید. موتورهای جستجو به صفحات Wiki بسیار علاقه دارند و این کار سئوی پروژه شما را به شدت افزایش می‌دهد.
3.  **توضیحات در فایل‌های جانبی:** در فایل `LICENSE` یا `CONTRIBUTING.md` نیز به صورت گذرا به نام پروژه اشاره کنید تا در جستجوهای مرتبط، این فایل‌ها نیز ایندکس شوند.
4.  **تصاویر (Diagrams):** برای درک بهتر نحوه تعامل پروکسی‌ها با سرور، افزودن یک دیاگرام معماری به فایل `README` می‌تواند نرخ کلیک (CTR) شما را افزایش دهد:
