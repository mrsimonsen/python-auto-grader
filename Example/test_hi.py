import hi as student
def main():
    total = 0
    score = 0

    total += 1
    if student.hi() == "hi":
        score += 1
    print(f"{score}/{total}")

if __name__ == '__main__':
    main()
