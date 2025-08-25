# CounselChat Child-Psych LoRA Project

This project fine-tunes the **[OpenAI GPT-OSS-20B](https://huggingface.co/openai/gpt-oss-20b)** model using **LoRA adapters (8-bit)** to specialize it as an "expert" in child psychology, based on counselor Q&A data. The ultimate objective is to create an LLM that specializes in, and can help with the rising issue of social anxiety in adolescents by creating a bridge between technology and society.

---

## Overview

We use the [CounselChat dataset](https://huggingface.co/datasets/nbertagnolli/counsel-chat), which contains anonymized therapist responses to user-submitted questions.  
From this dataset we extract and filter **child/teen/parent/school-related questions**, clean them, and prepare them for **supervised fine-tuning (SFT)**.

We also intend to draw more data from other sources to obtain a large breadth and depth of data that will amount to a noticeable change in base model behavior. 

The end goal is to train a model that can respond in a supportive, therapist-like style **without making diagnoses or giving medical advice**.

---

## Data Preparation

1. **Load Data**  - Load data from Huggingface, GitHub, or manually (sources in notebook)
2. **Filter for child-related content** - apply a regex-based filter to keep only child-related keywords
3. **Scrub for PII** - scrub all personal details (emails, phone numbers, links, etc.)
4. **Deduplicate** - remove duplicate data

--- 

## Training (more details later)
Once data is ready, training is done using 8-bit LoRA on GPT-OSS-20b.
Key libraries are:
- Transformers
- PEFT 
- TRL
- bitsandbytes

---

## Running in Google Colab
For non-technical collaborators:
1. Open the notebook [in Google Colab](https://colab.research.google.com/)
    - File --> Open notebook --> GitHub --> paste repo URL
2. Change runtime to GPU (for speed, not necessary)
    - Runtime --> Change runtime type --> "GPU"
3. Un-comment and run the install cell at the top of the notebook to install dependencies
4. Run all data prep cells
5. Run training (more details later)

--- 

## Ethics & Safety
- No diagnoses or prescriptions: the assistant must only provide support
- Sensitive data: although all datasets are publicly accessible, all outputs are stripped of PII (mentioned above)
- Escalation: any deployment will include guardrails for cases such as self-harm, abuse, or crisis