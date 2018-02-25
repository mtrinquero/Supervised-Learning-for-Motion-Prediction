# Mark Trinquero
# Stochastic Movement



def stochastic_value(grid,goal,step_cost,collision_cost,success_prob):
    failure_prob = (1.0 - success_prob)/2.0 # Probability(stepping left) = prob(stepping right) = failure_prob
    value = [[collision_cost for col in range(len(grid[0]))] for row in range(len(grid))]
    policy = [[' ' for col in range(len(grid[0]))] for row in range(len(grid))]
    
    
    helper = True
    while helper:
        helper = False
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if goal[0] == x and goal[1] == y:
                    if value[x][y] > 0:
                        helper = True
                        value[x][y] = 0
                        policy[x][y] = '*'
                elif grid[x][y] == 0:
                    for a in range(len(delta)):
                        x_new           = x + delta[a][0]
                        x_new_left      = x + delta[(a + 1) % 4][0]
                        x_new_right     = x + delta[(a - 1) % 4][0]
                        y_new           = y + delta[a][1]
                        y_new_left      = y + delta[(a + 1) % 4][1]
                        y_new_right     = y + delta[(a - 1) % 4][1]
                        new_value       = step_cost

                        

                        if x_new >= 0 and x_new < len(grid) and y_new >= 0 and y_new < len(grid[0]) and grid[x_new][y_new] == 0:
                            new_value += success_prob * value[x_new][y_new]
                        else:
                            new_value += success_prob * collision_cost

                        

                        if x_new_left >= 0 and x_new_left < len(grid) and y_new_left >= 0 and y_new_left < len(grid[0]) and grid[x_new_left][y_new_left] == 0:
                            new_value += failure_prob * value[x_new_left][y_new_left]
                        else:
                            new_value += failure_prob * collision_cost
                        
                        

                        if x_new_right >= 0 and x_new_right < len(grid) and y_new_right >= 0 and y_new_right < len(grid[0]) and grid[x_new_right][y_new_right] == 0:
                            new_value += failure_prob * value[x_new_right][y_new_right]
                        else:
                            new_value += failure_prob * collision_cost     
                        
                        

                        if new_value < value[x][y]:
                            helper          = True
                            value[x][y]     = new_value
                            policy[x][y]    = delta_name[a]
    
    return value, policy
