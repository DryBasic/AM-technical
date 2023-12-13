from SARQualityMeasure import SARQualityMeasure
from AbstractQualityMeasure import Member, Visit
import json
import pandas as pd
import datetime

def process_date(date_string, sep='/') -> datetime.date:
    """Convert mm-dd-yyyy strings to datetime.date object"""
    split_str = date_string.split(sep)
    int_split = [int(i) for i in split_str]
    return datetime.date(
        int_split[2],
        int_split[0],
        int_split[1]
        )

def create_member_from_grouping(group: pd.DataFrame) -> Member:
    visits = []
    for i, record in group.iterrows():
        visit = record.to_dict()
        visits.append(
            Visit(
                visitNumber=visit['visitNumber'],
                visitDate=process_date(visit['visitDate']),
                visitCode=visit['visitCode']
            )
        )
        member = group.iloc[0].to_dict()
        return Member(
                memberId=member['memberId'],
                age=member['age'],
                productLine=member['productLine'],
                enrolledStart=process_date(member['enrolledStart']),
                enrolledEnd=process_date(member['enrolledEnd']),
                visits=visits
            )


# read data, create Member objects
data = pd.read_csv('corrected_sample_data.csv')
members = []
for i, group in data.groupby('memberId').__iter__():
    members.append(create_member_from_grouping(group))

sarqm = SARQualityMeasure()

# iterate through members, generate results
results = []
for member in members:
    results.append(sarqm.get_result(member))

# write results to file
with open('results.json', 'w') as f:
    json.dump(results, f)