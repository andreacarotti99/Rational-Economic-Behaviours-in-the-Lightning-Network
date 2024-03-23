import sqlite3
from src.Simulation import Simulation


def create_db(db_name: str):
    db = db_name
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    create_simulation_table_sql = """
    CREATE TABLE IF NOT EXISTS simulation (
        Simulation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_path TEXT,
        payments_to_simulate INTEGER,
        payments_amount INTEGER,
        distribution TEXT,
        dist_func TEXT,
        tentative_nodes_to_keep INTEGER,
        alfa REAL,
        strategy_for_target TEXT,
        weight_func TEXT
    );
    """

    create_node_table_sql = """
    CREATE TABLE IF NOT EXISTS node (
        SimulationId INTEGER,
        SimulationNumber INTEGER,
        Node_pub_key TEXT,
        Node_earning REAL,
        Node_routing INTEGER,
        Node_degree INTEGER,
        Node_capacity INTEGER,
        Increased_profit INTEGER,
        FOREIGN KEY (SimulationId) REFERENCES simulation(Simulation_id)
    );
    """
    cursor.execute(create_simulation_table_sql)
    cursor.execute(create_node_table_sql)
    conn.commit()
    conn.close()

def db_insert_simulation_params(db_file, table_name, variables):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        insert_sql = f'''
            INSERT INTO {table_name} (
                snapshot_path,
                payments_to_simulate,
                payments_amount,
                distribution,
                dist_func,
                tentative_nodes_to_keep, 
                alfa,
                strategy_for_target,
                weight_func
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(insert_sql, variables)
        simulation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return simulation_id

    except sqlite3.Error as e:
        print(f"Error inserting variables: {e}")
        return None

def db_insert_simulation_results(db_file: str, simulation: Simulation, simulation_id: int, simulation_number: int):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        for node_pub_key in simulation.pathMap.channel_graph.network.nodes:
            if node_pub_key in simulation.nodes_earning:
                node_earning = simulation.nodes_earning[node_pub_key]
                node_routing = simulation.nodes_routing[node_pub_key]
            else:
                node_earning = 0
                node_routing = 0
            node_degree = simulation.pathMap.channel_graph.network.degree(node_pub_key)
            node_capacity = simulation.pathMap.channel_graph.get_expected_capacity(node_pub_key)


            variables = (simulation_id, simulation_number, node_pub_key, node_earning, node_routing, node_degree, node_capacity, 0)

            insert_sql = f'''
                INSERT INTO node (
                    SimulationId,
                    SimulationNumber,
                    Node_pub_key,
                    Node_earning,
                    Node_routing,
                    Node_degree,
                    Node_capacity,
                    Increased_profit
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(insert_sql, variables)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error inserting variables: {e}")


def update_increased_profit(db_file: str, simulation_id: int, simulation_number: int, node_pub_key: str):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        update_sql = '''
            UPDATE node
            SET Increased_profit = ?
            WHERE SimulationId = ? AND SimulationNumber = ? AND Node_pub_key = ?
        '''

        cursor.execute(update_sql, (1, simulation_id, simulation_number, node_pub_key))
        conn.commit()
    except sqlite3.Error as e:
        print(f'Error updating increased_profit: {e}')
    finally:
        if conn:
            conn.close()
