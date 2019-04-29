import datetime
import multiprocessing as mp
from itertools import chain
from sys import maxsize
import numpy as np

from agent import Agent
from evaluator import Evaluator

N_JOBS = 4


def work(id, weights, l,seed):
    evaluator = Evaluator(id)
    agent=Agent()
    agent.weights=weights[:]
    evaluator.set_agent(agent)
    evaluator.set_games_num(l)
    evaluator.seed=seed
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
                self.agents[i].weights = np.random.multivariate_normal(self.mu,self.sigma).tolist()

            temp_results = []
            seed=np.random.randint(2<<30)
            pool = mp.Pool(N_JOBS)
            ids = [j for j in range(0, self.N)]
            result = [pool.apply_async(work, args=(id, self.agents[id].weights, self.l,seed)) for id in ids]
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
            rew=[res[0] for res in results]
            print("mu:",np.mean(rew)," var:",np.std(rew),"\n",rew,"\n")
            if step % 2 == 0:
                self.file.write(''.join(map(str, self.curr_best)))
                self.file.write("\n")
                self.file.write(' '.join(["mu:",str(np.mean(rew))," var:",str(np.std(rew))]))
                self.file.write(' '.join(["\n",str(rew),"\n"]))
                self.file.write(str(datetime.datetime.now()))
                self.file.write("\n")
                self.file.flush()

        self.file.close()

    def get_agents(self):
        return self.agents


def run():
    weights_num = 8
    rho = 0.1
    mu = [0 for i in range(0, weights_num)]
    sigma = np.diag([100 for i in range(0, weights_num)])
    l = 1
    zt = 4
    n = 52
    f = open("weights.txt", "w")
    algorithm = Algorithm(mu, sigma, n, l, rho, zt, f)
    algorithm.run()


if __name__ == '__main__':
    run()
