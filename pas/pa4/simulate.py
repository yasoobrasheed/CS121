# CS121: Polling places
#
# Yasoob Rasheed
#
# Main file for polling place simulation

import sys
import util
import random
import queue
import click

class Voter(object):
    '''
    Initialize voter object with:
        arrival_time (float)
        voting_duration (float)
        start_time (float or None)
        departure_time (float or None)
    '''
    def __init__(self, a_t, v_d, s_t, d_t):
        self.arrival_time = a_t
        self.voting_duration = v_d
        self.start_time = s_t
        self.departure_time = d_t

    '''
    Return arrival time (float)
    '''
    @property
    def arrival_time(self):
        return self.arrival_time

    '''
    Set the arrival_time to the parameter given (no return value)
    '''
    @arrival_time.setter
    def arrival_time(self, arrival_time): 
        self.arrival_time = arrival_time

    '''
    Return voting_duration (float)
    '''
    @property
    def voting_duration(self):
        return self.voting_duration

    '''
    Set the start_time to the parameter given (no return value)
    '''
    @voting_duration.setter
    def voting_duration(self, voting_duration): 
        self.voting_duration = voting_duration

    '''
    Return start_time (float or None)
    '''
    @property
    def start_time(self):
        return self.start_time

    '''
    Set the start_time to the parameter given (no return value)
    '''
    @start_time.setter
    def start_time(self, start_time): 
        self.start_time = start_time

    '''
    Return departure_time (float or None)
    '''  
    @property  
    def departure_time(self):
        return self.departure_time

    '''
    Set the departure_time to the parameter given (no return value)
    '''
    @departure_time.setter
    def departure_time(self, departure_time):
        #if not isinstance(x, (int, float)):
        #   raise ValueError("Not a number") 
        self.departure_time = departure_time

    
class VoterGenerator(object):

    '''
    Initialize voter generator object with:
        arrival_rate (float)
        voting_duration_rate (float)
        timer (int) initialized to 0 
    '''
    def __init__(self, arrival_rate, voting_duration_rate):
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate
        self.timer = 0

    '''
    Generate a new voter with given poisson parameters
    set the arrival_time and voter_duration time of the voter
    increment the timer by the voting gap

    Variables:
        parameters: returns a tuple with the pseudo-randomized rates
        voter_gap: pseudo-randomized voter_gap from parameters
        voting_duration: pseudo-randomized voting duration

    Returns: Voter class object with arrival time and voting duration set
    '''
    def next(self):
        a_r = self.arrival_rate
        v_d_r = self.voting_duration_rate
        parameters = util.gen_poisson_voter_parameters(a_r, v_d_r)
        voter_gap = parameters[0]
        voting_duration = parameters[1]
        self.timer += voter_gap
        return Voter(self.timer, voting_duration, None, None)


class Precinct(object):
    '''
    Initialize voter generator object with:
        num_booths (int)
        PriorityQueue initialized with a max of num_booths
    '''
    def __init__(self, num_booths):
        self.num_booths = num_booths
        self.PRIORITY_QUEUE = queue.PriorityQueue(num_booths)
    
    '''
    Set the start and departure times of each voter
    If the queue is not full, add the voter and set both Variables
    equal to what they should be respectively
    If the queue is full, follow conditional logic to set the 
    respective times

    Returns: Voter class object with start time and departure time set
    '''
    def add_voter(self, voter_generator):
        voter = voter_generator.next()
        arrival_time = voter.arrival_time
        voting_duration = voter.voting_duration

        if not self.PRIORITY_QUEUE.full():
            voter.start_time = arrival_time
            voter.departure_time = arrival_time + voting_duration
            self.PRIORITY_QUEUE.put((voter.departure_time, voter))

        elif self.PRIORITY_QUEUE.full():
            last_voter = self.PRIORITY_QUEUE.get()

            if arrival_time > last_voter[0]:
                voter.start_time = arrival_time
            else:
                voter.start_time = last_voter[0]
            voter.departure_time = voter.get_start_time() + voting_duration

            self.PRIORITY_QUEUE.put((voter.departure_time, voter))

        return voter
        

def simulate_election_day(precincts, seed=0):
    '''
    Loop through all the precincts and put arrays of voters in that 
    precinct with their details in a dictionary
    If the voter comes once the booth is closed, they are not allowed to vote

    Variables:
        d: dictionary holding each key: precint name and value: voters array
        voters: array holding each initialized Voter object
        prec: Precinct object
        generator: VoterGenerator object
        voter: Voter object created by prec method

    Returns: dictionary of the form {'name': [Voter, Voter, ...]}
    '''
    d = {}

    for precinct in precincts:
        voters = []
        prec = Precinct(precinct['num_booths'])
        a_r = precinct['voter_distribution']['arrival_rate']
        v_d_r = precinct['voter_distribution']['voting_duration_rate']
        random.seed(seed)
        generator = VoterGenerator(a_r, v_d_r)
        for i in range(precinct['num_voters']):
            voter = prec.add_voter(generator)
            if voter.arrival_time <= precinct['hours_open'] * 60:
                voters.append(voter)
        d[precinct['name']] = voters

    return d


def find_avg_wait_time(precinct, num_booths, ntrials, initial_seed=0):
    '''
    Find the average wait time for each trial randomized slightly
    by the changing seed

    Variables:
        avg_wait_times_array: array holding avg wait times 
        wait_times_array: array holding the wait times
        wait_time: float containing the wait time
        avg_wait_time: float avereaging the wait times in wait_times_array

    Returns: median of the wait times in avg_wait_times_array (float)
    '''

    avg_wait_times_array = []

    for i in range(0, ntrials):
        random.seed(initial_seed + i)
        prec = Precinct(num_booths)
        a_r = precinct['voter_distribution']['arrival_rate']
        v_d_r = precinct['voter_distribution']['voting_duration_rate']
        generator = VoterGenerator(a_r, v_d_r)
        wait_times_array = []
        for i in range(precinct['num_voters']):
            voter = prec.add_voter(generator)
            wait_time = voter.start_time - voter.arrival_time
            wait_times_array.append(wait_time)
        avg_wait_time = sum(wait_times_array) / len(wait_times_array)
        avg_wait_times_array.append(avg_wait_time)


    avg_wait_times_array.sort()

    return avg_wait_times_array[ntrials // 2]


def find_number_of_booths(precinct, target_wait_time, max_num_booths, ntrials, seed=0):
    '''
    Find the number of booths that give an average lower than the
    target wait time

    Variables:
        avg_wait_time: call to the previous avg_wait_time function (float)

    Returns: tuple with (ideal num_booths, avg_wait_time for those booths)
             if none meet the target: return (0, None)
    '''
    
    for num_booths in range(1, max_num_booths + 1):
        avg_wait_time = find_avg_wait_time(precinct, num_booths, ntrials, seed)
        if avg_wait_time < target_wait_time:
            return (num_booths, avg_wait_time)
    return (0, None)


@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--max-num-booths', type=int)
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, max_num_booths, target_wait_time, print_voters):
    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = simulate_election_day(precincts, seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    return -1
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        if max_num_booths is None:
            max_num_booths = precinct["num_voters"]

        nb, avg_wt = find_number_of_booths(precinct, target_wait_time, max_num_booths, 20, seed)

        if nb is 0:
            msg = "The target wait time ({:.2f}) is infeasible"
            msg += " in precint '{}' with {} or less booths"
            print(msg.format(target_wait_time, precinct["name"], max_num_booths))
        else:
            msg = "Precinct '{}' can achieve average waiting time"
            msg += " of {:.2f} with {} booths"
            print(msg.format(precinct["name"], avg_wt, nb))


if __name__ == "__main__":
    cmd()