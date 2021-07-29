from fpdf import FPDF
from better_profanity import profanity


# preprocessing function to join a list into a string, without spaces between punctuation
def join_punctuation(seq, characters='.,;?!"'):
    characters = set(characters)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt
    yield current


# extra cleaning function of the final exercises output
def extra_preprocessing(generated_fib, original_sentences):
    for i, elem in enumerate(range(len(generated_fib))):
        generated_fib[i] = generated_fib[i].replace(" ,", ",").replace(" .", ".").replace(" ;", "").replace(" : ",":").replace(
            " %", "%").replace(" '", "'")
        original_sentences[i] = original_sentences[i].replace(" ,", ",").replace(" .", ".").replace(" ;", ";").replace(
            " : ", ":").replace(" %", "%").replace(" '", "'")

    return (original_sentences, generated_fib)


# for every sentence a profanity check is also applied, to indicate the inappropriate words
def profanity_check(text):
    # check for inappropriate words
    censored = profanity.censor(text)
    tokenized = censored.split()

    bad_indices = [i for i, elem in enumerate(tokenized) if elem =='****']
    bad_words = [word for i, word in enumerate(text.split()) if i in bad_indices]

    if bad_words:
        return bad_words
    else:
        return False


# this PDF class will be used to generate the pdf files
class PDF(FPDF):
    def header(self):
        # Logo
        self.image('./static/img/logo_semigramex.png', 80, 9, 46)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(60)
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')