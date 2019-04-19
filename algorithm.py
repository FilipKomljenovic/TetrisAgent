import datetime
import multiprocessing as mp
from itertools import chain

import numpy as np

from agent import Agent
from evaluator import Evaluator

N_JOBS = 8


def work(id, agents, l):
    evaluator = Evaluator(id)
    evaluator.set_agent(agents[id])
    evaluator.set_games_num(l)
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
                self.agents[i].weights = np.diag(self.sigma * np.random.randn(1, 8) + self.mu).tolist()

            temp_results = []

            pool = mp.Pool(N_JOBS)
            for i in range(0, self.N, N_JOBS):
                ids = [j for j in range(i, N_JOBS + i)]
                result = [pool.apply_async(work, args=(id, self.agents, self.l)) for id in ids]
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
            self.sigma = np.sqrt(np.diag(np.diag(np.cov(elite_matrix) + self.zt)))

            if self.curr_best is None or self.curr_best[0] < elite[0][0]:
                self.curr_best = elite[0]
            step += 1

            if step % 2 == 0:
                self.file.write(''.join(map(str, self.curr_best)))
                self.file.write("\n")
                self.file.write(str(datetime.datetime.now()))
                self.file.write("\n")
                self.file.flush()

        self.file.close()

    def get_agents(self):
        return self.agents


weights_num = 8
rho = 0.1
mu = [0 for i in range(0, weights_num)]
sigma = np.diag([100 for i in range(0, weights_num)])
l = 1
zt = 4
n = 104
f = open("weights.txt", "w")

algorithm = Algorithm(mu, sigma, n, l, rho, zt, f)
algorithm.run()
