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
        logger.debug(f"A stopping state is reached with {word}")
        return list(word)

    scrambled_list = []
    for i in range(0, len(word)):
        jumble_list = jumble(rest_of_word(word, i))

        for jumble_list_item in jumble_list:
            scrambled_list.append(word[i] + jumble_list_item)

    logger.debug(f"scrambled_list:{scrambled_list}")
    return scrambled_list


def display_list(jumbled_words_list, word_length, input_word):
    # Sort list as a prelude to eliminating duplicates in display
    jumbled_words_sorted = sorted(set(jumbled_words_list))

    logger.debug(f"My unique jumbled word list is:{jumbled_words_sorted}")
    logger.info(f"All possible unique {len(jumbled_words_sorted)} jumbles of word '{input_word}' are: ")
    #
    # Print in groups of 80//(length of (input word + space)) per line
    #
    line_capacity = 80 // (word_length + 1) - 1  # We start off at the 0 position
    logger.debug(f"Line capacity:{line_capacity+1}")
    i = 0
    display_line = ""

    for j in range(0, len(jumbled_words_sorted)):
        word = jumbled_words_sorted[j]

        if len(display_line) == 0:  # We don't want leading spaces
            display_line = word
        else:
            display_line = display_line + " " + word

        logger.debug(f"My display_line is currently:{display_line}")
        if (i == line_capacity) or (j == len(jumbled_words_sorted) - 1):
            logger.info(display_line)
            display_line = ""
            i = 0
        else:
            i += 1


def main():
    # ToDo: Add an argument and logic for passing the input word from the command line
    #  The command line input would then bypass the input() call
    parser = ArgumentParser(description="Display all jumbles of a word with unique letters")
    parser.add_argument('-l', '--loglevel', type=str, dest='loglevel', default='INFO',
                        choices=['CRITICAL', 'WARN', 'ERROR', 'INFO', 'DEBUG'], help='logging level')
    args = parser.parse_args()

    setup_logger(args.loglevel)
    word = input('Enter a word to scramble please: ')
    jumbled_words = jumble(word)

    display_list(jumbled_words, len(word), word)

    return 0


if __name__ == '__main__':
    sys.exit(main())
