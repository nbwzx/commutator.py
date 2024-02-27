import re


def clean(string: str) -> str:
    # Implements the internationalized string preparation algorithm from RFC 4518. https://tools.ietf.org/html/rfc4518#section-2
    string = re.sub(
        '[\u00ad\u1806\u034f\u180b-\u180d\ufe0f-\uff00\ufffc]+', '', string)
    string = re.sub('[\u0009\u000a\u000b\u000c\u000d\u0085]', ' ', string)
    string = re.sub(
        '[\U0001D173-\U0001D17A\U000E0020-\U000E007F\U000e0001]', '', string)
    string = re.sub(
        '[\u0000-\u0008\u000e-\u001f\u007f-\u0084\u0086-\u009f\u06dd\u070f\u180e\u200c-\u200f'
        '\u202a-\u202e\u2060-\u2063\u206a-\u206f\ufeff\ufff9-\ufffb]+',
        '',
        string
    )
    string = string.replace('\u200b', '')
    string = re.sub(
        '[\u00a0\u1680\u2000-\u200a\u2028-\u2029\u202f\u205f\u3000]', ' ', string)
    # [Invisible Unicode characters](https://invisible-characters.com/#:~:text=Invisible%20Unicode%20characters%3F,%2B2800%20BRAILLE%20PATTERN%20BLANK).
    string = re.sub(
        '[\u061c\u115f\u1160\u17b4\u17b5\u2064\u2800\u3164\uffa0]', ' ', string)
    string = re.sub('[\U0001D159]', ' ', string)

    # Speficially for this project.
    string = re.sub('[!！]', ' ', string)
    string = re.sub(r'\s+', ' ', string)
    string = string.strip()
    non_standard_characters = {
        "'": "｀΄＇ˈˊᑊˋꞌᛌ‘’՚‛՝`′׳´ʹ˴ߴ‵ߵʻʼ᾽ʽ῾ʾ᾿ʿ",
        ",": "¸ꓹ‚؍٫，",
        "/": "⁄Ⳇ⟋ノ╱〳∕⧸",
        ":": "︰∶:᛬⁚܃：ꓽ׃։ː꞉܄˸" + ";",
        "(": "（" + "{",
        ")": "）" + "}",
        "[": "【",
        "]": "】",
        "+": "𐊛+᛭",
        "*": "×"
    }
    for standard_char, chars in non_standard_characters.items():
        for char in chars:
            string = string.replace(char, standard_char)
    return string
