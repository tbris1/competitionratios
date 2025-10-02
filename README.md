# UK Specialty Training Competition Ratios Dashboard  

**[EDITED 02/10/2026 TO INCLUDE INFO ON 2025 COMPETITION RATIO DATA]**

---

## Overview  
The UK Specialty Training Competition Ratios Dashboard was designed by Dr Tom Brisk as part of a Clinical Data Science course.  

This dashboard aims to:  
- Demonstrate trends in competition for UK specialty training posts (ST1/CT1 level).  
- Make visualisation easier than reading through separate NHS tables.  

It has **not** been designed to:  
- Make political statements.  
- Guide individual career choices.  

---

## Contact  
For any queries, please contact: **tombrisk@gmail.com**  

---

## Ethics  
Data collected via the feedback form may be used in future publications.

This project and data collection were reviewed by a member of the local NHS trust’s research team, who confirmed that ethics approval was not required.  

---

## Technical Notes  

### 1. Average Calculations  
- **Average (outliers removed):**  
  - Values with fewer than 100 applicants excluded.  
  - Outliers removed using *1.5 × interquartile range* rule.  
  - Mean calculated across remaining specialties for each year.  

- **Average (all specialties):**  
  - Simple mean of all specialty competition ratios per year.  
  - Not weighted by applicant numbers (so niche, competitive specialties may skew results).  
  - Differs from some published averages, which calculate:  

    ```
    Mean = Total Applicants / Total Posts
    ```  

  - This project opts for a mean of individual competition ratios, as it better reflects demand for high-interest specialties rather than assuming applicants would accept any specialty post.  

---

### 2. Predictions  
- Future predictions are generated with a 2nd-degree polynomial regression model using the previous five years of data.  
- **Important disclaimer:**  
  - Predictions are for illustration only.  
  - They should **not** be used to guide decisions.  
  - Actual ratios will almost certainly differ due to political and workforce factors.  
- The dashboard will be updated with 2026 data when released (likely ~Sep 2026).  

---

### 3. Oxbridge Comparison  
“Oxbridge” competition ratios refer to the average entry ratio for undergraduate courses at the Universities of Oxford and Cambridge (~6:1). This is included as a point of comparison. It's a bit silly, really. But I found it somewhat interesting.  
