import ipaddress
import socket
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

MAX_BYTES = 2_000_000
TIMEOUT = (4, 8)
HEADERS = {"User-Agent": "SlopGuardAI/1.0 (content quality analyzer)"}


class ScrapeError(ValueError):
    pass


def validate_public_url(url: str) -> str:
    try:
        parsed = urlparse((url or "").strip())
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.username or parsed.password:
            raise ScrapeError("Enter a valid public http or https URL.")
        host = parsed.hostname.rstrip(".").encode("idna").decode("ascii")
        if host.casefold() == "localhost" or host.casefold().endswith(".localhost"):
            raise ScrapeError("Local and private network URLs are not allowed.")
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)}
        if not addresses:
            raise ScrapeError("The hostname did not resolve to a public address.")
        for address in addresses:
            ip = ipaddress.ip_address(address.split("%", 1)[0])
            if not ip.is_global:
                raise ScrapeError("Local and private network URLs are not allowed.")
        return parsed._replace(netloc=host + (f":{parsed.port}" if parsed.port else "")).geturl()
    except ScrapeError:
        raise
    except Exception as exc:
        raise ScrapeError("The URL is invalid or its host could not be safely resolved.") from exc


def _extract(html: str, url: str) -> tuple[str, str]:
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for node in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg"]):
            node.decompose()
        title = soup.title.get_text(" ", strip=True) if soup.title else url
        body = soup.find("article") or soup.find("main") or soup.body or soup
        blocks = [el.get_text(" ", strip=True) for el in body.find_all(["p", "h1", "h2", "h3", "li"])]
    except ImportError:
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.suppressed = 0
                self.capture = False
                self.title_parts = []
                self.parts = []
                self.current = []

            def handle_starttag(self, tag, attrs):
                if tag in {"script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg"}:
                    self.suppressed += 1
                if tag == "title": self.capture = True
                if tag in {"p", "h1", "h2", "h3", "li"} and not self.suppressed: self.current = []

            def handle_endtag(self, tag):
                if tag == "title": self.capture = False
                if tag in {"script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg"} and self.suppressed:
                    self.suppressed -= 1
                if tag in {"p", "h1", "h2", "h3", "li"} and not self.suppressed:
                    value = " ".join(self.current).strip()
                    if len(value) > 35: self.parts.append(value)

            def handle_data(self, data):
                if self.capture: self.title_parts.append(data)
                if not self.suppressed: self.current.append(data)

        parser = TextExtractor()
        parser.feed(html)
        title = " ".join(parser.title_parts).strip() or url
        blocks = parser.parts
    try:
        import trafilatura
        extracted = trafilatura.extract(html, url=url, include_comments=False, include_tables=True)
    except ImportError:
        extracted = None
    if not extracted:
        extracted = "\n".join(x for x in blocks if len(x) > 35)
    return title[:300], extracted[:50000].strip()


def fetch_article(url: str) -> dict:
    current = validate_public_url(url)
    session = requests.Session()
    try:
        for _ in range(4):
            # Revalidate each hop to prevent redirects into private networks.
            current = validate_public_url(current)
            response = session.get(current, headers=HEADERS, timeout=TIMEOUT, stream=True, allow_redirects=False)
            if response.is_redirect or response.is_permanent_redirect:
                location = response.headers.get("Location")
                response.close()
                if not location:
                    raise ScrapeError("The page returned an invalid redirect.")
                current = urljoin(current, location)
                continue
            if response.status_code >= 400:
                raise ScrapeError(f"The page returned HTTP {response.status_code}.")
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type and "html" not in content_type and "text/plain" not in content_type:
                raise ScrapeError("The URL does not appear to serve an HTML page.")
            data = bytearray()
            for chunk in response.iter_content(65536):
                data.extend(chunk)
                if len(data) > MAX_BYTES:
                    raise ScrapeError("The webpage is larger than the 2 MB limit.")
            html = bytes(data).decode(response.encoding or "utf-8", errors="replace")
            title, text = _extract(html, current)
            if len(text) < 80:
                raise ScrapeError("Could not extract enough article text from this page.")
            return {"url": current, "title": title, "text": text}
        raise ScrapeError("The page redirected too many times.")
    except requests.RequestException as exc:
        raise ScrapeError("Could not retrieve the webpage within the timeout.") from exc
    finally:
        session.close()
