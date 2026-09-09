from ai.translator import translate_hindi_to_santali


def generate_worksheet(class_name: str, subject: str, topic: str) -> dict:

    questions = [
        "जोड़िए: 2 + 3 = ______",
        "जोड़िए: 4 + 5 = ______",
        "जोड़िए: 6 + 2 = ______",
        "जोड़िए: 7 + 1 = ______",
        "जोड़िए: 3 + 4 = ______"
    ]

    santali_questions = []

    for question in questions:
        santali_questions.append(
            translate_hindi_to_santali(question)
        )

    return {
        "class": class_name,
        "subject": subject,
        "topic": topic,
        "hindi": questions,
        "santali": santali_questions
    }