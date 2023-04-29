from datetime import datetime


class Logger:
    @staticmethod
    def log_question_and_answer(image, question, answer):
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        image.save(f"log_shot_{timestamp}.png")
        with open(f"log_question_{timestamp}.txt", "w") as text_file:
            text_file.write(question)
        with open(f"log_answer_{timestamp}.txt", "w") as text_file:
            text_file.write(str(answer.id) + '\n\n' + answer.text)
