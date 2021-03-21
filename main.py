import os
from anki.storage import Collection

chapter = "lee_riemannian_manifolds_chapter_7.tex"


def get_latex(case, tmp_line, mode):
    first_line = tmp_line
    tmp_line = file_read.readline()
    file_write = open(path_file_write, "w")
    while tmp_line[0:len(case)] != case:
        if tmp_line == r"\begin{remark}":
            file_write.write("<br><br>")
        file_write.write(tmp_line)
        tmp_line = file_read.readline()
    file_write.close()
    last_line = tmp_line
    create_flashcard(first_line, last_line, mode)


def create_flashcard(begin_line, end_line, mode):
    file = open(path_file_write, "r")
    temp_string = file.read()
    # Find the Anki directory
    anki_home = 'C:/Users/Nik/Documents/GitHub/LaTeX_to_Anki_Script/Anki_Sandbox/User 1'
    anki_collection_path = os.path.join(anki_home, "collection.anki2")

    # 1. Load the anki collection
    col = Collection(anki_collection_path, log=True)

    # 2. Select the deck
    # Find the model to use (Basic, Basic with reversed, ...)
    if mode == 1 or 2:
        modelBasic = col.models.byName('1. Definition LaTeX')
    else:
        modelBasic = col.models.byName('2. Proof LaTeX')
    # Set the deck
    deck = col.decks.byName("Default")
    col.decks.select(deck['id'])
    col.decks.current()['mid'] = modelBasic['id']

    # 3. Create a new card
    note = col.newNote()
    if mode == 1:
        note.fields[0] = begin_line + "<br><br>" + r"\end{definition}" + "<br><br>" \
                         + r"\begin{remark}[]" + "<br><br>" + end_line
        note.fields[1] = begin_line + "<br>" + temp_string + "<br>" + end_line
    elif mode == 2:
        note.fields[0] = begin_line + "<br><br>" + end_line
        note.fields[1] = begin_line + "<br>" + temp_string + "<br>" + end_line
    else:
        note.fields[0] = begin_line + "<br>" + temp_string + "<br>" + end_line
        note.fields[1] = "Proof"
    col.addNote(note)

    # 4. Save changes
    col.save()
    file.close()


# Open File: READ
path_dir_read: str = r"C:\Users\Nik\Documents\GitHub\LaTeX\Mathmatical Physics" \
                     r"\Introduction to Riemannian Manifolds\Chapter"
path_file_read = os.sep.join([path_dir_read, chapter])
file_read = open(path_file_read, "r")

# Open File: WRITE
path_dir_write: str = r"C:\Users\Nik\Documents\GitHub\LaTeX_to_Anki_Script\Temp"
temp_file = "temp.txt"
path_file_write = os.sep.join([path_dir_write, temp_file])

# Loop
while True:
    temp_line = file_read.readline()

    if temp_line[0:len(r"\begin{definition}")] == r"\begin{definition}":
        if r"\label" in temp_line:
            get_latex(r"\end{remark}", temp_line, 1)
        else:
            get_latex(r"\end{definition}", temp_line, 2)

    if temp_line[0:len(r"\begin{theorem}")] == r"\begin{theorem}":
        get_latex(r"\end{theorem}", temp_line, 3)

    if temp_line[0:len(r"\begin{proposition}")] == r"\begin{proposition}":
        get_latex(r"\end{proposition}", temp_line, 3)

    if temp_line[0:len(r"\begin{lemma}")] == r"\begin{lemma}":
        get_latex(r"\end{lemma}", temp_line, 3)

    if temp_line[0:len(r"\begin{corollary}")] == r"\begin{corollary}":
        get_latex(r"\end{corollary}", temp_line, 3)

    if temp_line[0:len(r"\begin{remark}")] == r"\begin{remark}":
        get_latex(r"\end{remark}", temp_line, 3)

    if temp_line == "":
        file_read.close()
        break

# cd C:\Users\Nik\Documents\GitHub\LaTeX_to_Anki_Script
# "C:\Program Files\Anki\anki.exe" -b "Anki_Sandbox"
