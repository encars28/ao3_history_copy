from reader import Reader
from getpass import getpass
from pathlib import Path

USERNAME = input("Enter your username: ")
PASSWORD = getpass("Enter your password: ")

DOWNLOADS = downloads = str(Path.home() / "Downloads")

print()
print("Default downloads folder: " + DOWNLOADS)
while True:
    respuesta = input("Do you want to change the default downloads folder? (y/n): ")
    if respuesta.lower() == "y" or respuesta.lower() == "yes":
        DOWNLOADS = input("Enter the path to the folder: ")
        break
    elif respuesta.lower() == "n" or respuesta.lower() == "no":
        break
    else:
        print("Invalid option, please try again")

r = Reader(USERNAME, PASSWORD)

# Both pages follow the same structure, so we can use the same function
print()
print("Obtaining history...")
with open(DOWNLOADS + '/history.txt', 'w') as f:
    f.write("\n".join(r.history.works_urls))

print()
print("Obtaining marked for later...")
with open(DOWNLOADS + '/marked_for_later.txt', 'w') as f:
    f.write("\n".join(r.marked_for_later.works_urls))

print()
print('Security copy finished!')