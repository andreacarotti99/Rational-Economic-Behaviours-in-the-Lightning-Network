def node_degree_dist():
    return '''
    SELECT
    Node_degree / 2 as Node_channels,
    SimulationNumber
    FROM
        node
    WHERE
        SimulationNumber <= 1000 and Node_capacity > 0
    ORDER BY
        SimulationNumber, Node_degree;
    '''



def avgFee_avgRatio_allNodes():
    return '''
    SELECT
    SUM(Node_earning)/sum(Node_routing) as AvgFee, 
       sum(Increased_profit) as NodeIncreasingProfitInSimulation
    FROM
        node
    GROUP BY
        SimulationNumber;
    '''

def avgFee_avgRatio_top100HCN():
    return '''
    SELECT
    SUM(Node_earning)/sum(Node_routing) as AvgFee, sum(Node_earning)/sum(Node_capacity) as AvgRatio, SimulationNumber,
        sum(Increased_profit) as NodeIncreasingProfitInSimulation
    FROM
        node
    WHERE
        SimulationId = 1
        AND Node_pub_key IN (
                SELECT Node_pub_key
                FROM node
                WHERE SimulationId = 1 and SimulationNumber = 0 and Node_capacity > 0
                ORDER BY Node_capacity desc
                LIMIT 200
        )
    GROUP BY
        SimulationNumber;
    '''

def avgFee_avgRatio_least100HCN():
    return '''
    SELECT
    SUM(Node_earning)/sum(Node_routing) as AvgFee, sum(Node_earning)/sum(Node_capacity) as AvgRatio, SimulationNumber
    FROM
        node
    WHERE
        SimulationId = 1
        AND Node_pub_key IN (
                SELECT Node_pub_key
                FROM node
                WHERE SimulationId = 1 and SimulationNumber = 0 and Node_capacity > 0
                ORDER BY Node_capacity asc
                LIMIT 200
        )
    GROUP BY
        SimulationNumber;
    '''

def avgFee_query(max_simulation_number):
    return f'''
    SELECT
        SUM(Node_earning)/SUM(Node_routing) as AvgFee,
        SimulationNumber
    FROM node
    WHERE SimulationNumber <= {max_simulation_number}
    GROUP BY
        SimulationNumber;
    '''

def increased_profit(max_simulation_number, group_size):
    return f'''
    SELECT
        SUM(Increased_profit) as TotalIncreasedProfit,
        (SimulationNumber - 1) / {group_size} as SimulationGroup
    FROM
        node
    WHERE SimulationNumber <= {max_simulation_number} and SimulationNumber >= 1
    GROUP BY
        SimulationGroup;
    '''


# Query for average fee for top 200 nodes in capacity
def avgFee_top200_query():
    return '''
    SELECT
        SUM(Node_earning)/SUM(Node_routing) as AvgFee,
        SimulationNumber
    FROM
        node
    WHERE
        Node_pub_key IN (
            SELECT Node_pub_key
            FROM node
            
            ORDER BY Node_capacity desc
            LIMIT 200
        )
        and
        SimulationNumber <= 200
    GROUP BY
        SimulationNumber;
    '''
