import PyPDF2
from openai import OpenAI
import os
import yaml

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

client = OpenAI(api_key=config['api_key'] if config['api_key'] else os.getenv("OPENAI_API_KEY"))


def read_pdfs_in_folder(folder_path):
    pdf_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = " ".join([page.extract_text() for page in reader.pages])
                pdf_texts[filename] = text
    return pdf_texts


def divide_text(text, section_size):
    sections = []
    start = 0
    end = section_size
    while start < len(text):
        section = text[start:end]
        sections.append(section)
        start = end
        end += section_size
    return sections


def create_anki_cards(text, batch_size, output_file):
    section_size = config['section_size']
    divided_sections = divide_text(text, section_size)
    print(f"Divided text into {len(divided_sections)} sections")
    generated_flashcards = ' '
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    open(output_file, "w", encoding='utf-8').close()
    for i, text in enumerate(divided_sections):
        if i % batch_size == 0:
            print(f"Processing batch starting with section {i}")
            generated_flashcards = ''

        try:
            messages = [
                {"role": "system", "content": config['system_message']},
                {"role": "user", "content": config['user_message'] + text}
            ]

            response = client.chat.completions.create(
                model=config['model_name'],
                messages=messages,
                temperature=0.3,
                max_tokens=4096)

            response_from_api = response.choices[0].message.content
            generated_flashcards += response_from_api
        except Exception as e:
            print(f"An error occurred in section {i}: {e}")

        if i % batch_size == batch_size - 1 or i == len(divided_sections) - 1:
            print(f"Completed processing up to section {i}")

            with open(output_file, "a", encoding='utf-8') as f:
                f.write(generated_flashcards)

    print("Finished generating flashcards")


if __name__ == "__main__":
    if not os.path.exists(config['source_pdfs_folder']) or not os.listdir(config['source_pdfs_folder']):
        print(f"Error: No PDF files found in {config['source_pdfs_folder']}")
    else:
        pdf_texts = read_pdfs_in_folder(config['source_pdfs_folder'])
        if config['separate_flashcard_txt_per_pdf']:
            for filename, text in pdf_texts.items():
                output_file = config['output_txts_folder'] + "/" + os.path.splitext(filename)[0] + "_flashcards.txt"
                create_anki_cards(text, config['batch_size'], output_file)
        else:
            combined_text = "\n".join(pdf_texts.values())
            create_anki_cards(combined_text, config['batch_size'], config['output_txts_folder'] + "/flashcards.txt")
