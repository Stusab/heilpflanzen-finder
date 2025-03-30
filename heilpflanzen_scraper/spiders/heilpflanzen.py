import scrapy

class HeilpflanzenSpider(scrapy.Spider):
    name = "heilpflanzen"
    allowed_domains = ["meine-gesundheit.de"]
    start_urls = ["https://www.meine-gesundheit.de/medizin/heilpflanzen/heilpflanzen-liste"]

    def parse(self, response):
        pflanzen_links = response.css("a::attr(href)").getall()

        for link in pflanzen_links:
            if "/medizin/heilpflanzen" in link and not link.endswith("/medizin/heilpflanzen"):
                full_link = response.urljoin(link)
                yield response.follow(full_link, callback=self.parse_detail)

    def parse_detail(self, response):
        name = response.css("h1::text").get()
        name = name.strip() if name else "Unbekannt"

        # 🔍 Neue XPath-Strategie: fange Anwendungsgebiete & mögliche Folgezeilen ab
        raw_symptome = response.xpath(
            '//li[contains(text(), "Anwendungsgebiete")]/text() | '
            '//li[contains(text(), "Anwendungsgebiete")]/following-sibling::li[position() < 3]/text()'
        ).getall()

        symptome = [s.strip() for s in raw_symptome if s.strip()]

        # Sonderfall: nur "Anwendungsgebiete:" ohne weiteren Text
        if symptome and len(symptome) == 1 and symptome[0].lower().strip().endswith("anwendungsgebiete:"):
            symptome = ["Keine Angabe"]

        if not symptome:
            symptome = ["Keine Angabe"]

        yield {
            "name": name,
            "symptome": " ".join(symptome),
            "url": response.url
        }
