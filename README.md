# AI_Conference_Reviews_Research
This is the opensourced repository for code associated with the [Longitudinal Study on AI Research Conference Paper Rejections](https://docs.google.com/document/d/1kj89u9o5N7jQIPjkQh6XAoBAQlnWvOelbQMS5WUllwg/edit?usp=sharing) proposed by the LatinX in AI Coalition in March of 2019 and conducted in collaboration with the Black in AI Organization and Neural Information Processing Systems Foundation.

## Objectives
- Gather insight on papers rejected from elite AI conferences over the past 30 years
- Analyze differences in papers to intuit common reasons for rejection
- Compare reviews against papers that have been accepted
- Compare differences in rejections for open reviews against single-blind and double-blind reviews
- Develop tools and educational material from these findings that'll further progress and representation for those who have lacked representation at these conferences

### Research Questions
- Have any unexpected biases influenced reviews and rejection of papers?
    - Institutional Affiliation
    - Gender
    - Ethnicity
    - English Fluency


## Scripts
- [Parse NeurIPS review data into CSV for analysis with columns for Q1, Q2, Rebuttals, Paper_id, Title, NeurIPS_edition for use on NeurIPS reviews.](/scripts/neurips_html_toCSV.py)
- [Crawl OpenReview for ICLR review data](/scripts/iclr_data.py)
