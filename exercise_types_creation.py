from pyinflect import getInflection
from helper_functions import join_punctuation


# This is the function were the FIB type for verbs is generated
def generate_fib_verb(retrieved_tuple):
    fib_sentences = []
    original_sentences = []

    for tup in retrieved_tuple:
        sentences_solution = tup[0]
        tokens = tup[1]
        lemmas = tup[2]
        aux_index = tup[3]
        verb_target_index = tup[4]
        auxiliary = tup[5]

        if auxiliary:
            # If there is no word, interefering between the auxiliary and the target verb, we will only need one blank space.
            # Otherwise we will need one blank space for the auxiliary and one for the target verb.
            if not len(tokens[aux_index:verb_target_index]) == 1:
                tokens[aux_index] = "____"
                tokens[verb_target_index] = "____________({})".format(lemmas[verb_target_index])
            else:
                tokens[aux_index] = ""
                tokens[verb_target_index] = "____________({})".format(lemmas[verb_target_index])

            # create the final sentences
            fib = ' '.join([str(word) for word in tokens])

        # In the case of no auxiliary, just one blank will be necessary.
        else:
            tokens[verb_target_index] = "____________({})".format(lemmas[verb_target_index])
            fib = ' '.join([str(word) for word in tokens])

        # those are the actual FIB exercises
        fib_sentences.append(fib)
        # those will serve as exercise solutions
        original_sentences.append(sentences_solution)

    return (original_sentences, fib_sentences)


# The person number of a given verb, is necessary both for the multiple-choice as long as the Find-mistakes exercises
def retrieve_person_number(sentence_text, sentence_tokens, target_aux_index, exist_auxiliary, target_sentence_verb, spacy_model):

    # obtain the verb auxiliary of the sentence in case it exists
    if exist_auxiliary:
        target_sentence_auxiliary = sentence_tokens[target_aux_index]

    # initially we want to check that the Person number information is provided by the parser, otherwise we skip the sentence
    verb_token_model = spacy_model(sentence_text)
    person_number_found = False

    if exist_auxiliary:
        for token in verb_token_model:

            # In case a verb in a target sentence has an auxiliary, the person and the number will be obtained based on it
            if token.dep_ == 'aux' and token.text == target_sentence_auxiliary and token.head.text == target_sentence_verb:
                target_person = token.morph.get("Person")
                target_number = token.morph.get("Number")

                # we need to find both the person and the number
                if target_person and target_number:
                    person_number_found = True

            # in case the person number was not provided with the auxiliary, we can also check for the subject of the verb
            elif token.dep_ == 'nsubj' and token.head.text == target_sentence_verb:
                target_person = token.morph.get("Person")
                target_number = token.morph.get("Number")

                if target_person and target_number:
                    person_number_found = True

            if person_number_found:
                break

    # in case there is no auxiliary, the person number should be found by the subject of the verb
    else:
        for token in verb_token_model:
            if token.dep_ == 'nsubj' and token.head.text == target_sentence_verb:
                target_person = token.morph.get("Person")
                target_number = token.morph.get("Number")

                if target_person and target_number:
                    person_number_found = True

                if person_number_found:
                    break

    if person_number_found:
        return (True, (target_person, target_number))
    else:
        return (False, (0,0))


# Formation of find-mistakes exercises
def generate_grammar_mistake(sentence_tokens, target_verb_index, target_aux_index, verb_tense, target_verb_lemma, person, number):

    # For each verb tense, the transformation will be slightly different
    # For the simple present, the verb is converted in a gerund verb form and an auxiliary is inserted given the right person.
    if verb_tense == 'simple_present':

        # change the verb form
        changed_verb_form = getInflection(target_verb_lemma, tag='VBG', inflect_oov=True)
        person = int(person)
        number = str(number)

        if person == 1 and number=='Sing':
            auxiliary_change = 'am'
        elif person == 2 and number=='Sing':
            auxiliary_change = 'are'
        elif person == 3 and number=='Sing':
            auxiliary_change = 'is'
        elif person == 1 and number=='Plur':
            auxiliary_change = 'are'
        elif person == 2 and number=='Plur':
            auxiliary_change = 'are'
        elif person == 3 and number=='Plur':
            auxiliary_change = 'are'

        sentence_tokens[target_verb_index] = changed_verb_form[0]
        sentence_tokens.insert(target_verb_index, auxiliary_change)

    # For the present progressive, the verb is converted in a base form and the auxiliary is deleted.
    elif verb_tense == 'present_progressive':
        if person == 3 and number == 'Sing':
            changed_verb_form = getInflection(target_verb_lemma, tag='VBZ', inflect_oov=True)
        else:
            changed_verb_form = getInflection(target_verb_lemma, tag='VB', inflect_oov=True)

        sentence_tokens[target_verb_index] = changed_verb_form[0]
        del sentence_tokens[target_aux_index]

    # For the simple past, the verb is converted into the gerund form and an auxiliary is inserted based on the person.
    elif verb_tense == 'simple_past':
        # change the verb form
        changed_verb_form = getInflection(target_verb_lemma, tag='VBG', inflect_oov=True)

        if person == 1 and number == 'Sing':
            auxiliary_change = 'was'
        elif person == 2 and number == 'Sing':
            auxiliary_change = 'were'
        elif person == 3 and number == 'Sing':
            auxiliary_change = 'was'
        elif person == 1 and number == 'Plur':
            auxiliary_change = 'were'
        elif person == 2 and number == 'Plur':
            auxiliary_change = 'were'
        elif person == 3 and number == 'Plur':
            auxiliary_change = 'were'

        sentence_tokens[target_verb_index] = changed_verb_form[0]
        sentence_tokens.insert(target_verb_index, auxiliary_change)

    # For the past progressive, the verb is converted into the past participle and the auxiliary is deleted.
    elif verb_tense == 'past_progressive':
        changed_verb_form = getInflection(target_verb_lemma, tag='VBN', inflect_oov=True)
        sentence_tokens[target_verb_index] = changed_verb_form[0]
        del sentence_tokens[target_aux_index]

    # For the present perfect, the auxiliary is changed with the auxiliary of past perfect
    elif verb_tense == 'present_perfect':
        sentence_tokens[target_aux_index] = 'had'

    # For the past perfect, the auxiliary is changed with the auxiliaries of present perfect, according the right number
    elif verb_tense == 'past_perfect':
        if person == 3 and number == 'Sing':
            auxiliary_change = 'has'
        else:
            auxiliary_change = 'have'
        sentence_tokens[target_aux_index] = auxiliary_change

    error_injected_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ',' ')

    return error_injected_sentence


# Formation of multiple choice exercises
def generate_multiple_choice(sentence_tokens, target_verb_index, target_aux_index, verb_tense, target_verb_lemma, person, number):

    generated_distractors = []

    # For each verb tense, the transformation will be slightly different
    # For the simple present, the verb is converted in a gerund verb form and an auxiliary is inserted given the right person.
    if verb_tense == 'simple_present':
        # change the verb form
        changed_verb_form = getInflection(target_verb_lemma, tag='VBG', inflect_oov=True)
        person = int(person)
        number = str(number)

        if person == 1 and number == 'Sing':
            auxiliary_change = 'am'
        elif person == 2 and number == 'Sing':
            auxiliary_change = 'are'
        elif person == 3 and number == 'Sing':
            auxiliary_change = 'is'
        elif person == 1 and number == 'Plur':
            auxiliary_change = 'are'
        elif person == 2 and number == 'Plur':
            auxiliary_change = 'are'
        elif person == 3 and number == 'Plur':
            auxiliary_change = 'are'

        correct_choice = sentence_tokens[target_verb_index]
        wrong_choice = auxiliary_change + ' ' + changed_verb_form[0]
        sentence_tokens[target_verb_index] = "____________"
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    # For the present progressive, the verb is converted in a base form and the auxiliary is deleted.
    elif verb_tense == 'present_progressive':
        if person == 3 and number == 'Sing':
            changed_verb_form = getInflection(target_verb_lemma, tag='VBZ', inflect_oov=True)
        else:
            changed_verb_form = getInflection(target_verb_lemma, tag='VB', inflect_oov=True)

        correct_choice = sentence_tokens[target_aux_index] + ' ' + sentence_tokens[target_verb_index]
        wrong_choice = changed_verb_form[0]
        sentence_tokens[target_verb_index] = "____________"
        del sentence_tokens[target_aux_index]
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    # For the simple past, the verb is converted into the gerund form and an auxiliary is inserted based on the person.
    elif verb_tense == 'simple_past':
        changed_verb_form = getInflection(target_verb_lemma, tag='VBG', inflect_oov=True)

        if person == 1 and number == 'Sing':
            auxiliary_change = 'was'
        elif person == 2 and number == 'Sing':
            auxiliary_change = 'were'
        elif person == 3 and number == 'Sing':
            auxiliary_change = 'was'
        elif person == 1 and number == 'Plur':
            auxiliary_change = 'were'
        elif person == 2 and number == 'Plur':
            auxiliary_change = 'were'
        elif person == 3 and number == 'Plur':
            auxiliary_change = 'were'

        correct_choice = sentence_tokens[target_verb_index]
        wrong_choice = auxiliary_change + ' ' + changed_verb_form[0]
        sentence_tokens[target_verb_index] = "____________"
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    # For the past progressive, the verb is converted into the past participle and the auxiliary is deleted.
    elif verb_tense == 'past_progressive':
        changed_verb_form = getInflection(target_verb_lemma, tag='VBN', inflect_oov=True)

        correct_choice = sentence_tokens[target_aux_index] + ' ' + sentence_tokens[target_verb_index]
        wrong_choice = changed_verb_form[0]
        sentence_tokens[target_verb_index] = "____________"
        del sentence_tokens[target_aux_index]
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    # For the present perfect, the auxiliary is changed with the auxiliary of past perfect
    elif verb_tense == 'present_perfect':

        correct_choice = sentence_tokens[target_aux_index] + ' ' + sentence_tokens[target_verb_index]
        wrong_choice = 'had' + ' ' + sentence_tokens[target_verb_index]
        sentence_tokens[target_verb_index] = "____________"
        del sentence_tokens[target_aux_index]
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    # For the past perfect, the auxiliary is changed with the auxiliaries of present perfect, according the right number
    elif verb_tense == 'past_perfect':
        if person == 3 and number == 'Sing':
            auxiliary_change = 'has'
        else:
            auxiliary_change = 'have'

        correct_choice = sentence_tokens[target_aux_index] + ' ' + sentence_tokens[target_verb_index]
        wrong_choice = auxiliary_change + ' ' + sentence_tokens[target_verb_index]
        sentence_tokens[target_verb_index] = "____________"
        del sentence_tokens[target_aux_index]
        fib_sentence = ' '.join(join_punctuation(sentence_tokens)).replace('  ', ' ')

        generated_distractors.append([fib_sentence, correct_choice, wrong_choice])

    return generated_distractors