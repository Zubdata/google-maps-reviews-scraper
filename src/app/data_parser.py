from app.communiator import Communicator


class DataParser:
    """This class is responsible for parsing html data and converting into structured data"""

    def __init__(self) -> None:

        pass

    def get_total_stars(self, review):
        total_stars_tag = review.select_one("span.kvMYJc")
        if not total_stars_tag:
            total_stars_tag = review.select_one("span.fzvQIb")
            total_stars = total_stars_tag.text if total_stars_tag else None
            return total_stars

        return total_stars_tag.get("aria-label") if total_stars_tag else None

    def get_published_date(self, review):
        date_tag = review.select_one("span.rsqaWe")
        if not date_tag:
            date_tag = review.select_one("span.xRkPPb")
            published_date = (
                date_tag.text.replace(" on Google", "") if date_tag else None
            )
            return published_date

        return date_tag.text if date_tag else None

    def parse_review(self, review):
        """Parse HTML of a single review"""

        review_text_tag = review.select_one("div.MyEned")
        # review_text_tag = review.find("div", class_="MyEned")
        review_text = review_text_tag.text if review_text_tag else None

        total_stars = self.get_total_stars(review=review)

        # reviewer_name_tag = review.find("div", class_="d4r55 ")
        reviewer_name_tag = review.select_one("div.d4r55")
        reviewer_name = reviewer_name_tag.text if reviewer_name_tag else None

        published_date = self.get_published_date(review=review)

        return {
            "review_text": review_text,
            "total_stars": total_stars,
            "reviewer_name": reviewer_name,
            "published_date": published_date,
        }

    def parse_data(self, data: list):

        Communicator.log_message("Going to parse data")

        final_data = []

        for review in data:
            structured_data = self.parse_review(review)
            final_data.append(structured_data)

        Communicator.log_message("Data is parsed")

        return final_data
