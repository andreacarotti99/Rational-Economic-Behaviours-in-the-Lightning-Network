from src.continuative_game.utils import queries
from src.continuative_game.changing_fees.run_infinite_simulation_fees import run_infinite_simulation
from src.continuative_game.params import *


def main():
    print(f'Keeping all edges, normalizing fee and capacity using alfa {alfa}')
    print_params()
    db_name = 'fees_alfa' + str(alfa) + '.db'
    queries.create_db(db_name=db_name)
    run_infinite_simulation(db=db_name)

if __name__ == "__main__":
    main()
