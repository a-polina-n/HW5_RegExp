import re
import os
import shutil


def salty(text):
    """
    Translates a string from russian to the "salty" language by inserting
    cyrillic 'с' + previous vowel after every vowel in the original string.

    Args:
        text (str): Input string that supposed to be translated.

    Returns:
        str: Translated to the salty language string.
    """
    result = re.sub(r'([аеёиуыоэюяАЕЁИОУЫЭЮЯ])+', r'\1c\1', text)
    return result


def chords(path):
    """
    Extracts basic musical chords from a text song file.
    Can get chords A, B, C, D, E, F, G, H, Am, Em, Dm, Fm, Gm.

    Args:
        path (str): Path to the text file containing song lyrics with chords.

    Returns:
        set: A set of unique chords found in the file.
    """

    chord_pattern = r"\b[A-H]m?\b"
    text = open(path, encoding="utf-8").read()
    found_chords = re.findall(chord_pattern, text)
    return set(found_chords)


def rename_files(dir, pattern, new_pattern=None, sample_names=None, to_replace=False):
    """
    Renames files in a directory by pattern replacement, by a sample name dictionary,
    or by using both methods.

    Args:
        dir (str): Path to the directory that contains files.
        pattern (str): Regular expression pattern to found filenames for renaming.
        new_pattern (str, optional): Replacement pattern for matched filenames.
        sample_names (dict, optional): Dictionary of sample renaming rules, e.g. {'G1': 'WT_rep1'}.
                                       If provided, applied after pattern replacement.
        to_replace (bool, default=False): If true, renames original files.
                                          If false, creates copies with new names.

    Returns:
        None
    """
    for filename in os.listdir(dir):
        if not re.search(pattern, filename):
            continue
        new_name = filename

        if new_pattern is not None:
            new_name = re.sub(pattern, new_pattern, new_name)

        if sample_names is not None:
            for old_sample, new_sample in sample_names.items():
                new_name = new_name.replace(old_sample, new_sample)

        old_path = os.path.join(dir, filename)
        new_path = os.path.join(dir, new_name)

        if to_replace:
            os.rename(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)