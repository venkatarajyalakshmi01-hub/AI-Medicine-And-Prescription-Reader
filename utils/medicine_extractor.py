import re
import os
import pandas as pd
from difflib import SequenceMatcher


# =====================================================
# LOAD MEDICINE DATABASE
# =====================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

CSV_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "medicines.csv"
)


def load_medicine_database():

    try:

        df = pd.read_csv(
            CSV_PATH,
            encoding="utf-8-sig"
        )

        df = df.dropna(
            subset=["Medicine Name"]
        )

        df["Medicine Name"] = (
            df["Medicine Name"]
            .astype(str)
            .str.strip()
        )

        return df

    except Exception as error:

        print(
            "Medicine database error:",
            error
        )

        return pd.DataFrame()


# =====================================================
# TEXT NORMALIZATION
# =====================================================

def normalize_text(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =====================================================
# FIND MEDICINE FROM DATABASE
# =====================================================

def find_best_medicine_match(
    medicine_text,
    df
):

    if df.empty:
        return None, 0

    normalized_text = normalize_text(
        medicine_text
    )

    if not normalized_text:
        return None, 0

    best_match = None
    best_score = 0

    for medicine_name in df["Medicine Name"]:

        normalized_name = normalize_text(
            medicine_name
        )

        # ---------------------------------------------
        # EXACT / PARTIAL MATCH
        # ---------------------------------------------

        if normalized_name in normalized_text:

            return medicine_name, 1.0

        # ---------------------------------------------
        # FUZZY MATCH
        # ---------------------------------------------

        score = SequenceMatcher(
            None,
            normalized_text,
            normalized_name
        ).ratio()

        if score > best_score:

            best_score = score
            best_match = medicine_name

    return best_match, best_score


# =====================================================
# EXTRACT BASIC DETAILS
# =====================================================

def extract_basic_details(line):

    strength_match = re.search(
        r"\b\d+(?:\.\d+)?\s*(?:mg|ml|g|mcg|%|mg/ml)\b",
        line,
        re.IGNORECASE
    )

    strength = (
        strength_match.group()
        if strength_match
        else ""
    )

    dosage_match = re.search(
        r"\b\d+\s*(?:tablet|tablets|tab|capsule|capsules|cap|ml|drop|drops|puff|puffs)\b",
        line,
        re.IGNORECASE
    )

    dosage = (
        dosage_match.group()
        if dosage_match
        else ""
    )

    frequency_match = re.search(
        r"\b(?:once daily|twice daily|thrice daily|"
        r"once|twice|thrice|"
        r"1-0-1|1-1-1|0-1-0|1-0-0|0-0-1|1-1-0)\b",
        line,
        re.IGNORECASE
    )

    frequency = (
        frequency_match.group()
        if frequency_match
        else ""
    )

    duration_match = re.search(
        r"\b\d+\s*(?:day|days|week|weeks|month|months)\b",
        line,
        re.IGNORECASE
    )

    duration = (
        duration_match.group()
        if duration_match
        else ""
    )

    instruction_match = re.search(
        r"\b(?:after food|before food|with food|"
        r"without food|before meals|after meals|"
        r"at night|in the morning|empty stomach)\b",
        line,
        re.IGNORECASE
    )

    instructions = (
        instruction_match.group()
        if instruction_match
        else ""
    )

    return (
        strength,
        dosage,
        frequency,
        duration,
        instructions
    )


# =====================================================
# MAIN MEDICINE EXTRACTION
# =====================================================

def extract_medicine_details(text):

    medicines = []

    df = load_medicine_database()

    if df.empty:

        print(
            "Medicine database is empty."
        )

        return medicines

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if len(line) < 4:
            continue

        # ---------------------------------------------
        # EXTRACT DETAILS
        # ---------------------------------------------

        (
            strength,
            dosage,
            frequency,
            duration,
            instructions
        ) = extract_basic_details(line)

        # ---------------------------------------------
        # REMOVE DETAILS FROM LINE
        # ---------------------------------------------

        medicine_text = line

        for value in [
            strength,
            dosage,
            frequency,
            duration,
            instructions
        ]:

            if value:

                medicine_text = medicine_text.replace(
                    value,
                    ""
                )

        medicine_text = medicine_text.strip(
            " ,:-"
        )

        if not medicine_text:
            continue

        # ---------------------------------------------
        # FIND MEDICINE IN DATASET
        # ---------------------------------------------

        matched_name, confidence = (
            find_best_medicine_match(
                medicine_text,
                df
            )
        )

        # ---------------------------------------------
        # ONLY ACCEPT DATASET MEDICINES
        # ---------------------------------------------

        if (
            matched_name
            and confidence >= 0.85
        ):

            medicine_rows = df[
                df["Medicine Name"]
                == matched_name
            ]

            if medicine_rows.empty:
                continue

            medicine_row = medicine_rows.iloc[0]

            # -----------------------------------------
            # AVOID DUPLICATES
            # -----------------------------------------

            already_exists = any(
                item["medicine_name"]
                == matched_name
                for item in medicines
            )

            if already_exists:
                continue

            medicines.append({

                "medicine_name":
                    matched_name,

                "strength":
                    strength,

                "dosage":
                    dosage,

                "frequency":
                    frequency,

                "duration":
                    duration,

                "instructions":
                    instructions,

                "match_status":
                    "Matched",

                "confidence":
                    round(
                        confidence * 100,
                        2
                    ),

                "composition":
                    medicine_row.get(
                        "Composition",
                        ""
                    ),

                "uses":
                    medicine_row.get(
                        "Uses",
                        ""
                    ),

                "side_effects":
                    medicine_row.get(
                        "Side_effects",
                        ""
                    ),

                "manufacturer":
                    medicine_row.get(
                        "Manufacturer",
                        ""
                    )
            })

        # ---------------------------------------------
        # IMPORTANT:
        # IF NOT FOUND -> DO NOTHING
        # ---------------------------------------------

        else:

            continue

    return medicines