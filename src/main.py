from scanner import Scanner


def main():
    sas = Scanner(open('../test/example.ft'))
    print(sas.getNextToken())
    print(sas.getNextToken())
    print(sas.getNextToken())
    print(sas.getNextToken())
    print(sas.getNextToken())

if __name__ == '__main__':
    main()
