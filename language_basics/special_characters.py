""" special_characters.py - (c) 2024 by MFH

unicode points and other things related to special characters

# ref: https://stackoverflow.com/questions/17908593/how-to-find-the-unicode-of-the-subscript-alphabet
# and Wikipedia/Unicode_character_tables 
''.join(unicodedata.lookup("GREEK CAPITAL LETTER "+n.upper()) for n in "alpha beta gamma delta epsilon theta iota phi rho psi chi".split())
'ΑΒΓΔΕΘΙΦΡΨΧ'
''.join(unicodedata.lookup("GREEK SMALL LETTER "+n.upper()) for n in "alpha beta gamma delta epsilon theta iota phi rho psi chi".split())
'αβγδεθιφρψχ'

"""
import unicodedata

class Script(str):
    """This class groups tables and functions for sub- and superscript unicode characters.
    Usage: Script("Hello!").sup() => 'ᴴᵉˡˡᵒꜝ' 
    """
    normal = {'digits': "0123456789+-=().!$−＋¡⊥∨≠∪∩⊃∘°∙".encode(),
              'upper': range(65,65+26),
              'lower': range(97,97+26),
              'greek': 'αβγδεθιφρψχ'.encode()
             }
    superscript = {  'digits': "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ᐧꜝᙚᐨᐩꜞᗮᘁᙾᐡᐢᐣᐤᣞᣟ",
                     'upper': "ᴬᴮ ᴰᴱ ᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾ ᴿ ᵀᵁⱽᵂ  ᙆ",
                     'lower': "ᵃᵇᶜᵈᵉᶠᵍʰⁱʲᵏˡᵐⁿᵒᵖ ʳˢᵗᵘᵛʷˣʸᶻ",
                     'greek': "ᵅᵝᵞᵟᵋᶿᶥᶲ ᵠᵡ", # missing: rho
                  }
    subscript = {  'digits': "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎",
                   'lower': "ₐ   ₑ  ₕᵢⱼₖₗₘₙₒₚ ᵣₛₜᵤᵥ ₓ ",
                   'greek': " ᵦᵧ     ᵨᵩᵪ", }
    def sup(self): return self.translate(self.superscript)
    def sub(self): return self.translate(self.subscript)
for tag,table in (('sup', Script.superscript), ('sub', Script.subscript)):
        table.update((letter, translation if translation !=' ' else f"<{tag}>{letter}</{tag}>")
                     for category in tuple(table)
                     for letter, translation in zip(Script.normal[category],table[category]))
