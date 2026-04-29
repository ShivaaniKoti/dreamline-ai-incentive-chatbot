from datetime import date

def validate_record(record):
    required_fields = [
        "program_name", "state", "city", "incentive_type",
        "property_type", "description", "eligibility_criteria",
        "incentive_amount", "valid_until", "updated_at",
        "review_needed", "program_links"
    ]

    for field in required_fields:
        if field not in record:
            record[field] = None

    if not record.get("updated_at"):
        record["updated_at"] = str(date.today())

    if not record.get("program_name") or not record.get("description"):
        record["review_needed"] = "Yes"
    elif record.get("review_needed") not in ["Yes", "No"]:
        record["review_needed"] = "No"

    return record