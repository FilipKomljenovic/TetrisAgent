from joblib import Parallel, delayed

from evaluator import Evaluator

N_JOBS = -1


def work(id):
    evaluator = Evaluator(id)
    return evaluator.evaluate()


ids = range(0, N_JOBS)
# results = []
# with Parallel(n_jobs=-1, backend="multiprocessing") as parallel:
#     n_iter = 0
#     while len(results) < 30:
#         results.append(parallel(map(delayed(work), ids)))
#         n_iter += N_JOBS

# pool = Pool(N_JOBS)
# results = pool.map(work, ids)
results = Parallel(n_jobs=N_JOBS, verbose=0, backend="multiprocessing")(map(delayed(work), ids))
best = 0
index = 0

for i in range(0, len(results)):
    if results[i][0] > best:
        best = results[i][0]
        index = i

print(len(results))
print("\n")
print("Best agent score:", best, "\nWeights:", results[index][1])
