import datetime as dt

# Global variables
START_TIME = dt.datetime.now()


def main():


    print(f'Total execution time:\t\t{(dt.datetime.now() - START_TIME)}')


if __name__ == "__main__":
    main()