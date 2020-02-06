#The values in the distance matrix has been rounded off to prodice whole numbers because routing solver works only with integers.
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def create_data_model():
    data = {}
    data['distance_matrix'] = [
        [0,12113,7722,8079,16573,16824,16422,12989,16741,16549,15879,16947,15546,16512,16288,6058,13873,8130,14286,13564,13063,11675],
        [12113,0,5620,6805,4805,4711,4333,1596,10259,4451,3911,5158,3629,4641,4243,6327,2155,8054,12908,13990,11813,446],
        [7722,5620,0,1919,8898,9530,9048,5658,12618,9190,8383,9259,8046,8885,8837,2203,6490,3373,13801,14769,17172,5232],
        [8079,6805,1919,0,8867,9780,9301,6337,11341,9438,8611,9175,8302,8926,9057,3807,7021,1477,12043,12921,18553,6494],
        [16573,4805,8898,8867,0,1215,985,3652,5470,1020,930,380,1177,238,828,10524,2789,9257,8157,9193,9807,5202],
        [16824,4711,9530,9780,1215,0,486,3947,5891,345,1174,1194,1498,1027,723,10873,3072,10323,8582,9487,8834,5148],
        [16422,4333,9048,9301,985,486,0,3485,6122,142,691,1119,1012,753,256,10425,2605,9874,8824,9778,9306,4763],
        [12989,1596,5658,6337,3652,3947,3485,0,8930,3623,2890,4030,2557,3545,3314,6947,885,7342,11489,12632,12217,1823],
        [16741,10259,12618,11341,5470,5891,6122,8930,0,6039,6390,5137,6645,5655,6135,14805,8151,10583,2703,3731,8160,10635],
        [16549,4451,9190,9438,1020,345,142,3623,6039,0,829,1104,1153,799,382,10561,2744,9999,8740,9681,9173,4883],
        [15879,3911,8383,8611,930,1174,691,2890,6390,829,0,1254,340,736,456,9834,2006,9203,9083,10104,9994,4321],
        [16947,5158,9259,9175,380,1194,1119,4030,5137,1104,1254,0,1531,519,1039,10902,3164,9507,7833,8850,9522,5561],
        [15546,3629,8046,8302,1177,1498,1012,2557,6645,1153,340,1531,0,1018,791,9498,1674,8932,9326,10369,10294,4030],
        [16512,4641,8885,8926,238,1027,753,3545,5655,799,736,519,1018,0,589,10454,2671,9366,8349,9369,9729,5045],
        [16288,4243,8837,9057,828,723,256,3314,6135,382,456,1039,791,589,0,10260,2430,9619,8836,9819,9555,4665],
        [6058,6327,2203,3807,10524,10873,10425,6947,14805,10561,9834,10902,9498,10454,10260,0,7831,5036,15843,16613,15983,5883],
        [13873,2155,6490,7021,2789,3072,2605,885,8151,2744,2006,3164,1674,2671,2430,7831,0,7903,10767,11877,11535,2493],
        [8130,8054,3373,1477,9257,10323,9874,7342,10583,9999,9203,9507,8932,9366,9619,5036,7903,0,10829,11599,18737,7788],
        [14286,12908,13801,12043,8157,8582,8824,11489,2703,8740,9083,7833,9326,8349,8836,15843,10767,10829,0,1202,8085,13260],
        [13564,13990,14769,12921,9193,9487,9778,12632,3731,9681,10104,8850,10369,9369,9819,16613,11877,11599,1202,0,7431,14365],
        [13063,11813,17172,18553,9807,8834,9306,12217,8160,9173,9994,9522,10294,9729,9555,15983,11535,18737,8085,7431,0,12149],
        [11675,446,5232,6494,5202,5148,4763,1823,10635,4883,4321,5561,4030,5045,4665,5883,2493,7788,13260,14365,12149,0]
    ]                                           #stores the distances from one node to another   
    data['num_vehicles'] = 1                    #stores the number of salesperson
    data['depot'] = 0                           #stores the index of the starting point of the salesperson
    return data


def print_solution(manager, routing, assignment):
    print('\tDistance covered : {} kilometres\n'.format(assignment.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = '\tRaces to be followed in the order :\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += '\t {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = assignment.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    print(plan_output)
    plan_output += 'Route distance: {}kilometres\n'.format(route_distance)


def main():
    data = create_data_model()
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    assignment = routing.SolveWithParameters(search_parameters)             #solving the problem
    if assignment:
        print_solution(manager, routing, assignment)                        #prints the route to be followed

if __name__ == '__main__':
    main()

