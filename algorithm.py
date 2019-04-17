import datetime
import multiprocessing as mp
from itertools import chain

import numpy as np

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
            # sum = dict.fromkeys([i for i in range(0, self.WEIGHTS_NUM)], 0)

            for i in range(0, int(best_agents)):
                elite.append((results[i]))

            # for el in elite:
            #     for col in range(0, self.WEIGHTS_NUM):
            #         sum[col] += el[1][col]

            # for i in range(0, self.WEIGHTS_NUM):
            # self.mu[i] = (sum[i] / self.WEIGHTS_NUM)

            elite_matrix = np.zeros((int(best_agents), self.WEIGHTS_NUM))
            for i in range(0, len(elite)):
                elite_matrix[i] = elite[i][1]

            elite_matrix = elite_matrix.transpose()
            self.mu = np.mean(elite_matrix, 1)

            self.sigma = np.diag(np.diag(np.cov(elite_matrix) + self.zt))
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
rho = 0.2
mu = [0 for i in range(0, weights_num)]
sigma = np.diag([100 for i in range(0, weights_num)])
l = 1
zt = 4
n = 104
f = open("weights.txt", "w")

algorithm = Algorithm(mu, sigma, n, rho, zt, f)
algorithm.run()
