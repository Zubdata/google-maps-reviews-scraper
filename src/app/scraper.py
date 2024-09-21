from playwright.sync_api import sync_playwright
from app.communiator import Communicator
from app.config import Config
from app.data_saver import DataSaver
from app.data_parser import DataParser
from bs4 import BeautifulSoup
from playwright._impl._errors import TimeoutError
from app.loader import Loader


class Scraper:
    """Main backend class for scraping the reviews"""

    def __init__(self):
        self.browser = None
        self.page = None

    def extract_reviews(self):
        """Extract the raw HTML of all reviews from the page and
        return a list of review elements."""

        reviews = self.page.locator(".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde")

        soup = BeautifulSoup(reviews.inner_html(), "html.parser")
        reviews = soup.select(".jftiEf")

        return reviews

    def open_url(self, url):
        Communicator.log_message("Going to open url.")

        self.page.goto(url, wait_until="load")
        try:
            self.page.wait_for_selector(
                ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde", timeout=30000
            )

        except TimeoutError:
            print("Error: Page is not loaded!")
            exit()
        else:
            Communicator.log_message("Page is loaded.")

    def load_reviews(self):

        scroller = Loader(self.page)
        scroller.load_all()

    def launch_browser(self):
        Communicator.log_message("Launching browser..")

        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)

        context = self.browser.new_context()

        def handle_route(route):
            if route.request.resource_type in ["image", "font"]:
                route.abort()  # Block the request
            else:
                route.continue_()  # Allow the request

        # Start intercepting requests
        context.route("**/*", handle_route)

        self.page = context.new_page()
        Communicator.log_message("Browser is launched.")

    def close_browser(self):
        Communicator.log_message("Closing browser")

        if self.browser:
            self.browser.close()

        Communicator.log_message("Browser is closed")

    def main(self):

        self.launch_browser()
        try:

            url = Config.get_url()

            self.open_url(url)
            self.load_reviews()
            reviews = self.extract_reviews()
            data_parser = DataParser()
            final_data = data_parser.parse_data(reviews)

            data_saver = DataSaver()
            data_saver.save(final_data)
        except Exception as e:
            Communicator.log_message(f"Error occured while scraping. Error: {e}")

        finally:
            self.close_browser()
