import pandas as pd
from scraper import scrape_page_text
from ai_extractor import extract_incentive_data

urls = [
    "https://www.irs.gov/credits-deductions/residential-clean-energy-credit",
    "https://mysafeflhome.com/",
    "https://www.tampaelectric.com/residential/saveenergy/rebates/"
]

records = []

for url in urls:
    print(f"Processing: {url}")

    try:
        text = scrape_page_text(url)
        data = extract_incentive_data(text, url)

        records.append(data)
        print("Success")

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

df = pd.DataFrame(records)

columns = [
    "program_name",
    "state",
    "city",
    "incentive_type",
    "property_type",
    "description",
    "eligibility_criteria",
    "incentive_amount",
    "valid_until",
    "updated_at",
    "review_needed",
    "program_links"
]

df = df[columns]

df.to_csv("output/shivaani_extracted_tampa_incentives.csv", index=False)

print("CSV created successfully!")
