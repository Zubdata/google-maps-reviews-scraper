from app.communiator import Communicator


class Loader:
    """This class is responsible for loading all the reviews and then expanding each review"""

    def __init__(self, page) -> None:
        self.page = page

    def is_throbber_present(self):
        """
        Check if the loader (throbber) is present.
        If the loader is present, it indicates that more content is loading and we need to scroll further.
        If not, it means we've reached the end of the page.
        """

        js_code = """
        () => document.querySelectorAll(".lXJj5c.Hk4XGb");
"""

        throbber = self.page.evaluate(js_code)

        return throbber

    def click_all_more(self):
        """Click on all more buttons to expand review text"""

        js_code = """
                let allbtn = document.querySelectorAll(".w8nwRe.kyuRq");

        allbtn.forEach(function(btn) {
            btn.click(); // Click each button
        });
        """

        self.page.evaluate(js_code)

    def scroll_div(self, element):

        js_code = """
        (element)=>{
        let element_scroll_height = element.scrollHeight;
        let scroller_current_height = element.scrollTop;

        element.scrollBy(scroller_current_height, element_scroll_height);
        }
"""

        self.page.evaluate(js_code, element)

    def scroll(self):
        """Scroll the reviews to load all reviews of the place"""

        Communicator.log_message("Starting scrolling...")

        while True:
            if not self.is_throbber_present():
                break

            reviews_div = self.page.query_selector(
                ".m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde"
            )

            self.scroll_div(reviews_div)

        Communicator.log_message("Scrolling has ended")

        self.click_all_more()

    def load_all(self):
        Communicator.log_message("Going to load all reviews...")

        self.scroll()
