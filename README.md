# Running the System

***

### Alterations to Source Data

- Impossible date of November 31st for memberId 5
    - Corrected to Nov 30
- visitNumber not chronological for member 3 (visitNumber 3 is the first)
    - Corrected visitNumber 3 to 2024

***

### Omitted Components 

For the sake of time, several core components were omitted:
- Exception handling
- Schema validations
- Tests
- Docstrings

***

### Potential Efficiency Improvements

- When checking through visits, iterates through all visitation data.
    - Visits may be better expressed through a date-indexed data structure