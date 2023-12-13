from AbstractQualityMeasure import AbstractQualityMeasure, Member, Visit
import datetime

class SARQualityMeasure(AbstractQualityMeasure):
    def __init__(self):
        super(SARQualityMeasure, self).__init__()
        self.product_line = 'Medicare' # unchanged from superclass
        self.age_range = [18, 27]
        self.max_enrollment_date = datetime.date(2023, 12, 31) # unchanged from superclass

    def _check_qualifying_event(self) -> None:
        check = False
        for visit in self.member.visits:
            if visit.visitDate.year == 2023:
                check = check or visit.get_classification() == 'Rehabilitation'
        self._has_event = check

    def _check_exclusion(self) -> None:
        check = False
        for visit in self.member.visits:
            if visit.visitDate.year == 2023:
                check = check or visit.get_classification() == 'Stroke Exclusion'
        self._is_excluded = check

    def _check_numerator(self) -> None:
        check = False
        # assumes visits are sorted by date ascending
        last_stroke = datetime.date(9999, 12, 31)
        for visit in reversed(self.member.visits):
            vis_class = visit.get_classification()
            if vis_class == 'Stroke' and visit.visitDate.year == 2023:
                last_stroke = visit.visitDate
            elif vis_class == 'Rehabilitation' and (last_stroke - visit.visitDate).days <= 7:
                check = True
        self._is_numerator = check
