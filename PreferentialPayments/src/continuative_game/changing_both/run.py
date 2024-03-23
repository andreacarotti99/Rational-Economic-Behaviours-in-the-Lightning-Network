from src.continuative_game.changing_both.infinite_simulation import infinite_simulation
from src.continuative_game.params import print_params, alfa, distribution
from src.continuative_game.utils import queries


def main():
    print('Changing both: CHANNELS and FEES')
    print_params()

    db_name = f'channels_alfa{alfa}_{distribution[0:4]}_BOTH.db'
    queries.create_db(db_name=db_name)
    infinite_simulation(db=db_name)

if __name__ == "__main__":
    main()
