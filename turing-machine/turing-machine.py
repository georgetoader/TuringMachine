# Python 3.0

import sys


# build internal representation of TM
def readTM():
    nr_states = int(sys.stdin.readline().strip())
    final_states = sys.stdin.readline().strip().split()
    transitions = sys.stdin.read().strip().split('\n')
    # tuple containing TM internal representation
    TM = (nr_states, final_states, transitions)
    return TM


# returns new TM configuration after 1 transition is completed
def step(TM, TM_input):
    # split the input containing the left&right words and the current state
    # use variable "complete" to return after 1 transition is over
    TM_input = TM_input.split(',')
    complete = False
    # search for a matching transition
    # TM[2] stores all transitions
    for transition in TM[2]:
        values = transition.split()
        # check matching current state and current value
        if int(values[0]) == int(TM_input[1]) and values[1] == TM_input[2][0]:
            # found matching transition
            complete = True
            # change current state and value
            TM_input[1] = values[2]
            TM_input[2] = values[3] + TM_input[2][1:]
            if values[4] == 'R':
                # move cursor to the right
                # add the current value to the end of left word
                TM_input[0] = TM_input[0] + TM_input[2][0]
                if len(TM_input[2]) == 2:
                    # if there are no more values left in right word add "#"
                    TM_input[2] = "#)"
                else:
                    # remove the first value in right word
                    TM_input[2] = TM_input[2][1:]
            elif values[4] == 'L':
                # move cursor to the left
                # add value from left word to the beginning of right word
                TM_input[2] = TM_input[0][-1:] + TM_input[2]
                if len(TM_input[0]) == 2:
                    # if there are no more values left in left word add "#"
                    TM_input[0] = "(#"
                else:
                    # remove the last value in left word
                    TM_input[0] = TM_input[0][:-1]
        # if 1 transition has been completed exit
        if complete:
            break
    # if no transitions have been completed return False
    if not complete:
        return False
    # return the new configuration
    separator = ','
    return separator.join(TM_input)


# check if word is accepted by TM
def accept(TM, word):
    # if there are no final states the word can't be accepted
    if TM[1][0] == '-':
        return False
    # form the configuration based on the new input
    TM_input = "(#,0," + word + ")"
    # loop to complete all transitions available
    # update the configuration after every step
    while True:
        TM_input = step(TM, TM_input)
        # if no transitions were completed in last step return False
        if not TM_input:
            return False
        # check to see if it reached a final state
        state = TM_input.split(',')
        for i in TM[1]:
            if int(state[1]) == int(i):
                return True


# check if word is accepted by TM in k steps
def k_accept(TM, word, k):
    # if there are no final states the word can't be accepted
    if TM[1][0] == '-':
        return False
    TM_input = "(#,0," + word + ")"
    while k > 0:
        TM_input = step(TM, TM_input)
        # if no transitions were completed in last step return False
        if not TM_input:
            return False
        state = TM_input.split(',')
        # check to see if it reached a final state
        for i in TM[1]:
            if int(state[1]) == int(i):
                return True
        # subtract the number of steps
        k -= 1
    # the word wasn't accepted in k steps so return False
    return False


def main():
    test = sys.stdin.readline().strip()
    inputs = sys.stdin.readline().strip().split()
    TM = readTM()
    # based on the value in "test" call certain functions
    # for every value in "inputs" call the specific function(step/accept/k_accept)
    if test == "step":
        for i in range(0, len(inputs)):
            new_config = step(TM, inputs[i])
            print(new_config, end=" ")
    elif test == "accept":
        for i in range(0, len(inputs)):
            res = accept(TM, inputs[i])
            print(res, end=" ")
    elif test == "k_accept":
        for i in range(0, len(inputs)):
            values = inputs[i].split(',')
            res = k_accept(TM, values[0], int(values[1]))
            print(res, end=" ")


if __name__ == "__main__":
    main()
