import sys


def guide():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--help':
            return "HELP"


def url_generator(List_Of_Commands):
    commands = ""

    for i in range(0, len(List_Of_Commands)):
        if (i % 2 == 0) & (i != 0):
            commands += "+"

        commands += List_Of_Commands[i]

        if i % 2 == 0:
            commands += ":"

    url = "https://inspirehep.net/search?p=" + commands + \
        "&of=recjson&ot=creator,abstract,creation_date," + \
        "primary_report_number,number_of_citations,title," + \
        "system_control_number,source_of_acquisition,FIXME_OAI"

    return url


def main():
    print(guide())


if __name__ == "__main__":
    main()
