import csv

def export_csv_jd_resume(jd_data, resume_data, path="skill_gap_report.csv"):
    with open(path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Section", "Skill", "Score/Status"])

        writer.writerow(["--- Resume Skills ---", "", ""])
        for row in resume_data:
            writer.writerow(["Resume", row.get("Resume Skill"), row.get("Similarity Score")])

        writer.writerow(["--- Job Description Coverage ---", "", ""])
        for row in jd_data:
            writer.writerow(["JD", row.get("JD Skill"), row.get("Status")])

    return path
