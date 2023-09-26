import calendar
import re
from datetime import datetime, timedelta

MONTHS = calendar.month_name[1:]

section_identifiers = {
    "policy_dates": [
        "period", "offering"
    ],
    "contributions": [
        "contribution", "compensation", "percent"
    ]
}


class Policy:
    def __init__(self, policy):
        self.policy = policy
        self.result = {
            "periods": None,
            "stipulation": None,
            "minimum_contribution": None,
            "maximum_contribution": None
        }

    def review_policy(self):
        sections = self.policy.split('\n')
        for section in sections:
            self._review_section(section)
        return self.result

    def _review_section(self, section):
        lower_section = section.lower()

        for identifier in section_identifiers:
            found = False
            keys = section_identifiers[identifier]
            for key in keys:
                if key in lower_section:
                    found = True
            if found:
                self._date_locate(lower_section) if identifier == "policy_dates" \
                    else self._contribution_locate(lower_section)

    def _date_locate(self, section):
        found = False
        if self.result["periods"]:
            return
        occurrence = 0
        for month in MONTHS:
            if month.lower() in section:
                occurrence += 1
        if occurrence > 1:
            found = True
        if found:
            return self._find_date_sentence(section)

    def _find_date_sentence(self, section):
        sentences = section.split('.')
        for sentence in sentences:
            if "commenc" in sentence:
                for month in MONTHS:
                    if month.lower() in sentence:
                        return self._examine_sentence_date(sentence)

    def _examine_sentence_date(self, sentence):
        # It is possible to calculate Trading days using Pandas. I would add this to the model rules
        # if we set it up to retrieve specific periods.
        if "trading day" in sentence:
            self.result["stipulation"] = "Beginning dates start on first subsequent Trading Day. " \
                                         "Ending dates are the last Trading date on or before indicated date."
        date_range = []
        sentences = [sentence]
        if "end" in sentence:
            sentences = sentence.split(" end")
        for sentence in sentences:
            date_range.append(self._get_dates(sentence))
        if len(date_range) == 1:
            date_range.append(self._populate_end_from_start(date_range[0]))
        readable = ""
        date_range = self._check_rotate(date_range)
        for x in range(len(date_range[0])):
            readable += f"{date_range[0][x].capitalize()} - {date_range[1][x].capitalize()}"
            if x != len(date_range[0]) - 1:
                readable += ", "
        self.result["periods"] = readable

    @staticmethod
    def _check_rotate(date_range):
        if len(date_range) > 1:
            start = datetime.strptime(f"{date_range[0][0]} 2022", '%B %d %Y')
            end = datetime.strptime(f"{date_range[1][0]} 2022", '%B %d %Y')
            if start > end:
                date_range[1] = date_range[1] + [date_range[1].pop(0)]
        return date_range

    @staticmethod
    def _populate_end_from_start(dates):
        # Leap year could affect tentative end dates in February.
        end_dates = []
        for date in dates:
            end = datetime.strptime(f"{date} 2022", '%B %d %Y') - timedelta(days=1)
            end_dates.append(end.strftime("%B %d").lower())
        return end_dates + [end_dates.pop(0)]

    @staticmethod
    def _get_dates(sentence):
        dates = []
        for month in MONTHS:
            check = sentence.find(month.lower())
            if check > 1:
                dates.append(sentence[check: check + len(month) + 3].strip().replace(',', ''))
        return dates

    def _contribution_locate(self, section):
        sentences = section.split('.')
        for sentence in sentences:
            self._locate_symbol(sentence)

    def _locate_symbol(self, sentence):
        symbols = ['%', '$']
        for symbol in symbols:
            if symbol in sentence:
                return self._locate_compensation(sentence)

    def _locate_compensation(self, sentence):
        limits = [("minimum_contribution", "not less than"), ("maximum_contribution", "not more than"),
                  ("maximum_contribution", "not exceed")]
        potential_value = self._find_value(sentence)
        for limit in limits:
            loc = sentence.find(limit[1])
            if loc > -1:
                sentences = [sentence[loc:]]
                if " or " in sentence:
                    sentences = sentence[loc:].split(" or ")
                for sentence in sentences:
                    value = self._find_value(sentence)
                    if value and not self.result[limit[0]]:
                        self.result[limit[0]] = value
                    elif value:
                        self.result[limit[0]] += f" or {value}"
        if not self.result[limits[0][0]] and self.result["maximum_contribution"] \
                and potential_value not in self.result["maximum_contribution"]:
            self._check_for_minimum(potential_value)

    def _check_for_minimum(self, potential_value):
        potential = int(''.join([i for i in potential_value if i.isdigit()]))
        maximum = int(''.join([i for i in self.result['maximum_contribution'] if i.isdigit()]))
        if potential < maximum:
            self.result["minimum_contribution"] = potential_value

    @staticmethod
    def _find_value(fragment):
        value = re.search("(\d+(\.\d+)?%)", fragment)
        if not value:
            p = re.compile(r'\$?(?:(?:[1-9][0-9]{0,2})(?:,[0-9]{3})+|[1-9][0-9]*|0)(?:[\.,][0-9][0-9]?)?(?![0-9]+)')
            value = re.search(p, fragment)
        return value.group() if value else None
