import importlib.util

def tests(file):
    spec = importlib.util.spec_from_file_location(file,f"./{file}")
    student = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student)
    total = 1
    score = 0

    if student.hi() == "hi":
        score += 1


    rep = f"{score}/{total}"
    return rep
