# PDF to Anki Flashcards

This project converts text extracted from PDF files into Anki flashcards using OpenAI's GPT model and is highly customizable.

## Requirements

- Python 3.x

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/AykoSc/pdfs-to-anki-cards.git
    cd pdfs-to-anki-cards
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

The `config.yaml` file is pre-configured and contains functionalities to:
- split flashcards by pdfs.
- set OpenAI's API key.
- set OpenAI's GPT model.
- ...

## Usage

1. Configure the `config.yaml` file to your needs.

2. Place your PDF files in the folder specified by `source_pdfs_folder` in the `config.yaml` file.

3. Run the script:
    ```sh
    python main.py
    ```

4. The generated flashcards will be saved in the folder specified by `output_txts_folder` in the `config.yaml` file.

## Acknowledgements

This project is based on [PDF2AnkiCards](https://github.com/y0zg/PDF2AnkiCards).