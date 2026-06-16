# L7-Resilience-Scanner 🛡️

<div align="center">

**[English](#english) | [فارسی](#farsi)**

</div>

---

<a id="english"></a>
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
```


# ابزار تست تاب‌آوری لایه ۷ - L7-Resilience-Scanner 🛡️

**L7-Resilience-Scanner** یک ابزار حرفه‌ای و قدرتمند تست فشار (Stress Testing) است که با استفاده از کتابخانه **Python AsyncIO** طراحی شده است. این ابزار به طور اختصاصی برای متخصصان امنیت و مدیران شبکه جهت ارزیابی تاب‌آوری (Resilience)، ظرفیت بارگذاری (Load Capacity) و پایداری وب‌سایت‌ها و اپلیکیشن‌های تحت وب در برابر ترافیک سنگین و همزمان لایه ۷ (HTTP/HTTPS) توسعه یافته است.

---

### 🚀 ویژگی‌های کلیدی
* **هسته AsyncIO:** طراحی بهینه‌شده برای دستیابی به حداکثر بازدهی و تعداد درخواست‌ها با کمترین میزان مصرف منابع سیستم.
* **مدیریت هوشمند پروکسی:** جمع‌آوری خودکار لیست پروکسی‌ها از ۱۸ منبع معتبر جهانی و اعتبارسنجی لحظه‌ای (Real-time Validation) برای اطمینان از سلامت اتصالات.
* **دور زدن کش (Cache-Busting):** عبور از مکانیزم‌های کشینگ CDNها و فایروال‌های وب (WAF) با تزریق پارامترهای تصادفی در انتهای URL.
* **پشتیبانی کامل از SSL/TLS:** امکان تست و ممیزی ایمن سرورهای HTTPS از طریق تونل‌زنی.
* **مانیتورینگ زنده:** مشاهده لحظه‌ای آمار شامل تعداد درخواست در ثانیه (RPS)، میزان تأخیر (Latency) و نرخ موفقیت یا خطا.

---

### 🛠 راهنمای نصب و اجرا
برای شروع استفاده، دستورات زیر را به ترتیب در ترمینال یا محیط Command Prompt خود وارد کنید:

```bash
# کلون کردن مخزن پروژه
git clone [https://github.com/mr-coder20/L7-Resilience-Scanner.git](https://github.com/mr-coder20/L7-Resilience-Scanner.git)

# ورود به پوشه پروژه
cd L7-Resilience-Scanner

# نصب کتابخانه‌های پیش‌نیاز
pip install -r requirements.txt

# اجرای موتور تست
python engine.py
cd L7-Resilience-Scanner
pip install -r requirements.txt
python engine.py
