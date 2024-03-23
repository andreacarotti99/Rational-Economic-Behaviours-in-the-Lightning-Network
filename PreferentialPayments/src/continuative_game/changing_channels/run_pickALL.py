from src.continuative_game.utils import queries
from src.continuative_game.changing_channels.infinite_simulation_channels_pickALL import run_infinite_simulation
from src.continuative_game.params import *

'''
Before running the script, edit the configuration file 'params.py'
'''

def main():
    print(f'Keeping all edges, normalizing fee and capacity using alfa {alfa}')
    print_params()
    db_name = f'channels_alfa{alfa}_{distribution[0:4]}_ALL.db'
    queries.create_db(db_name=db_name)
    run_infinite_simulation(db=db_name)

if __name__ == "__main__":
    main()
