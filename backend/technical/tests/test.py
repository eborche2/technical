import json

from django.test import TestCase, Client


ONE = """- Initial Contribution Periods. Subject to the following paragraph (b), the Plan shall be implemented by a series of consecutive Contribution Periods commencing on January 1 and July 1 each year and ending on the following June 30 and December 31, respectively. The first Contribution Period under this Plan shall commence on July 1, 2010, and shall end on December 31, 2010. The Plan shall continue until terminated in accordance with Section 13 or Section 19.
- Changes. The Committee shall have the power to change the duration and/or frequency of Contribution Periods with respect to future purchases of Shares, without shareholder approval, if such change is announced to all Employees who are eligible under Section 3 at least five Business Days before the Commencement Date of the first Contribution Period to be affected by the change; provided, however, that no Contribution Period shall exceed 27 months.
- Contribution Amounts. Subject to the limitations of Sections 3(b) and 11, a Participant shall elect to have Contributions made as payroll deductions on each payday during the Contribution Period in any percentage of his or her Compensation that is not less than 1% and not more than 15% (or such other maximum percentage as the Committee may establish from time to time before any Commencement Date) of such Participant’s Compensation on each payday during the Contribution Period. Contribution amounts shall be withheld in whole percentages only."""

TWO = """- “Offering Period” means a period of time specified by the Administrator, consistent with Section 423 of the Code, beginning on the Offer Date and ending on the Acquisition Date. Unless otherwise determined by the Administrator, each Offering Period shall be a period of three (3) calendar months commencing on January 1, April 1, July 1 and October 1 of each calendar year during the Term of the Plan. The first Offering Period under the Plan shall commence as of July 1, 2021.
- Enrollment. An eligible Employee may become a Participant in the Plan by completing an enrollment election form and any other required enrollment documents provided by the Administrator or its designee and submitting them to the Administrator or its designee prior to the commencement of an Offering Period in accordance with the rules established by the Administrator. The enrollment documents, which may, in the discretion of the Administrator, be in electronic form, shall set forth the amount of the Participant’s Compensation in whole dollars, which may not exceed $5,000 per Offering Period (or such other amount as may be prescribed by the Administrator from time to time) or forty percent (40%) of Participant’s Compensation per Offering Period (or such other percentage as may be prescribed by the Administrator from time to time), to be paid as Contributions pursuant to the Plan. An Employee’s payroll enrollment election shall become effective on an Offer Date in accordance with the rules established by the Administrator. Amounts deducted from a Participant’s Compensation pursuant to this Article V shall be credited to the Participant’s Plan account. No interest shall be payable on the amounts credited to the Participant’s Plan account. After an eligible Employee has become a Participant in the Plan for an Offering Period, the Participant’s payroll authorization for that Offering Period shall continue in force and effect for that Offering Period, unless the Participant withdraws from the Plan or the Administrator permits any such change during the Offering Period and the Participant changes such election in accordance with the procedures established by the Administrator."""

THREE = """- Frequency and Duration. The Administrator may establish Offering Periods of such frequency and duration as it may from time to time determine as appropriate.
- First Offering Period. The first Offering Period under the Plan shall commence on the IPO Date and shall end on the last Trading Day on or immediately preceding May 14, 2020.
- Successive Offering Periods. Unless the Administrator determines otherwise, following the completion of the first Offering Period, a new Offering Period shall commence on the first Trading Day on or following May 15 and November 15 of each calendar year and end on or following the last Trading Day on or immediately preceding November 14 and May 14, respectively, approximately six (6) months later.
- At the time a Participant enrolls in the Plan pursuant to Section 5 of the Plan, he or she will elect to have Contributions (in the form of payroll deductions or otherwise, to the extent permitted by the Administrator) made on each pay day during the Offering Period in an amount not exceeding fifteen percent (15%) of the Compensation, which he or she receives on each pay day during the Offering Period (for illustrative purposes, should a pay day occur on an Exercise Date, a Participant will have any payroll deductions made on such day applied to his or her account under the then-current Purchase Period or Offering Period). The Administrator, in its sole discretion, may permit all Participants in a specified Offering to contribute amounts to the Plan through payment by cash, check or other means set forth in the subscription agreement prior to each Exercise Date of each Purchase Period. A Participant’s subscription agreement will remain in effect for successive Offering Periods unless terminated as provided in Section 10 hereof."""

FOUR = """4. Offerings. Subject to the right of the Company in its sole discretion to sooner terminate the Plan or to change the commencement date or term of any offering, commencing with the Offering Date of December 1, 2020, the Plan will operate with separate consecutive six-month offerings with the following Offering Dates: June 1 and December 1; provided, however,
3


that no offering may have a term in excess of 27 months. Unless a termination of or change to the Plan has previously been made by the Company, the final offering under this Plan shall commence on June 1, 2029 and terminate on November 30, 2029. In order to become eligible to purchase shares of Common Stock, an Eligible Employee must complete and submit an Enrollment Form and any other necessary documents at least 15 days (or such other period as may be designated by the Administrator) before the Offering Date of the particular offering in which he or she wishes to participate in accordance with Section 7. Participation in one offering under the Plan shall neither limit, nor require, participation in any other offering.
5. Price. The Purchase Price per share shall be eighty-five percent (85%) of the Fair Market Value of the Common Stock on the last day of the offering.
6. Number of Shares to be Offered. The maximum number of shares that will be offered under the Plan is 20,000,000 shares, subject to adjustment as permitted under Section 20. If the total number of shares of Common Stock for which options are to be granted on any date in accordance with Section 12 exceeds the number of shares of Common Stock then available under the Plan or a given sub-plan (after deduction of all shares for which options have been exercised under the Plan or are then outstanding), the Company shall make a pro rata allocation of the shares remaining available in as nearly a uniform manner as it determines is practicable and equitable. In such event, the payroll deductions to be made pursuant to the authorizations therefor shall be reduced accordingly and the Company shall give written notice of the reduction to each participant affected.
7. Participation.
7.1 An Eligible Employee may become a participant by completing an Enrollment Form provided by the Company and submitting it to the Company, or with such other entity designated by the Company for this purpose, no later than 15 days (or such other period as may be designated by the Administrator) prior to the commencement of the offering to which it relates.
7.2 Payroll deductions for a participant shall commence on the Offering Date as described above and shall continue through subsequent offerings pursuant to Section 10 until the participant’s termination of employment, subject to modification by the participant as provided in Section 8.1, and unless participation is earlier withdrawn or suspended by the employee as provided in Section 9 or deductions are reduced (including to zero) by the Company pursuant to Section 6.
7.3 Payroll deduction shall be the sole means of accumulating funds in a participant’s Account, except in foreign countries where payroll deductions are not allowed, in which case the Company may authorize alternative payment methods.
7.4 The Company may require current participants to complete a new Enrollment Form at any time it deems necessary or desirable to facilitate Plan administration or for any other reason.
8. Payroll Deductions.
8.1 At the time an Eligible Employee files a payroll deduction authorization, he or she shall elect to have deductions made from his or her Compensation on each payday during the time he or she is a participant in an offering at (i) any non-fractional percentage rate from one
4


percent (1%) to twenty percent (20%) or (ii) any flat dollar amount (not exceeding 20%), but in each case shall not exceed $10,625 in any offering. A participant may change his or her payroll deduction percentage election, including changing the payroll deduction percentage or flat dollar amount to zero, effective as of any Offering Date by filing a revised authorization, provided the revised authorization is filed at least 15 days (or such other period as may be designated by the Administrator) prior to such Offering Date."""
test_dictionary = [
    {
        "payload": ONE,
        "result":
            {
                "periods": "January 1 - June 30, July 1 - December 31",
                "stipulation": None,
                "minimum_contribution": "1%",
                "maximum_contribution": "15%"}
    },
    {
        "payload": TWO,
        "result":
            {
                "periods": "January 1 - March 31, April 1 - June 30, July 1 - September 30, October 1 - December 31",
                "stipulation": None,
                "minimum_contribution": None,
                "maximum_contribution": "$5,000 or 40%"
            },
    },
    {
        "payload": THREE,
        "result":
            {
                "periods": "May 15 - November 14, November 15 - May 14",
                "stipulation": "Beginning dates start on first subsequent Trading Day. Ending dates are the last Trading date on or before indicated date.",
                "minimum_contribution": None,
                "maximum_contribution": "15%"
            }
    },
    {
        "payload": FOUR,
        "result":
            {
                'periods': 'June 1 - November 30, December 1 - May 31',
                'stipulation': None,
                'minimum_contribution': '1%',
                'maximum_contribution': '20%'
            }
    }
]


class PolicyTestCase(TestCase):
    """
    Test the policy endpoint
    """

    def setUp(self):
        self.client = Client()

    def test_results(self):
        for i, test in enumerate(test_dictionary):
            result = self.client.post("/unstructured", json.dumps({"policy": test["payload"]}), content_type="application/json")
            json_result = result.json()
            for cat in json_result:
                self.assertEqual(json_result[cat], test["result"][cat])

