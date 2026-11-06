
import csv
import shutil

# Sample dataset: 25 fake and 25 genuine accounts
accounts = [
    ["Instagram", "fake_101", 20, 1800, 2, 15, 5, 0, 0, "fake"],
    ["Instagram", "fake_102", 35, 2500, 1, 10, 3, 0, 0, "fake"],
    ["Instagram", "fake_103", 15, 2000, 0, 5, 2, 0, 0, "fake"],
    ["Instagram", "fake_104", 50, 3000, 3, 20, 4, 0, 0, "fake"],
    ["Instagram", "fake_105", 10, 1500, 1, 8, 2, 0, 0, "fake"],
    ["Instagram", "fake_106", 25, 2200, 2, 12, 5, 0, 0, "fake"],
    ["Instagram", "fake_107", 40, 2800, 1, 18, 3, 0, 0, "fake"],
    ["Instagram", "fake_108", 18, 1900, 0, 7, 2, 0, 0, "fake"],
    ["Instagram", "fake_109", 30, 2400, 2, 14, 4, 0, 0, "fake"],
    ["Instagram", "fake_110", 12, 1600, 1, 6, 3, 0, 0, "fake"],
    ["Instagram", "fake_111", 45, 3100, 2, 22, 5, 0, 0, "fake"],
    ["Instagram", "fake_112", 22, 2100, 1, 11, 3, 0, 0, "fake"],
    ["Instagram", "fake_113", 16, 1700, 0, 9, 2, 0, 0, "fake"],
    ["Instagram", "fake_114", 38, 2600, 2, 16, 4, 0, 0, "fake"],
    ["Instagram", "fake_115", 28, 2300, 1, 13, 3, 0, 0, "fake"],
    ["Instagram", "fake_116", 14, 1800, 0, 8, 2, 0, 0, "fake"],
    ["Instagram", "fake_117", 32, 2700, 2, 19, 4, 0, 0, "fake"],
    ["Instagram", "fake_118", 19, 2000, 1, 10, 3, 0, 0, "fake"],
    ["Instagram", "fake_119", 42, 2900, 2, 21, 5, 0, 0, "fake"],
    ["Instagram", "fake_120", 11, 1400, 0, 4, 2, 0, 0, "fake"],
    ["Instagram", "fake_121", 27, 2250, 1, 12, 4, 0, 0, "fake"],
    ["Instagram", "fake_122", 17, 1850, 0, 7, 2, 0, 0, "fake"],
    ["Instagram", "fake_123", 36, 2550, 2, 17, 4, 0, 0, "fake"],
    ["Instagram", "fake_124", 24, 2150, 1, 9, 3, 0, 0, "fake"],
    ["Instagram", "fake_125", 13, 1650, 0, 6, 2, 0, 0, "fake"],

    ["Instagram", "user_201", 850, 400, 120, 900, 80, 1, 0, "genuine"],
    ["Instagram", "user_202", 1200, 600, 200, 1200, 100, 1, 0, "genuine"],
    ["Instagram", "user_203", 650, 350, 90, 800, 70, 1, 0, "genuine"],
    ["Instagram", "user_204", 2000, 800, 300, 1500, 120, 1, 1, "genuine"],
    ["Instagram", "user_205", 500, 300, 75, 700, 60, 1, 0, "genuine"],
    ["Instagram", "user_206", 1500, 700, 250, 1300, 110, 1, 0, "genuine"],
    ["Instagram", "user_207", 900, 450, 140, 950, 85, 1, 0, "genuine"],
    ["Instagram", "user_208", 3000, 900, 400, 1800, 130, 1, 1, "genuine"],
    ["Instagram", "user_209", 700, 380, 100, 850, 75, 1, 0, "genuine"],
    ["Instagram", "user_210", 1800, 750, 280, 1400, 115, 1, 0, "genuine"],
    ["Instagram", "user_211", 1100, 550, 180, 1100, 95, 1, 0, "genuine"],
    ["Instagram", "user_212", 2500, 850, 350, 1600, 125, 1, 1, "genuine"],
    ["Instagram", "user_213", 600, 320, 85, 750, 65, 1, 0, "genuine"],
    ["Instagram", "user_214", 1400, 650, 220, 1250, 105, 1, 0, "genuine"],
    ["Instagram", "user_215", 950, 480, 150, 1000, 90, 1, 0, "genuine"],
    ["Instagram", "user_216", 2200, 800, 320, 1550, 120, 1, 1, "genuine"],
    ["Instagram", "user_217", 750, 390, 110, 880, 78, 1, 0, "genuine"],
    ["Instagram", "user_218", 1600, 720, 260, 1350, 112, 1, 0, "genuine"],
    ["Instagram", "user_219", 1050, 520, 170, 1050, 92, 1, 0, "genuine"],
    ["Instagram", "user_220", 2800, 880, 380, 1700, 128, 1, 1, "genuine"],
    ["Instagram", "user_221", 550, 310, 80, 720, 62, 1, 0, "genuine"],
    ["Instagram", "user_222", 1300, 620, 210, 1200, 102, 1, 0, "genuine"],
    ["Instagram", "user_223", 800, 420, 130, 920, 82, 1, 0, "genuine"],
    ["Instagram", "user_224", 1900, 780, 290, 1450, 118, 1, 0, "genuine"],
    ["Instagram", "user_225", 1000, 500, 160, 1020, 88, 1, 0, "genuine"]
]

# Column names
headers = [
    "platform",
    "username",
    "followers_count",
    "following_count",
    "posts_count",
    "account_age_days",
    "bio_length",
    "profile_pic",
    "verified",
    "label"
]

# Save the original dataset
with open("collected_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(accounts)

# Create a separate final dataset file
shutil.copyfile("collected_data.csv", "member1_final_dataset.csv")

# Count fake and genuine accounts
fake_count = sum(1 for account in accounts if account[-1] == "fake")
genuine_count = sum(1 for account in accounts if account[-1] == "genuine")

print("DATA COLLECTION COMPLETED!")
print("Total accounts:", len(accounts))
print("Fake accounts:", fake_count)
print("Genuine accounts:", genuine_count)
print("Original dataset saved in collected_data.csv")
print("Final dataset saved in member1_final_dataset.csv")
