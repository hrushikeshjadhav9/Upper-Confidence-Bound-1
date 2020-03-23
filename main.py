import random
import matplotlib.pyplot as plt
import numpy as np

class Slot_machine():
    """ a simple slot machine """

    def __init__(self, mean):
        """

        :param mean: actual win rate
        mean_estimate: current mean estimate
        N: number of plays a the slot machine
        """
        self.mean = mean
        self.mean_estimate = 0
        self.N = 0
        self.x = 0

    def pull(self):
        """ modeled pull operation in a slot machine """
        self.x = self.mean + np.random.randn()
        self.update()
        return self.x

    def update(self):
        """ updates mean estimate and tracks number of pulls """
        self.N += 1
        self.mean_estimate = (1.0 - (1.0 / self.N)) * self.mean_estimate + (1.0 / self.N) * self.x


def ucb(mean_estimate, N, Nj):
    if Nj == 0:
        return float('inf')
    return mean_estimate + np.sqrt(2*np.log(N)/Nj)

def experiment(N,  *means):
    """ compares epsilon values given by user """
    all_sm = [Slot_machine(mean) for mean in means]

    # records actual mean estimates of pulled slot machines
    all_pulls = np.empty(N)

    for i in range(N):

        index = np.argmax([ucb(sm.mean_estimate, i+1, sm.N) for sm in all_sm])
        x = all_sm[index].pull()
        all_pulls[i] = x

        # Tracking progress through time
        cumulative_average = np.cumsum(all_pulls)/(np.arange(N)+1)

    return all_pulls, cumulative_average


if __name__ == "__main__":

    # Number of plays / pulls.
    N = 2000
    pulls, cumulative_average = experiment(N, 0.1, 0.3, 0.5)

    # plt.plot(pulls)
    # plt.ylabel("all slot machine pulls")
    # plt.xlabel("iteration")
    # plt.show()

    plt.plot(cumulative_average)
    plt.ylabel("cumulative average")
    plt.xlabel("pull count")
    plt.show()

