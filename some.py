import os
import shutil

# ১. যে ফোল্ডারটি অর্গানাইজ করতে চান তার পাথ দিন
SOURCE_DIR = r"C:\Users\YourUsername\Downloads"

# ২. ফাইল এক্সটেনশন অনুযায়ী ফোল্ডারের ক্যাটাগরি সেট করুন
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".html", ".css", ".js", ".cpp"]
}

def organize_folder():
    # ফোল্ডারের ভেতরের সব ফাইল ও ফোল্ডারের নাম পান
    files = os.listdir(SOURCE_DIR)

    for file_name in files:
        file_path = os.path.join(SOURCE_DIR, file_name)

        # যদি এটি ফাইল না হয়ে ফোল্ডার হয়, তবে সেটি এড়িয়ে যান
        if os.path.isdir(file_path):
            continue

        # ফাইলের এক্সটেনশন আলাদা করুন
        _, extension = os.path.splitext(file_name)
        extension = extension.lower()

        moved = False

        # ক্যাটাগরি চেক করে ফাইল সরানোর প্রসেস
        for category, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                category_path = os.path.join(SOURCE_DIR, category)

                # ক্যাটাগরি ফোল্ডার না থাকলে তৈরি করুন
                if not os.path.exists(category_path):
                    os.makedirs(category_path)

                # ফাইলটি নতুন ফোল্ডারে নিয়ে যান
                shutil.move(file_path, os.path.join(category_path, file_name))
                print(f"Moved: {file_name} ---> {category}/")
                moved = True
                break

        # তালিকাভুক্ত এক্সটেনশন না মিললে "Others" ফোল্ডারে রাখুন
        if not moved and extension:
            others_path = os.path.join(SOURCE_DIR, "Others")
            if not os.path.exists(others_path):
                os.makedirs(others_path)
            shutil.move(file_path, os.path.join(others_path, file_name))
            print(f"Moved: {file_name} ---> Others/")

if __name__ == "__main__":
    organize_folder()
    print("ফোল্ডার অর্গানাইজ সম্পন্ন হয়েছে!")