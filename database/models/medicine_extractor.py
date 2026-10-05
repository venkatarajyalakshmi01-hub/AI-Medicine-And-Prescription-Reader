import re


def extract_medicine_details(text):

    medicines = []

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Find medicine strength such as 500 mg, 250 mg, 5 ml
        strength_match = re.search(
            r'\b\d+(?:\.\d+)?\s*(?:mg|ml|g|mcg)\b',
            line,
            re.IGNORECASE
        )

        strength = strength_match.group() if strength_match else ""

        # Find dosage patterns
        dosage_match = re.search(
            r'\b\d+\s*(?:tablet|tablets|tab|capsule|capsules|cap|ml)\b',
            line,
            re.IGNORECASE
        )

        dosage = dosage_match.group() if dosage_match else ""

        # Find frequency
        frequency_match = re.search(
            r'\b(?:once|twice|thrice|once daily|twice daily|'
            r'thrice daily|1-0-1|1-1-1|0-1-0|1-0-0)\b',
            line,
            re.IGNORECASE
        )

        frequency = frequency_match.group() if frequency_match else ""

        # Remove extracted details to get possible medicine name
        medicine_name = line

        if strength:
            medicine_name = medicine_name.replace(strength, "")

        if dosage:
            medicine_name = medicine_name.replace(dosage, "")

        if frequency:
            medicine_name = medicine_name.replace(frequency, "")

        medicine_name = medicine_name.strip(" ,:-")

        if medicine_name:

            medicines.append({
                "medicine_name": medicine_name,
                "strength": strength,
                "dosage": dosage,
                "frequency": frequency
            })

    return medicines