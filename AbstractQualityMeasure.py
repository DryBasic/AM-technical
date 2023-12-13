import datetime

class Visit:
    def __init__(self, visitNumber: int, visitDate: datetime.date, visitCode: str):
        self.visitNumber = visitNumber
        self.visitDate = visitDate
        self.visitCode = visitCode
        
        # may prefer to read these codes from somewhere else for cleanliness
        self.ICD10CM = {
            'Z44.001': 'Rehabilitation',
            'Z44.002': 'Rehabilitation',
            'Z44.009': 'Rehabilitation',
            'Z44.011': 'Rehabilitation',
            'Z44.012': 'Rehabilitation',
            'Z44.019': 'Rehabilitation',
            'Z44.021': 'Rehabilitation',
            'Z44.022': 'Rehabilitation',
            'Z44.029': 'Rehabilitation',
            'Z44.101': 'Rehabilitation',
            'G45.0': 'Stroke',
            'G45.1': 'Stroke',
            'G45.2': 'Stroke',
            'G45.8': 'Stroke',
            'G45.9': 'Stroke',
            'G46.0': 'Stroke',
            'G46.1': 'Stroke',
            'G46.2': 'Stroke',
            'G97.31': 'Stroke',
            'G97.32': 'Stroke',
            'Z51.89': 'Stroke Exclusion'
        }

    def get_classification(self):
        return self.ICD10CM.get(self.visitCode)


class Member:
    def __init__(self, memberId: int, age: int, productLine: str, enrolledStart: datetime.date, enrolledEnd: datetime.date, visits: list):
        self.memberId = memberId
        self.age = age
        self.productLine = productLine
        self.enrolledStart = enrolledStart
        self.enrolledEnd = enrolledEnd
        self.visits = visits


class AbstractQualityMeasure:
    def __init__(self, *, product_line='Medicare', age_range=[18, 30],
        max_enrollment_date=datetime.date(datetime.date.today().year, 12, 31)) -> None:
        """Takes Member object and keyword arguments to set generic defaults for result attributes.
        
        kwargs
        * product_line: product line required for qualification; defaults to 'Medicare'
        * age_range: inclusive age range (2-item list of integers) for qualification; defaults to [18, 30]
        * max_enrollment_date: member must have coverage through this date; defaults to end current year"""
        # Arbitrarily assigned default values
        self.product_line = product_line
        self.age_range = age_range
        self.max_enrollment_date = max_enrollment_date
        # For exclusions, events, and the numerator
        # I could not think of default attributes to be used, so they
        # will default to True per their functional "_check" definitions
            # will always need to be overwritten for specific quality measures

        # set result conditions to NoneType
        self._reset()

    def _reset(self) -> None:
        self._matches_product_line = None
        self._matches_age_requirements = None
        self._is_enrolled_through = None
        self._is_excluded = None
        self._has_event = None
        self._is_denominator = None
        self._is_numerator = None
        self.member = None


    def get_result(self, member: Member) -> dict:
        self.member = member
        
        self._check_product_line()
        self._check_age_requirements()
        self._check_enrollment()
        self._check_exclusion()
        self._check_qualifying_event()
        self._check_denominator()
        self._check_numerator()

        results = {
            'matches_product_line': self._matches_product_line,
            'matches_age_requirements': self._matches_age_requirements,
            'is_enrolled_through': self._is_enrolled_through,
            'is_excluded': self._is_excluded,
            'has_event': self._has_event,
            'is_denominator': self._is_denominator,
            'is_numerator': self._is_numerator
        }
        self._reset()
        
        return results 

    def _check_product_line(self) -> None:
        check = self.member.productLine == self.product_line
        self._matches_product_line = check

    def _check_age_requirements(self) -> None:
        lower, upper = self.age_range
        check = lower <= self.member.age <= upper
        self._matches_age_requirements = check

    def _check_enrollment(self) -> None:
        check = self.member.enrolledEnd >= self.max_enrollment_date
        self._is_enrolled_through = check
        
    def _check_exclusion(self) -> None:
        check = True
        self._is_excluded = check

    def _check_qualifying_event(self) -> None:
        check = True
        self._has_event = check

    def _check_denominator(self) -> None:
        self._is_denominator = all([
            self._matches_product_line,
            self._matches_age_requirements,
            self._is_enrolled_through,
            self._is_excluded,
            self._has_event
        ])

    def _check_numerator(self) -> None:
        check = True
        self._is_numerator = check
