import datetime
from itertools import chain
import numpy as np
import random as rand
import multiprocessing as mp
from joblib import Parallel, delayed

from agent import Agent
from evaluator import Evaluator

N_JOBS = 8
l = 1


def work(id, agents, l):
    evaluator = Evaluator(id)
    evaluator.set_agent(agents[id])
    evaluator.set_games_num(l)
    return evaluator.evaluate()


class Algorithm:
    l = 1
    WEIGHTS_NUM = 8

    def __init__(self, mu, sigma, n, rho, zt, file):
        self.evaluator = None
        self.mu = mu
        self.sigma = sigma
        self.N = n
        self.rho = rho
        self.zt = zt
        self.agents = [Agent() for i in range(0, n)]
        self.ids = [i for i in range(0, N_JOBS)]
        self.file = file

    def run(self):
        curr_best_ag = (0, 0)
        step = 0

        while curr_best_ag[0] < 1000:
            for i in range(0, self.N):
                self.agents[i].weights = self.sigma * np.random.randn(1, 8) * self.mu

            self.reset()
            temp_results = []

            pool = mp.Pool(N_JOBS)
            for i in range(0, self.N, N_JOBS):
                ids = [j for j in range(0, self.N)]
                result = [pool.apply_async(work, args=(id, self.agents, Algorithm.l)) for id in ids]
                output = [p.get() for p in result]
                temp_results.append(output)
            pool.close()
            pool.join()

            # while n < self.N:
            #     ids = [i for i in range(n, N_JOBS + n)]
            #     n += N_JOBS
            #     temp_results.append(Parallel(n_jobs=N_JOBS, verbose=10, backend="multiprocessing")(
            #         delayed(work)(id, self.agents, self.l) for id in ids))

            results = list(chain(*temp_results))
            results.sort(reverse=True)
            best_agents = self.rho * self.N
            elite = []
            sum = dict.fromkeys([i for i in range(0, self.WEIGHTS_NUM)], 0)

            for i in range(0, int(best_agents)):
                elite.append((results[i]))

            for el in elite:
                for col in range(0, self.WEIGHTS_NUM):
                    sum[col] += el[1][col]

            for i in range(0, self.WEIGHTS_NUM):
                self.mu[i] = (sum[i] / self.WEIGHTS_NUM)

            self.sigma = np.cov(self.mu)
            curr_best_ag = elite[0]
            step += 1

            if step % 2 == 0:
                self.file.write(str(curr_best_ag))
                self.file.write("\n")
                self.file.write(str(datetime.datetime.now()))

    def get_agents(self):
        return self.agents

    def reset(self):
        self.mu = [0 for i in range(0, weights_num)]


weights_num = 8
rho = 0.1
mu = [0 for i in range(0, weights_num)]
sigma = np.diag([100 for i in range(0, weights_num)])
l = 1
zt = 4
n = 16
f = open("weights.txt", "w+")

algorithm = Algorithm(mu, sigma, n, rho, zt, f)
algorithm.run()
