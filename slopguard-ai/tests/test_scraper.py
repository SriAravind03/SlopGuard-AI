import pytest

from scraper.url_scraper import ScrapeError, _extract, validate_public_url


@pytest.mark.parametrize("url", ["", "file:///etc/passwd", "http://localhost/", "http://127.0.0.1", "http://10.0.0.1", "ftp://example.com"])
def test_rejects_invalid_and_private_urls(url):
    with pytest.raises(ScrapeError): validate_public_url(url)


def test_requires_http_scheme():
    with pytest.raises(ScrapeError): validate_public_url("javascript:alert(1)")


def test_html_extraction_strips_navigation_and_scripts():
    html = "<html><head><title>Test story</title></head><body><nav>Ignore this navigation</nav><script>ignore()</script><article><p>" + "Useful article content with concrete details and enough words to pass the extraction limit. " * 3 + "</p></article></body></html>"
    title, text = _extract(html, "https://example.com/story")
    assert title == "Test story"
    assert "Useful article content" in text
    assert "Ignore this navigation" not in text
