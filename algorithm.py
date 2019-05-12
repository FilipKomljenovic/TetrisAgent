import datetime
import multiprocessing
import multiprocessing as mp
import sys
from itertools import chain

import numpy as np

from agent import Agent
from evaluator import Evaluator

N_JOBS = multiprocessing.cpu_count()


def work(id, weights, l, seed):
    agent = Agent()
    agent.weights = weights[:]
    evaluator = Evaluator(id, agent, l)
    evaluator.seed = seed[:]
    return evaluator.evaluate()


class Algorithm:
    WEIGHTS_NUM = 8

    def __init__(self, mu, sigma, n, l, rho, zt, file):
        self.evaluator = None
        self.mu = mu
        self.sigma = sigma
        self.N = n
        self.l = l
        self.rho = rho
        self.zt = zt
        self.agents = [Agent() for i in range(0, n)]
        self.ids = [i for i in range(0, N_JOBS)]
        self.file = file
        self.curr_best = None

    def run(self):
        curr_best_ag = (0, 0)
        step = 0

        while curr_best_ag[0] < 1000:
            for i in range(0, self.N):
                self.agents[i].weights = np.random.multivariate_normal(self.mu, self.sigma).tolist()

            temp_results = []
            seed = [np.random.randint(2 << 30) for i in range(0, self.l)]
            pool = mp.Pool(N_JOBS)
            ids = [j for j in range(0, self.N)]
            result = [pool.apply_async(work, args=(id, self.agents[id].weights, self.l, seed)) for id in ids]
            output = [p.get() for p in result]
            temp_results.append(output)
            pool.close()
            pool.join()

            results = list(chain(*temp_results))
            results.sort(reverse=True)
            best_agents = self.rho * self.N
            elite = []

            for i in range(0, int(best_agents)):
                elite.append((results[i]))

            elite_matrix = np.zeros((int(best_agents), self.WEIGHTS_NUM))
            for i in range(0, len(elite)):
                elite_matrix[i] = elite[i][1]

            elite_matrix = elite_matrix.transpose()
            self.mu = np.mean(elite_matrix, 1)
            self.sigma = np.diag(np.diag(np.cov(elite_matrix) + self.zt))

            if self.curr_best is None or self.curr_best[0] < elite[0][0]:
                self.curr_best = elite[0]
            step += 1
            rew = [res[0] for res in results]
            mu_pop = np.mean(rew)
            var_pop = np.std(rew)
            print("mu:", mu_pop, " var:", var_pop, "\n", rew, "\n")

            self.file.write(''.join(map(str, self.curr_best)))
            self.file.write("\n")
            self.file.write(''.join(["mu:", str(mu_pop), " var:", str(var_pop)]))
            self.file.write(''.join(["\n", str(rew), "\n"]))
            self.file.write(str(datetime.datetime.now()))
            self.file.write("\n")
            self.file.flush()

        self.file.close()

    def get_agents(self):
        return self.agents


def run():
    weights_num = 8
    x = input('If you want to enter the initial parameters for algorithm, press Y, otherwise press any key\n').lower()
    if x.lower() == 'y':
        try:
            f = open(input('Please give path to file with parameters.\n'), 'r')
            a = list(f)
            mu = [float(a[0].rstrip()) for i in range(0, weights_num)]
            sigma = np.diag([float(a[1].rstrip()) for i in range(0, weights_num)])
            n = int(a[2].rstrip())
            f.close()
        except:
            print('Error while reading file.')
            sys.exit(0)
    else:
        mu = [0 for i in range(0, weights_num)]
        sigma = np.diag([100 for i in range(0, weights_num)])
        n = 100
    rho = 0.1
    l = 3
    zt = 4
    f = open("weights.txt", "w")
    algorithm = Algorithm(mu, sigma, n, l, rho, zt, f)
    algorithm.run()


if __name__ == '__main__':
    run()
