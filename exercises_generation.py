import pandas as pd
import random
import spacy
from sentences_retrieval import retrieve_verb_tense
from exercise_types_creation import generate_grammar_mistake, generate_multiple_choice, generate_fib_verb
from helper_functions import PDF, extra_preprocessing, profanity_check


# Generate mistakes for the Find-mistakes and Multiple-choice exercises
def generate_mistakes_verb(retrieved_tuple, verb_tense, spacy_model, exercise_type):

    mistakes_generations = []
    original_sentences = []

    for elem in retrieved_tuple:
        original_sentence = elem[0]
        sentence_tokens = elem[1]
        target_aux_index = elem[3]
        target_verb_index = elem[4]
        person = elem[6][0]
        number = str(elem[7][0])

        # sometimes the library use a string number instead of a number
        if person == 'One':
            person = 1
        elif person == 'Two':
            person = 2
        elif person == 'Three':
            person = 3
        else:
            person = int(person)

        # verb to be ill-injected
        target_sentence_verb = sentence_tokens[target_verb_index]

        # we take the lemma form of the target verb for better results of the conversion library
        verb_token_model = spacy_model(target_sentence_verb)
        target_verb_lemma = "".join([token.lemma_ for token in verb_token_model])

        if exercise_type == 'mistakes':
            error_exercise = generate_grammar_mistake(sentence_tokens, target_verb_index, target_aux_index, verb_tense, target_verb_lemma, person, number)
        elif exercise_type == 'multiple':
            error_exercise = generate_multiple_choice(sentence_tokens, target_verb_index, target_aux_index, verb_tense, target_verb_lemma, person, number)

        mistakes_generations.append(error_exercise)
        original_sentences.append(original_sentence)

    return (original_sentences, mistakes_generations)


# In this function the selection of the appropriate verb tense, along with the necessary parameters takes place
def verb_tense_generation(corpus, learner_level, sentence_number, verb_tense_couple, exercise_type, shuffle_instances):

    # we aim on retrieving an equal number of sentences for each verb tense
    sentence_number = int(sentence_number / 2)

    # We retrieve the appropriate sentences based on the given parameters each time and we generate the relevant exercise types
    # Simple Present/ Present Progressive
    if verb_tense_couple == 1:

        if exercise_type == 'fib':
            retrieve_simple_present = retrieve_verb_tense(corpus, learner_level, sentence_number, 1, False, 'fib', None)
            retrieve_present_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 3, True, 'fib', None)
            simple_present = generate_fib_verb(retrieve_simple_present)
            present_progressive = generate_fib_verb(retrieve_present_progressive)

        elif exercise_type == 'mistakes':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_simple_present = retrieve_verb_tense(corpus, learner_level, sentence_number, 1, False, 'mistakes', spacy_model)
            retrieve_present_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 3, True, 'mistakes', spacy_model)
            simple_present = generate_mistakes_verb(retrieve_simple_present, 'simple_present', spacy_model, 'mistakes')
            present_progressive = generate_mistakes_verb(retrieve_present_progressive, 'present_progressive', spacy_model, 'mistakes')

        elif exercise_type == 'multiple':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_simple_present = retrieve_verb_tense(corpus, learner_level, sentence_number, 1, False, 'multiple', spacy_model)
            retrieve_present_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 3, True, 'multiple', spacy_model)
            simple_present = generate_mistakes_verb(retrieve_simple_present, 'simple_present', spacy_model, 'multiple',)
            present_progressive = generate_mistakes_verb(retrieve_present_progressive, 'present_progressive', spacy_model, 'multiple',)

        generated_sentences = simple_present[1] + present_progressive[1]
        original_generated_sentences = simple_present[0] + present_progressive[0]

    # Simple Past/ Past Progressive
    elif verb_tense_couple == 2:

        if exercise_type == 'fib':
            retrieve_simple_past = retrieve_verb_tense(corpus, learner_level, sentence_number, 2, False, 'fib', None)
            retrieve_past_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 4, True, 'fib', None)
            simple_past = generate_fib_verb(retrieve_simple_past)
            past_progressive = generate_fib_verb(retrieve_past_progressive)

        elif exercise_type == 'mistakes':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_simple_past = retrieve_verb_tense(corpus, learner_level, sentence_number, 2, False, 'mistakes', spacy_model)
            retrieve_past_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 4, True, 'mistakes', spacy_model)
            simple_past = generate_mistakes_verb(retrieve_simple_past, 'simple_past', spacy_model, 'mistakes')
            past_progressive = generate_mistakes_verb(retrieve_past_progressive, 'past_progressive', spacy_model, 'mistakes')

        elif exercise_type == 'multiple':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_simple_past = retrieve_verb_tense(corpus, learner_level, sentence_number, 2, False, 'multiple', spacy_model)
            retrieve_past_progressive = retrieve_verb_tense(corpus, learner_level, sentence_number, 4, True, 'multiple', spacy_model)
            simple_past = generate_mistakes_verb(retrieve_simple_past, 'simple_past', spacy_model, 'multiple')
            past_progressive = generate_mistakes_verb(retrieve_past_progressive, 'past_progressive', spacy_model, 'multiple')

        generated_sentences = simple_past[1] + past_progressive[1]
        original_generated_sentences = simple_past[0] + past_progressive[0]

    # Present/Past Perfect
    elif verb_tense_couple == 3:

        if exercise_type == 'fib':
            retrieve_present_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 5, True, 'fib', None)
            retrieve_past_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 6, True, 'fib', None)
            present_perfect = generate_fib_verb(retrieve_present_perfect)
            past_perfect = generate_fib_verb(retrieve_past_perfect)

        elif exercise_type == 'mistakes':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_present_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 5, True, 'mistakes', spacy_model)
            retrieve_past_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 6, True, 'mistakes', spacy_model)
            present_perfect = generate_mistakes_verb(retrieve_present_perfect, 'present_perfect', spacy_model, 'mistakes')
            past_perfect = generate_mistakes_verb(retrieve_past_perfect, 'past_perfect', spacy_model, 'mistakes')

        elif exercise_type == 'multiple':
            spacy_model = spacy.load('en_core_web_sm')
            retrieve_present_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 5, True, 'multiple', spacy_model)
            retrieve_past_perfect = retrieve_verb_tense(corpus, learner_level, sentence_number, 6, True, 'multiple', spacy_model)
            present_perfect = generate_mistakes_verb(retrieve_present_perfect, 'present_perfect', spacy_model, 'multiple')
            past_perfect = generate_mistakes_verb(retrieve_past_perfect, 'past_perfect', spacy_model, 'multiple')

        generated_sentences = present_perfect[1] + past_perfect[1]
        original_generated_sentences = present_perfect[0] + past_perfect[0]

    # shuffle for better results
    packed_tuples = [(generated_sentences[index], original_generated_sentences[index]) for index, elem in enumerate(range(len(generated_sentences)))]

    if shuffle_instances:
        random.shuffle(packed_tuples)

    gener_sentences = []
    original_sentences = []

    for tuple_index, elem in enumerate(range(len(packed_tuples))):
        gener_sentences.append(packed_tuples[tuple_index][0])
        original_sentences.append(packed_tuples[tuple_index][1])

    original_fib_tuple = (original_sentences, gener_sentences)

    # check whether enough instances exist in the corpus
    if len(list(original_fib_tuple[1])) < sentence_number:
        if len(list(original_fib_tuple[1])) == 0:
            print("== NOTE: We are very sorry, but it seems that there is no sentence example of that Verb Tense in our corpus. ==")
            print("== Perhaps a different difficulty level might help. == \n")
        else:
            print("== NOTE: We are very sorry, but it seems that there are only {} examples of the given exercise type in our corpus. == \n".format(len(list(original_fib_tuple[1]))))
            print("== Perhaps a different difficulty level might help. == \n")
        return original_fib_tuple

    else:
        return original_fib_tuple


# Generate the pdf exercises file for fill-in-the-blank and find-mistakes exercise
def generate_files_fib_finderror(corpus, learner_level, sentence_number, teach_goal, extra_options):

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)

    if teach_goal[3] == 'fib':
        exercise_type = 'Fill-in-the-blank'
    elif teach_goal[3] == 'mistakes':
        exercise_type = 'Find-the-mistake'
    elif teach_goal[3] == 'multiple':
        exercise_type = 'Multiple-choice'

    # if the teaching goal concerns Verb Tenses
    if teach_goal[1] == 'verb_tense_even':
        if teach_goal[2] == 'Simple_Progressive_Present':
            pdf.cell(190, 0, 'Simple and Progressive Present, {} exercises for {} level'.format(exercise_type, learner_level), 0,0, 'C')
        elif teach_goal[2] == 'Simple_Progressive_Past':
            pdf.cell(190, 0, 'Simple and Progressive Past, {} exercises for {} level'.format(exercise_type, learner_level), 0,0, 'C')

        pdf.ln(15)
        pdf.cell(30, 10, 'Exercises', 0, 0, 'L')
        pdf.ln(15)
        pdf.set_font('Times', '', 10)

        # in case of a shuffling option
        if 'shuffle' in extra_options:
            generated_fib = list(verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], True))
        else:
            generated_fib = list(verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], False))

        clean_results = list(extra_preprocessing(generated_fib[1], generated_fib[0]))

    elif teach_goal[1] == 'verb_tense_odd':
        if teach_goal[2] == 'Perfect_Present_Past':
            pdf.cell(190, 0, 'Present and Past Perfect, {} exercises for {} level'.format(exercise_type, learner_level), 0, 0, 'C')

        pdf.ln(15)
        pdf.cell(30, 10, 'Exercises', 0, 0, 'L')
        pdf.ln(10)
        pdf.set_font('Times', '', 10)

        # in case of a shuffling option
        if 'shuffle' in extra_options:
            generated_fib = list(verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], True))
        else:
            generated_fib = list(verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], False))

        clean_results = list(extra_preprocessing(generated_fib[1], generated_fib[0]))

    for i, item in enumerate(clean_results[1]):
        try:
            pdf.multi_cell(0, 5, "{}. {} \n".format(i + 1, item.encode('latin-1', 'ignore').decode('latin-1')), 0, 1)

            # in case the profanity option is checked
            if 'profanity' in extra_options:
                bad_words = profanity_check(item)

                if bad_words:
                    string_bad_words = ', '.join(bad_words)
                    pdf.set_fill_color(220, 50, 50)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(0, 5, "The sentence {}, contains these possibly topic-sensitive words: {}".format(i+1, string_bad_words.encode('latin-1', 'ignore').decode('latin-1')), 0, 0, 'L', 1)
                    pdf.ln(6)
                    pdf.set_text_color(0, 0, 0)

        except UnicodeEncodeError:
            print("An encoding error has occured for the item: {} \n".format(item))
            print("That item has been skipped.\n")

    # if solutions are asked
    if 'solution' in extra_options:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 13)
        pdf.cell(30, 10, 'Solutions', 0, 0, 'L')
        pdf.ln(10)
        pdf.set_font('Times', '', 10)

        for i, item in enumerate(clean_results[0]):
            try:
                pdf.multi_cell(0, 5, "{}. {} \n".format(i + 1, item.encode('latin-1', 'ignore').decode('latin-1')), 0, 1)
            except UnicodeEncodeError:
                print("An encoding error has occured for the item: {} \n".format(item))
                print("That item has been skipped.\n")

    pdf.output('./static/files/generations/generated_exercises.pdf','F')

    if 'solution' in extra_options:
        return (clean_results[0], clean_results[1])
    else:
        return ('without_solutions', clean_results[1])


# Generate the pdf exercises file for multiple-choice exercise
def generate_files_multiple(corpus, learner_level, sentence_number, teach_goal, extra_options):

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 13)

    if teach_goal[3] == 'fib':
        exercise_type = 'Fill-in-the-blank'
    elif teach_goal[3] == 'mistakes':
        exercise_type = 'Find-the-mistake'
    elif teach_goal[3] == 'multiple':
        exercise_type = 'Multiple-choice'

    # if the teaching goal concerns Verb Tenses
    if teach_goal[1] == 'verb_tense_even':
        if teach_goal[2] == 'Simple_Progressive_Present':
            pdf.cell(190, 0, 'Simple and Progressive Present, {} exercises for {} level'.format(exercise_type, learner_level), 0,0, 'C')
        elif teach_goal[2] == 'Simple_Progressive_Past':
            pdf.cell(190, 0, 'Simple and Progressive Past, {} exercises for {} level'.format(exercise_type, learner_level), 0,0, 'C')

        pdf.ln(15)
        pdf.cell(30, 10, 'Exercises', 0, 0, 'L')
        pdf.ln(15)
        pdf.set_font('Times', '', 10)

        # in case of a shuffle option
        if 'shuffle' in extra_options:
            generated_fib = verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], True)
        else:
            generated_fib = verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], False)

    elif teach_goal[1] == 'verb_tense_odd':
        if teach_goal[2] == 'Perfect_Present_Past':
            pdf.cell(190, 0, 'Present and Past Perfect, {} exercises for {} level'.format(exercise_type, learner_level), 0,0, 'C')

        pdf.ln(15)
        pdf.cell(30, 10, 'Exercises', 0, 0, 'L')
        pdf.ln(10)
        pdf.set_font('Times', '', 10)

        if 'shuffle' in extra_options:
            generated_fib = verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], True)
        else:
            generated_fib = verb_tense_generation(corpus, learner_level, sentence_number, teach_goal[0], teach_goal[3], False)

    # the exercises solutions
    generated_multiple_solutions = generated_fib[0]
    # the fib, correct choice, wrong choice pack
    generated_multiple_pack = generated_fib[1]

    generated_multiple_fib = []
    generated_multiple_correct = []
    generated_multiple_wrong = []

    # unpack the packed generations for better processing
    for elem in generated_multiple_pack:
        generated_multiple_fib.append(elem[0][0])
        generated_multiple_correct.append(elem[0][1])
        generated_multiple_wrong.append(elem[0][2])

    for i, item in enumerate(generated_multiple_solutions):

        try:
            pdf.multi_cell(0, 5, "{}. {} \n".format(i + 1, generated_multiple_fib[i].encode('latin-1', 'ignore').decode('latin-1')), 0, 1)

            # in case the profanity option is checked
            if 'profanity' in extra_options:
                bad_words = profanity_check(item)

                if bad_words:
                    string_bad_words = ', '.join(bad_words)
                    pdf.set_fill_color(220, 50, 50)
                    pdf.set_text_color(255, 255, 255)
                    pdf.cell(0, 5, "The sentence {}, contains these possibly topic-sensitive words: {}".format(i+1, string_bad_words.encode('latin-1', 'ignore').decode('latin-1')), 0, 0, 'L', 1)
                    pdf.ln(6)
                    pdf.set_text_color(0, 0, 0)

            pdf.multi_cell(0, 5, "A. {} \n".format(generated_multiple_correct[i].encode('latin-1', 'ignore').decode('latin-1')), 0, 1)
            pdf.multi_cell(0, 5, "B. {} \n".format(generated_multiple_wrong[i].encode('latin-1', 'ignore').decode('latin-1')), 0, 1)
            pdf.ln(6)

        except UnicodeEncodeError:
            print("An encoding error has occured for the item: {} \n".format(item))
            print("That item has been skipped.\n")

    # if solutions are asked
    if 'solution' in extra_options:
        pdf.ln(5)
        pdf.set_font('Arial', 'B', 13)
        pdf.cell(30, 10, 'Solutions', 0, 0, 'L')
        pdf.ln(10)
        pdf.set_font('Times', '', 10)
        for i, item in enumerate(generated_multiple_solutions):
            try:
                pdf.multi_cell(0, 5, "{}. {} \n".format(i + 1, item.encode('latin-1', 'ignore').decode('latin-1')), 0, 1)
            except UnicodeEncodeError:
                print("An encoding error has occured for the item: {} \n".format(item))
                print("That item has been skipped.\n")

    pdf.output('./static/files/generations/generated_exercises.pdf','F')

    pack_multiple = (generated_multiple_fib, generated_multiple_correct, generated_multiple_wrong)

    if 'solution' in extra_options:
        return (generated_multiple_solutions, pack_multiple)
    else:
        return ('without_solutions', pack_multiple)


def main(retrieved_parameters):

    # unpack the retrieved generation parameters
    resource, instances, difficulty, teaching_goal, extra_options = str(retrieved_parameters).split("_")

    # the input resource
    if resource == 'wikipedia':
        corpus = pd.read_pickle('./data/wikipedia_corpus_complete.pkl')
        corpus = corpus.sample(frac=1).reset_index(drop=True)
    elif resource == 'bnc':
        corpus = pd.read_pickle('./data/bnc_corpus_complete.pkl')
        corpus = corpus.sample(frac=1).reset_index(drop=True)

    # the number of sentences
    sentence_number = int(instances)

    # the difficulty level of the exercises
    learner_level = difficulty

    # the target teaching category
    if teaching_goal == 'fib-present-simple-progr':
        teach_goal = (1, 'verb_tense_even', 'Simple_Progressive_Present', 'fib')
    elif teaching_goal == 'fib-past-simple-progr':
        teach_goal = (2, 'verb_tense_even', 'Simple_Progressive_Past', 'fib')
    elif teaching_goal == 'fib-present-past-perfect':
        teach_goal = (3, 'verb_tense_odd', 'Perfect_Present_Past', 'fib')
    elif teaching_goal == 'mistakes-present-simple-progr':
        teach_goal = (1, 'verb_tense_even', 'Simple_Progressive_Present', 'mistakes')
    elif teaching_goal == 'mistakes-past-simple-progr':
        teach_goal = (2, 'verb_tense_even', 'Simple_Progressive_Past', 'mistakes')
    elif teaching_goal == 'mistakes-present-past-perfect':
        teach_goal = (3, 'verb_tense_odd', 'Perfect_Present_Past', 'mistakes')
    elif teaching_goal == 'multiple-present-simple-progr':
        teach_goal = (1, 'verb_tense_even', 'Simple_Progressive_Present', 'multiple')
    elif teaching_goal == 'multiple-past-simple-progr':
        teach_goal = (2, 'verb_tense_even', 'Simple_Progressive_Past', 'multiple')
    elif teaching_goal == 'multiple-present-past-perfect':
        teach_goal = (3, 'verb_tense_odd', 'Perfect_Present_Past', 'multiple')

    # the generation process is similar for the fib and find-mistakes type and different for the multiple-choice
    if teach_goal[3] == 'multiple':
        return generate_files_multiple(corpus, learner_level, sentence_number, teach_goal, extra_options)
    else:
        return generate_files_fib_finderror(corpus, learner_level, sentence_number, teach_goal, extra_options)