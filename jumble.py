import logging
import sys
from argparse import ArgumentParser

initial_input_length = 0
logger = logging.getLogger()


def setup_logger(loglevel):
    global logger
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)-8s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(loglevel)


def rest_of_word(word, index):
    """
    Given a word consisting of unique characters, return all the
    characters in the word except for the one at position index.
    :param word:
    :param index:
    :return:
    """
    new_word = ""
    for i in range(0, len(word)):
        if i != index:
            new_word += word[i]
    return new_word


def jumble(word):
    """
    A word with unique letters is jumbled by having each letter in turn
    begin the sequence and then adding it to the jumble of the remaining letters.
    :param word:
    :return:
    """
    if len(word) == 1:
        logger.debug("A stopping state is reached with {}".format(word))
        return list(word)

    scrambled_list = []
    for i in range(0, len(word)):
        jumble_list = jumble(rest_of_word(word, i))

        for jumble_list_item in jumble_list:
            scrambled_list.append(word[i] + jumble_list_item)

    logger.debug("scrambled_list:{}".format(scrambled_list))
    return scrambled_list


def display_list(jumbled_words_list, word_length, input_word):
    # Sort list as a prelude to eliminating duplicates in display
    jumbled_words_sorted = sorted(jumbled_words_list)
    logger.debug("My sorted jumbled list is:{}".format(jumbled_words_sorted))
    #
    # Let us now eliminate the dupes from this sorted list.
    prev_word = ""
    jumbled_words = []
    for word in jumbled_words_sorted:
        if prev_word != word:
            jumbled_words.append(word)
            prev_word = word

    logger.debug("My unique jumbled word list is:{}".format(jumbled_words))
    logger.info("All possible unique {} jumbles of word '{}' are: "
                .format(len(jumbled_words), input_word))
    #
    # Print in groups of 80//(length of (input word + space)) per line
    #
    line_capacity = 80 // (word_length + 1) - 1  # We start off at the 0 position
    logger.debug("Line capacity:{}".format(line_capacity + 1))
    i = 0
    display_line = ""

    for j in range(0, len(jumbled_words)):
        word = jumbled_words[j]

        if len(display_line) == 0:  # We don't want leading spaces
            display_line = word
        else:
            display_line = display_line + " " + word

        logger.debug("My display_line is currently:{}".format(display_line))
        if (i == line_capacity) or (j == len(jumbled_words) - 1):
            logger.info(display_line)
            display_line = ""
            i = 0
        else:
            i += 1


def main():
    parser = ArgumentParser(description="Display all jumbles of a word with unique letters")
    parser.add_argument('-l', '--loglevel', type=str, dest='loglevel', default='INFO',
                        choices=['CRITICAL', 'WARN', 'ERROR', 'INFO', 'DEBUG'], help='logging level')
    args = parser.parse_args()

    setup_logger(args.loglevel)
    word = input('Enter a word to scramble please: ')
    jumbled_words = jumble(word)
    # logger.info("All possible unique jumbles of word '{}' are: ".format(word))

    display_list(jumbled_words, len(word), word)

    return 0


if __name__ == '__main__':
    sys.exit(main())
