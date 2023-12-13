# Running the System

Requirements: `pandas==2.0.3`

The `run_system.py` file can be run immediately after cloning the repository assuming a compatible environment.
The provided `sample_data.csv` will fail due to date errors (detailed in the next section), thus the corrected version must be used.
Sample output is given by the `results.json` file.

***

### Alterations to Source Data

- Impossible date of November 31st for `memberId` "5"
    - Corrected to Nov 30
- visitNumber not chronological for `memberId` "3" (`visitNumber` "3" is the first)
    - Corrected `visitNumber` "3" to 12-31-2023 from 01-01-2023
        - Chose this new date as opposed to 01-01-2024 because it is assumed that this serves as a test for Stroke Exclusion

***

### Omitted Components 

For the sake of time, several core components were omitted:
- Exception handling (throughout all files)
- Schema validations (sample data shape)
- Tests
- Docstrings

***

### Potential Efficiency Improvements

- When checking through visits, iterates through all visitation data.
    - Visits may be better expressed through a date-indexed data structure