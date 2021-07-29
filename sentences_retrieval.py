import random
from exercise_types_creation import retrieve_person_number
from pyinflect import getInflection


# This is a function that checks a number of consistency conditions that should be checked, so that
# the results of multiple-choice and Find-mistakes exercises will be valid
def check_exercise_type_consistency(sentence, tokens, aux_index, verb_target_index, auxiliary, spacy_model):
    valid_sentence = True

    # the verb to be converted
    target_sentence_verb = tokens[verb_target_index]

    # a sentence is consistence if between the auxiliary (if exists) and the verb, there is no word interfering
    if not aux_index == None:
        if not tokens[aux_index + 1] == target_sentence_verb:
            valid_sentence = False

    if valid_sentence:
        # another consistency factor is the person number, which is necessary to generate realistic results
        person_number_found = retrieve_person_number(sentence, tokens, aux_index, auxiliary, target_sentence_verb, spacy_model)

        if person_number_found[0]:
            target_person = person_number_found[1][0]
            target_number = person_number_found[1][1]

            verb_token_model = spacy_model(target_sentence_verb)
            target_verb_lemma = "".join([token.lemma_ for token in verb_token_model])

            possible_inflections = ['VBG', 'VBZ', 'VB', 'VBN']
            inflected_correctly = True

            # final consistency factor
            for inflection in possible_inflections:
                changed_verb_form = getInflection(target_verb_lemma, tag=inflection, inflect_oov=True)
                # sentences with verbs that are unknown to the conversion library being used, will be skipped
                if changed_verb_form == None:
                    inflected_correctly = False

            if inflected_correctly:
                return (True, (target_person, target_number))

    return (False, (0,0))


# Query the corpus to obtain all the relevant sentences, corresponding a target teaching goal for verb tenses
# The output are those sentences, along with a relevant set of information, necessary for the generation process
def retrieve_verb_tense(corpus, learner_level, sentences_number, verb_tense, auxiliary, exercise_type, spacy_model):

    # filter the corpus based on the target level
    corpus = corpus[corpus['Level'] == learner_level]

    # shuffle the whole dataset each time for better variety of results
    corpus = corpus.sample(frac=1).reset_index(drop=True)

    # in those lists, every necessary piece of information for the exercise generation process, will be stored
    original_sentences = []
    tokens = []
    lemmas = []
    aux_indices = []
    verb_target_indices = []
    auxiliary_existance = []
    target_person = []
    target_number = []

    for i, row in corpus.iterrows():
        validation_flag = False
        extra_auxiliary = False

        # stop when the asked number of sentences is collected
        if len(original_sentences) == sentences_number:
            break
        else:

            # depending on whether the verb tense contains an auxiliary or not, the implementation slightly changes
            if auxiliary:

                # if a verb exists in the sentence
                if 'VERB' in row['Upos']:
                    # in case more than one verbs exist
                    if row['Upos'].count('VERB')>1:
                        # obtain their indices
                        verb_indices = [i for i in range(len(row['Upos'])) if row['Upos'][i] == 'VERB']
                        # select randomly one of the verbs
                        verb_target_index = random.choice(verb_indices)
                    else:
                        # obtain the index of the single target verb
                        verb_target_index = row['Upos'].index('VERB')

                    # - Present Continuous -
                    if verb_tense == 3:
                        accepted_auxiliaries = ['am', 'are', 'is']
                        # a verb in present continuous should be a VERB, in Present Tense and in a Verb Particle form along with the auxiliaries am, are, is
                        if 'Tense=Pres' in row['Features'][verb_target_index] and 'VerbForm=Part' in row['Features'][verb_target_index]:
                            validation_flag = True

                    # - Past Continuous -
                    elif verb_tense == 4:
                        accepted_auxiliaries = ['was', 'were']
                        # a verb in past continuous should be a verb in present tense and particle form, along with an auxiliary was/were
                        if 'Tense=Pres' in row['Features'][verb_target_index] and 'VerbForm=Part' in row['Features'][verb_target_index]:
                            validation_flag = True

                    # - Present Perfect -
                    elif verb_tense == 5:
                        accepted_auxiliaries = ['have', 'has']
                        # a verb in present perfect should be in the past participle form, along with the auxiliary have/has
                        if 'Tense=Past' in row['Features'][verb_target_index] and 'VerbForm=Part' in row['Features'][verb_target_index]:
                            validation_flag = True
                            extra_auxiliary = True

                    # - Past Perfect -
                    elif verb_tense == 6:
                        accepted_auxiliaries = ['had']
                        # a verb in past perfect should be in the past participle form, along with the auxiliary had
                        if 'Tense=Past' in row['Features'][verb_target_index] and 'VerbForm=Part' in row['Features'][verb_target_index]:
                            validation_flag = True
                            extra_auxiliary = True

                    # if a sentence contains the proper target teaching goal
                    if validation_flag:
                        second_validation_flag = False

                        # search for the first auxiliary that will be found before the target verb
                        for aux_index, search_aux in reversed(list(enumerate(row['Tokens'][:verb_target_index]))):

                            # in case it is an auxiliary that we search for, pass it (it depends on the verb tense)
                            if search_aux.lower() in accepted_auxiliaries:

                                # in case there are more than one auxiliaries (eg. I will have been driving)
                                if extra_auxiliary:

                                    # - Present Perfect -
                                    if verb_tense == 5:
                                        # obtain the next word of that auxiliary for a window of 2
                                        second_aux_index_window1 = row['Tokens'].index(search_aux) + 1
                                        second_aux_index_window2 = row['Tokens'].index(search_aux) + 2

                                        # skip it in the case of auxiliary 'been'
                                        if not row['Tokens'][second_aux_index_window1] == 'been' and not row['Tokens'][second_aux_index_window2] == 'been':
                                            # in that case we will keep the flag false, since the information which will be passed on for the generation will be different
                                            second_validation_flag = False

                                            # for that auxiliary we validate that its head is the target verb (for extra safety)
                                            if row['Head'][aux_index] == row['id'][verb_target_index]:
                                                append_flag = True

                                                # in case of multiple-choice and find-mistakes type of exercise, we validate for extra consistency conditions
                                                if exercise_type == 'mistakes' or exercise_type == 'multiple':
                                                    mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], aux_index, verb_target_index, auxiliary, spacy_model)

                                                    if mistakes_exercise[0]:
                                                        person, number = mistakes_exercise[1]
                                                        target_person.append(person)
                                                        target_number.append(number)
                                                    else:
                                                        append_flag = False

                                                if append_flag:
                                                    original_sentences.append(row['Sentence'])
                                                    tokens.append(row['Tokens'])
                                                    lemmas.append(row['Lemma'])
                                                    aux_indices.append(aux_index)
                                                    verb_target_indices.append(verb_target_index)
                                                    auxiliary_existance.append(auxiliary)

                                    # - Past Perfect -
                                    elif verb_tense == 6:
                                        # obtain the next word of that auxiliary for a window of 2
                                        second_aux_index_window1 = row['Tokens'].index(search_aux) + 1
                                        second_aux_index_window2 = row['Tokens'].index(search_aux) + 2

                                        # check that the word is not the auxiliary 'been'
                                        if not row['Tokens'][second_aux_index_window1] == 'been' and not row['Tokens'][second_aux_index_window2] == 'been':
                                            # in that case we will keep the flag false, since the next lines of code are different
                                            second_validation_flag = False

                                            # for that auxiliary we validate that its head is the target verb (for extra safety)
                                            if row['Head'][aux_index] == row['id'][verb_target_index]:
                                                append_flag = True

                                                if exercise_type == 'mistakes' or exercise_type == 'multiple':
                                                    mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], aux_index, verb_target_index, auxiliary, spacy_model)

                                                    if mistakes_exercise[0]:
                                                        person, number = mistakes_exercise[1]
                                                        target_person.append(person)
                                                        target_number.append(number)
                                                    else:
                                                        append_flag = False

                                                if append_flag:
                                                    original_sentences.append(row['Sentence'])
                                                    tokens.append(row['Tokens'])
                                                    lemmas.append(row['Lemma'])
                                                    aux_indices.append(aux_index)
                                                    verb_target_indices.append(verb_target_index)
                                                    auxiliary_existance.append(auxiliary)

                                    if second_validation_flag:
                                        # for that auxiliary we validate that its head is the target verb (for extra safety)
                                        if row['Head'][aux_index] == row['id'][verb_target_index]:
                                            append_flag = True

                                            if exercise_type == 'mistakes' or exercise_type == 'multiple':
                                                mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], aux_index, verb_target_index, auxiliary, spacy_model)

                                                if mistakes_exercise[0]:
                                                    person, number = mistakes_exercise[1]
                                                    target_person.append(person)
                                                    target_number.append(number)
                                                else:
                                                    append_flag = False

                                            if append_flag:
                                                original_sentences.append(row['Sentence'])
                                                tokens.append(row['Tokens'])
                                                lemmas.append(row['Lemma'])
                                                aux_indices.append(aux_index)
                                                verb_target_indices.append(verb_target_index)
                                                auxiliary_existance.append(auxiliary)

                                # case without more than one auxiliaries
                                else:
                                    # for that auxiliary we validate that its head is the target verb (for extra safety)
                                    if row['Head'][aux_index] == row['id'][verb_target_index]:
                                        append_flag = True

                                        if exercise_type == 'mistakes' or exercise_type == 'multiple':
                                            mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], aux_index, verb_target_index, auxiliary, spacy_model)

                                            if mistakes_exercise[0]:
                                                person, number = mistakes_exercise[1]
                                                target_person.append(person)
                                                target_number.append(number)
                                            else:
                                                append_flag = False

                                        if append_flag:
                                            original_sentences.append(row['Sentence'])
                                            tokens.append(row['Tokens'])
                                            lemmas.append(row['Lemma'])
                                            aux_indices.append(aux_index)
                                            verb_target_indices.append(verb_target_index)
                                            auxiliary_existance.append(auxiliary)


            # This is the case for the verb tenses, without auxiliaries
            else:
                # - Simple Present -
                if verb_tense == 1:
                    # if a verb exists in the sentence
                    if 'VERB' in row['Upos']:
                        # obtain the index of the verb
                        verb_target_index = row['Upos'].index('VERB')

                        # a verb in simple present should be a VERB, in Present Tense and not in a Verb Particle form
                        if 'Tense=Pres' in row['Features'][verb_target_index] and not 'VerbForm=Part' in row['Features'][verb_target_index]:
                            append_flag = True

                            if exercise_type == 'mistakes' or exercise_type == 'multiple':
                                mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], None, verb_target_index, auxiliary, spacy_model)

                                if mistakes_exercise[0]:
                                    person, number = mistakes_exercise[1]
                                    target_person.append(person)
                                    target_number.append(number)
                                else:
                                    append_flag = False

                            if append_flag:
                                original_sentences.append(row['Sentence'])
                                tokens.append(row['Tokens'])
                                lemmas.append(row['Lemma'])
                                aux_indices.append(None)
                                verb_target_indices.append(verb_target_index)
                                auxiliary_existance.append(auxiliary)

                # - Simple Past -
                elif verb_tense == 2:
                    # a verb in simple past should be in past tense VBD
                    if 'VBD' in row['Xpos']:
                        # obtain the index of the target verb
                        verb_target_index = row['Xpos'].index('VBD')
                        append_flag = True

                        if exercise_type == 'mistakes' or exercise_type == 'multiple':
                            mistakes_exercise = check_exercise_type_consistency(row['Sentence'], row['Tokens'], None, verb_target_index, auxiliary, spacy_model)

                            if mistakes_exercise[0]:
                                person, number = mistakes_exercise[1]
                                target_person.append(person)
                                target_number.append(number)
                            else:
                                append_flag = False

                        if append_flag:
                            original_sentences.append(row['Sentence'])
                            tokens.append(row['Tokens'])
                            lemmas.append(row['Lemma'])
                            aux_indices.append(None)
                            verb_target_indices.append(verb_target_index)
                            auxiliary_existance.append(auxiliary)

    if exercise_type == 'mistakes' or exercise_type == 'multiple':
        retrieved_tuple = [(original_sentences[i], tokens[i], lemmas[i], aux_indices[i], verb_target_indices[i], auxiliary_existance[i], target_person[i], target_number[i]) for i, elem in enumerate(original_sentences)]
    else:
        retrieved_tuple = [(original_sentences[i], tokens[i], lemmas[i], aux_indices[i], verb_target_indices[i], auxiliary_existance[i], None, None) for i, elem in enumerate(original_sentences)]

    return retrieved_tuple