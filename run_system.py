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

# written to take a single member entity so func can be distributed
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
# __iter__ method returns generator containing grouped dataframes
for i, group in data.groupby('memberId').__iter__():
    members.append(create_member_from_grouping(group))

sarqm = SARQualityMeasure()

# iterate through members, store results in memory
results = []
for member in members:
    results.append(sarqm.get_result(member))

# write results to file
# may wish to include a memberId in the results
# or bundle results with "header" file containing these IDs
with open('results.json', 'w') as f:
    json.dump(results, f)